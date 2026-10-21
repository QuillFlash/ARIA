#!/usr/bin/env python3
"""ARIA budget and cache checker.

Simulates SillyTavern turns for ARIA's Chat Completions and Text Completions
presets, counts the rendered tokens (characters / 4, comments stripped) for a
few configurations, and fails when something would break the budget, the
wiring or prompt caching.

Usage: python3 tools/aria_budget.py [preset.json ...]   (no arguments: every preset in DEFAULT_PRESETS)
"""
import json
import random
import re
import sys
from pathlib import Path

BUDGET = 7500
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PRESETS = [
    ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json",
    ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",
    ROOT / "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json",
    ROOT / "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json",
]
VOLATILE = re.compile(r'\{\{(roll|random|pick|time|date|weekday|isotime|isodate|idle_duration|lastMessage|'
                      r'lastCharMessage|lastUserMessage|lastMessageId|currentSwipeId|char|group|charIfNotGroup|input)\b')
HTML_TAGS = {'details', 'summary', 'thinking', 'think', 'br', 'b', 'span', 'div'}
FALSE_WORDS = {'', 'off', 'false', '0'}


def budget_for(filename):
    """The token budget for a preset, by its filename: 3550 for Chibi Edition, BUDGET otherwise."""
    return 3550 if 'Chibi Edition' in filename else BUDGET


def take_macro(s, i):
    """Return the index just past the macro that opens at s[i] ('{{'), honouring nesting."""
    depth, j = 0, i
    while j < len(s):
        if s.startswith('{{', j):
            depth, j = depth + 1, j + 2
        elif s.startswith('}}', j):
            depth, j = depth - 1, j + 2
            if depth == 0:
                return j
        else:
            j += 1
    raise ValueError(f'unclosed macro near: {s[i:i + 60]!r}')


def split_if(s, i):
    """For an if-block whose body starts at s[i], return (then_text, else_text or None, end_index)."""
    depth, j, else_at = 1, i, None
    while j < len(s):
        if re.match(r'\{\{[#]?if[\s}]', s[j:]):
            depth += 1
        elif s.startswith('{{/if}}', j):
            depth -= 1
            if depth == 0:
                if else_at is None:
                    return s[i:j], None, j + len('{{/if}}')
                return s[i:else_at], s[else_at + len('{{else}}'):j], j + len('{{/if}}')
        elif s.startswith('{{else}}', j) and depth == 1 and else_at is None:
            else_at = j
        j += 1
    raise ValueError('unclosed {{if}}')


def render(s, state, rng):
    """Render the macros ARIA uses, the way SillyTavern's experimental macro engine does."""
    out, i = [], 0
    while i < len(s):
        if not s.startswith('{{', i):
            out.append(s[i])
            i += 1
            continue
        j = take_macro(s, i)
        m = s[i + 2:j - 2]
        if m.startswith('//'):
            pass
        elif m == 'trim':
            out.append('\x00TRIM\x00')
        elif m.startswith('setvar::'):
            name, _, value = m[len('setvar::'):].partition('::')
            state[name] = render(value, state, rng)
        elif m.startswith('addvar::'):
            name, _, value = m[len('addvar::'):].partition('::')
            value = render(value, state, rng)
            try:
                state[name] = str(int(state.get(name) or 0) + int(value))
            except ValueError:
                state[name] = (state.get(name) or '') + value
        elif m.startswith('getvar::'):
            out.append(state.get(m[len('getvar::'):], ''))
        elif m.startswith('.') and '=' in m:
            name, _, value = m[1:].partition('=')
            state[name.strip()] = value.strip()
        elif re.match(r'#?if\s', m):
            cond = m.split(None, 1)[1].strip()
            inverted = cond.startswith('!')
            name = cond.lstrip('!').strip().lstrip('.')
            then_text, else_text, end = split_if(s, j)
            truthy = state.get(name, '').strip().lower() not in FALSE_WORDS
            branch = then_text if truthy != inverted else (else_text or '')
            text = render(branch, state, rng)
            out.append(text if m.startswith('#') else text.strip())
            j = end
        elif m.startswith('roll::'):
            out.append(str(rng.randint(1, 20)))
        elif m.startswith('random::'):
            out.append(rng.choice(m[len('random::'):].split('::')))
        elif m == 'user':
            out.append('User')
        elif m == 'char':
            out.append('Char')
        else:
            out.append(s[i:j])
        i = j
    text = ''.join(out)
    # SillyTavern strips the newlines (only the newlines) on both sides of {{trim}}
    return re.sub(r'(?:\r?\n)*\x00TRIM\x00(?:\r?\n)*', '', text)


def strip_setvar_bodies(s):
    """Content with every setvar body and comment removed, to find volatile macros that would render in place."""
    out, i = [], 0
    while i < len(s):
        if s.startswith('{{setvar::', i) or s.startswith('{{//', i):
            i = take_macro(s, i)
            continue
        out.append(s[i])
        i += 1
    return ''.join(out)


READS = re.compile(r'\{\{getvar::([\w-]+)\}\}|\{\{#?if !?\.([\w-]+)\}\}')
NONEMPTY_SET = re.compile(r'\{\{setvar::([\w-]+)::(?!\}\})|\{\{\.([\w-]+)\s*=')


def order_errors(parts):
    """parts: [(label, raw_text)] in evaluation order. A variable must get a non-empty value in an earlier part,
    or earlier inside the same part, before a part reads it; blanking setvars ({{setvar::x::}}) do not count."""
    errors, have = [], set()
    for label, text in parts:
        events = sorted([(m.start(), 'set', m.group(1) or m.group(2)) for m in NONEMPTY_SET.finditer(text)]
                        + [(m.start(), 'read', m.group(1) or m.group(2)) for m in READS.finditer(text)])
        for _, kind, name in events:
            if kind == 'set':
                have.add(name)
            elif name not in have:
                errors.append(f'order: {label} reads {name} before anything earlier sets it')
                have.add(name)  # report each variable once
    return errors


def tokens(text):
    return round(len(text) / 4)


def wiring_errors(rendered, main_text, raw_all, label_owner='the Main Prompt'):
    """Dangling tags, dangling bold labels and unpaired variables across one rendered configuration."""
    errors = []
    text_all = '\n'.join(rendered.values())
    defined = {t for t in re.findall(r'<([A-Za-z_]+)>', text_all) if f'</{t}>' in text_all}
    for t in sorted(set(re.findall(r'<([A-Za-z_]+)>', text_all)) - defined - HTML_TAGS):
        errors.append(f'dangling tag reference <{t}>')
    labels = set(re.findall(r'\*\*([^*]+?):\*\*', main_text))
    for name, t in rendered.items():
        if t is main_text:
            continue
        for hit in re.finditer(r'\*\*([^*]+?):\*\*', t):
            line_start = t.rfind('\n', 0, hit.start()) + 1
            if re.fullmatch(r'[\s\-*#]*', t[line_start:hit.start()]):
                continue  # a label opening a line is a local heading
            if hit.group(1) not in labels:
                errors.append(f"{name} points at **{hit.group(1)}:**, which {label_owner} does not define")
    # Blanking setvars ({{setvar::x::}}) only clear a variable, so they do not count as a set that must be read.
    setters = {m.group(1) or m.group(2) for m in NONEMPTY_SET.finditer(raw_all)}
    readers = set(re.findall(r'\{\{getvar::([\w-]+)\}\}', raw_all)) | set(re.findall(r'\{\{#?if !?\.([\w-]+)\}\}', raw_all))
    for v in sorted(readers - setters):
        errors.append(f'variable read but never set: {v}')
    for v in sorted(setters - readers):
        errors.append(f'variable set but never read: {v}')
    return errors, setters


# ---------------------------------------------------------------- Chat Completions

def simulate_cc(preset, enabled, seed, state=None, impersonate=False):
    """Render one turn: relative entries top to bottom, then In-Chat entries. Returns ({id: text}, state)."""
    rng = random.Random(seed)
    state = dict(state or {})
    prompts = {p['identifier']: p for p in preset['prompts']}
    order = [row['identifier'] for row in preset['prompt_order'][1]['order']]
    rendered = {}
    for phase in (0, 1):
        for pid in order:
            p = prompts[pid]
            if pid not in enabled or p.get('marker') or (p.get('injection_position') or 0) != phase:
                continue
            trig = p.get('injection_trigger') or []
            if trig and ('impersonate' in trig) != impersonate:
                continue
            rendered[pid] = render(p.get('content') or '', state, rng)
    return rendered, state


def analyse_cc(preset, filename=''):
    prompts = {p['identifier']: p for p in preset['prompts']}
    order = preset['prompt_order'][1]['order']
    name = {pid: prompts[pid].get('name', pid) for pid in prompts}
    errors = []

    ids = [p['identifier'] for p in preset['prompts']]
    if len(ids) != len(set(ids)):
        errors.append('duplicate prompt identifiers')
    for row in order:
        if row['identifier'] not in prompts:
            errors.append(f"prompt_order names a missing prompt: {row['identifier']}")

    shipped = {row['identifier'] for row in order if row['enabled']}
    by_prefix = lambda *pre: {pid for pid in prompts if name[pid].startswith(pre)}
    patches = by_prefix('🩹')
    core = shipped - by_prefix('🎲', '⏰')
    lc_ids = {pid for pid in prompts if name[pid].startswith('🧠 The Logic Core')}
    # The jailbreak entries are imported from Realistic Frankenstein, replace the Logic Core, and carry its tags and helper
    # variables. Each gets its own path, and they stay out of the ARIA wiring checks.
    jb_ids = {pid for pid in prompts if 'Demons of Delusion' in name[pid]}
    plan_ids = lc_ids | jb_ids
    twin_ids = {pid for pid in prompts if 'twin' in name[pid]}
    skip_all_on = by_prefix('🌳', '🌿') | twin_ids | plan_ids
    skip_all_on |= {'enhanceDefinitions'} | patches
    no_patch = {row['identifier'] for row in order} - skip_all_on

    def path_total(plan, patch):
        """Render a real path: every module on, one plan (the Logic Core or one jailbreak), one patch."""
        enabled = no_patch | {plan} | ({patch} if patch else set())
        rendered, _ = simulate_cc(preset, enabled, seed=1)
        return sum(tokens(t) for t in rendered.values()), enabled

    def best_patch(plan):
        """The patch that costs most on this path, its own text plus the lines it hands the plan and the gate."""
        return max(patches, key=lambda pid: path_total(plan, pid)[0], default=None)

    # The system-role twin is a second copy of the Logic Core, so it does not need a path of its own.
    path_plans = sorted((lc_ids - twin_ids) | jb_ids, key=lambda pid: name[pid])
    lc_plan = min(lc_ids - twin_ids, key=lambda pid: name[pid], default=None)
    paths = {}
    for plan in path_plans:
        patch = best_patch(plan)
        total, enabled = path_total(plan, patch)
        label = 'Logic Core' if plan in lc_ids else name[plan]
        paths[label] = (total, enabled)
    table_patch = best_patch(lc_plan) if lc_plan else (best_patch(path_plans[0]) if path_plans else None)
    everything = no_patch | plan_ids | ({table_patch} if table_patch else set())

    totals = {}
    for label, enabled in (('core', core), ('shipped default', shipped)):
        rendered, _ = simulate_cc(preset, enabled, seed=1)
        totals[label] = sum(tokens(t) for t in rendered.values())
    rendered, _ = simulate_cc(preset, everything, seed=1)
    print('Per-entry tokens with every entry ON (alternatives included; not a runnable path):')
    for pid, text in rendered.items():
        print(f'  {tokens(text):5}  {name[pid]}')
    for label, (total, enabled) in paths.items():
        totals[f'fully kitted ({label})'] = total
    # SillyTavern also appends the preset's own impersonation_prompt setting on Impersonate turns
    imp_setting = tokens(render(preset.get('impersonation_prompt') or '', {}, random.Random(1)))
    for label, (total, enabled) in paths.items():
        imp, _ = simulate_cc(preset, enabled, seed=1, impersonate=True)
        normal, _ = simulate_cc(preset, enabled, seed=1)
        totals[f'Impersonate ({label})'] = sum(tokens(t) for t in imp.values()) - total + \
            sum(tokens(normal[pid]) for pid in normal if pid not in imp) + imp_setting
    budget = budget_for(filename)
    for label, (total, enabled) in paths.items():
        if total > budget:
            errors.append(f'fully kitted ({label}) is {total} tokens, over the {budget} budget')

    lc_patch = best_patch(lc_plan) if lc_plan else None
    lc_path = no_patch | ({lc_plan} if lc_plan else set()) | ({lc_patch} if lc_patch else set())
    rendered, _ = simulate_cc(preset, lc_path, seed=1)
    named = {name[pid]: t for pid, t in rendered.items()}
    main_text = named.get(name.get('main', ''), '')
    raw_all = '\n'.join(p.get('content') or '' for p in preset['prompts'] if p['identifier'] not in jb_ids)
    wiring, setters = wiring_errors(named, main_text, raw_all)
    errors += wiring
    # The same wiring check over every Logic Core shape: each 🏷️ tags entry on its own (the <thinking> one and the Gemini 4
    # Argon <thought> one) or none, normal and Impersonate, each model patch, the assistant Logic Core, its system-role twin,
    # or neither. With a tags entry on nothing may name <logic_core>: the plan opens on the fence tag, and a second tag there
    # is what models copied. The jailbreak entries stay out: their imported text names Realistic Frankenstein's tags and
    # helper variables, which ARIA does not define.
    tags_ids = by_prefix('🏷️')
    base = lc_path - patches - tags_ids - lc_ids
    seen = set(errors)
    for tags in sorted(tags_ids) + [None]:
        for imp in (False, True):
            for patch in sorted(patches) + [None]:
                for lc in sorted(lc_ids) + [None]:
                    enabled = base | ({patch} if patch else set()) | ({tags} if tags else set()) | ({lc} if lc else set())
                    r, _ = simulate_cc(preset, enabled, seed=1, impersonate=imp)
                    label = f"{name[tags] if tags else 'Tags OFF'}, {'Impersonate' if imp else 'normal'}, {name[lc] if lc else 'no Logic Core'}, {name[patch] if patch else 'no patch'}"
                    nm = {name[pid]: t for pid, t in r.items()}
                    found, _ = wiring_errors(nm, nm.get(name.get('main', ''), ''), raw_all)
                    if tags:
                        if re.search(r'</?logic_core', '\n'.join(r.values())):
                            found.append('Tags ON render names <logic_core>')
                    for e in found:
                        if e not in seen:
                            seen.add(e)
                            errors.append(f'{e} ({label})')
    errors += order_errors([(name[r['identifier']], prompts[r['identifier']].get('content') or '') for r in order
                            if r['identifier'] in prompts and r['identifier'] not in jb_ids])
    blanked = set(re.findall(r'\{\{setvar::([\w-]+)::\}\}', prompts['main']['content']))
    for v in sorted(v for v in setters if v.startswith('aria') and v not in blanked):
        errors.append(f'splice variable not blanked by the Main Prompt: {v}')

    stale = {v: 'stale value from an earlier turn' for v in setters}
    a, _ = simulate_cc(preset, lc_path, seed=1)
    b, _ = simulate_cc(preset, lc_path, seed=99, state=stale)
    for pid in a:
        p = prompts[pid]
        relative = (p.get('injection_position') or 0) == 0
        if relative and a[pid] != b.get(pid):
            errors.append(f'cache: {name[pid]} renders differently between turns')
        if relative and VOLATILE.search(strip_setvar_bodies(p.get('content') or '')):
            errors.append(f'cache: {name[pid]} contains a per-turn macro in the system block')
        if relative and p.get('injection_trigger'):
            errors.append(f'cache: {name[pid]} has generation triggers, so the system block changes on some turns')

    def stale_changes_system_block(enabled, state):
        """The relative entries whose text changes when an earlier turn left `state` behind."""
        fresh, _ = simulate_cc(preset, enabled, seed=1)
        after, _ = simulate_cc(preset, enabled, seed=99, state=state)
        return [pid for pid in fresh if (prompts[pid].get('injection_position') or 0) == 0 and fresh[pid] != after.get(pid)]

    # The same stale-state test for every patch on its own over the shared base, and for the base with no patch. Everything ON
    # holds only one patch, so a variable that one patch sets, another patch prints and the Main Prompt does not blank (the Gemini
    # 3.8 Flash text that Gemini All-In-One printed after the 3.8 patch was switched off) stays invisible there.
    for patch in [pid for pid in ids if pid in patches] + [None]:
        enabled = no_patch | ({patch} if patch else set())
        if stale_changes_system_block(enabled, stale):
            leaks = [v for v in sorted(setters) if stale_changes_system_block(enabled, {v: stale[v]})]
            errors.append(f"cache: with {name[patch] if patch else 'no patch'} on over the shared base, a stale "
                          f"{', '.join(leaks) or 'variable'} from an earlier turn prints in the system block; "
                          f"the Main Prompt must blank it")
    for row in order:
        p = prompts[row['identifier']]
        if p.get('injection_position') == 1 and (p.get('injection_depth') or 0) != 0:
            errors.append(f"cache: {name[row['identifier']]} is In-Chat at depth {p['injection_depth']}; keep it at 0")
    return totals, errors


# ---------------------------------------------------------------- Text Completions

SWITCH = re.compile(r'\{\{\.(aria-[\w-]+) = (on|off)\}\}')


def simulate_tc(preset, overrides, seed, state=None):
    """Render the system prompt, then the post-history block, with switch overrides applied."""
    rng = random.Random(seed)
    state = dict(state or {})
    system = SWITCH.sub(lambda m: '{{.%s = %s}}' % (m.group(1), overrides.get(m.group(1), m.group(2))),
                        preset['sysprompt']['content'])
    rendered_system = render(system, state, rng)
    rendered_post = render(preset['sysprompt'].get('post_history') or '', state, rng)
    return {'System Prompt': rendered_system, 'Post-History': rendered_post}, state


def analyse_tc(preset, filename=''):
    errors = []
    system = preset['sysprompt']['content']
    shipped = dict(SWITCH.findall(system))
    if not shipped:
        errors.append('no aria-* switches found in the System Prompt')
    patches = [s for s in shipped if s.startswith('aria-patch')]
    # The shared base: every switch that is not a patch ON, every patch OFF. Patches are ranked over it, the way analyse_cc
    # does, because a patch hands the plan and the gate lines that print only while the Logic Core, Bonds, Fate or the
    # Flash Gate are on, and with everything else off the ranking picked a patch that is not the real maximum.
    plans = [s for s in ('aria-logic-core', 'aria-micro') if s in shipped]
    base = {s: 'on' for s in shipped if not s.startswith('aria-patch') and s not in plans} | {p: 'off' for p in patches}

    def patch_cost(p, path_base):
        """A patch's whole cost over a path, its own text plus any line it hands the plan and the gate."""
        r_on, _ = simulate_tc(preset, path_base | {p: 'on'}, 1)
        r_off, _ = simulate_tc(preset, path_base, 1)
        return sum(tokens(t) for t in r_on.values()) - sum(tokens(t) for t in r_off.values())

    # The Logic Core and the Micro jailbreak are alternatives, so each gets its own fully kitted path.
    path_bases = {}
    if 'aria-logic-core' in plans:
        path_bases['Logic Core'] = base | {'aria-logic-core': 'on', 'aria-micro': 'off'}
    if 'aria-micro' in plans:
        path_bases['Micro jailbreak'] = base | {'aria-logic-core': 'off', 'aria-micro': 'on'}
    path_bases['no plan'] = base | {'aria-logic-core': 'off', 'aria-micro': 'off'}
    paths = {}
    for label, path_base in path_bases.items():
        largest = max(patches, key=lambda p: patch_cost(p, path_base), default=None)
        paths[label] = path_base | ({largest: 'on'} if largest else set())
    roomy = dict(shipped) | {'aria-logic-core': 'on', 'aria-fate': 'on', 'aria-time-place': 'on'}

    totals = {}
    for label, overrides in (('shipped (lean, 32k)', shipped), ('+ Logic Core, Fate, Time', roomy)):
        rendered, _ = simulate_tc(preset, overrides, seed=1)
        totals[label] = sum(tokens(t) for t in rendered.values())
    raw_base = base | {s: 'on' for s in plans}
    raw_patch = max(patches, key=lambda p: patch_cost(p, raw_base), default=None)
    print('Tokens with every switch ON (alternatives included; not a runnable path):')
    rendered, _ = simulate_tc(preset, raw_base | ({raw_patch: 'on'} if raw_patch else set()), seed=1)
    for part, text in rendered.items():
        print(f'  {tokens(text):5}  {part}')
    for label, overrides in paths.items():
        rendered, _ = simulate_tc(preset, overrides, seed=1)
        totals[f'fully kitted ({label})'] = sum(tokens(t) for t in rendered.values())
    budget = budget_for(filename)
    for label, total in totals.items():
        if label.startswith('fully kitted (') and total > budget:
            errors.append(f'{label} is {total} tokens, over the {budget} budget')

    lc_overrides = paths.get('Logic Core') or paths.get('no plan')
    rendered, _ = simulate_tc(preset, lc_overrides, seed=1)
    raw_all = system + '\n' + (preset['sysprompt'].get('post_history') or '')
    wiring, setters = wiring_errors(rendered, rendered['System Prompt'], raw_all, 'the System Prompt')
    errors += wiring
    # Every Logic Core shape: tags on and off, Logic Core on and off, with each patch alone; with tags on nothing may
    # name <logic_core>
    seen = set(errors)
    for tags in ('on', 'off'):
      for lc in ('on', 'off'):
        for patch in patches + [None]:
            overrides = dict(lc_overrides) | {p: 'off' for p in patches} | {
                'aria-thinking-tags': tags, 'aria-logic-core': lc, 'aria-micro': 'off'}
            if patch:
                overrides[patch] = 'on'
            r, _ = simulate_tc(preset, overrides, seed=1)
            found, _ = wiring_errors(r, r['System Prompt'], raw_all, 'the System Prompt')
            if tags == 'on' and re.search(r'</?logic_core', r['System Prompt'] + r['Post-History']):
                found.append('tags-on render names <logic_core>')
            for e in found:
                if e not in seen:
                    seen.add(e)
                    errors.append(f"{e} (aria-thinking-tags {tags}, aria-logic-core {lc}, {patch or 'no patch'})")
    errors += order_errors([('the System Prompt', system), ('the post-history', preset['sysprompt'].get('post_history') or '')])

    stale = {v: 'stale value from an earlier turn' for v in setters}
    for overrides in (shipped, lc_overrides):
        a, _ = simulate_tc(preset, overrides, seed=1)
        b, _ = simulate_tc(preset, overrides, seed=99, state=stale)
        if a['System Prompt'] != b['System Prompt']:
            errors.append('cache: the System Prompt renders differently between turns')
            break

    def stale_changes_system(overrides, state):
        """Whether the System Prompt changes when an earlier turn left `state` behind."""
        a, _ = simulate_tc(preset, overrides, seed=1)
        b, _ = simulate_tc(preset, overrides, seed=99, state=state)
        return a['System Prompt'] != b['System Prompt']

    # The same stale-state test for every patch on its own over the base, and for the base with no patch: a variable that
    # a patch sets and the Main Prompt's first line does not blank prints whatever it last held, once that patch is OFF
    for patch in patches + [None]:
        overrides = base | ({patch: 'on'} if patch else {})
        if stale_changes_system(overrides, stale):
            leaks = [v for v in sorted(setters) if stale_changes_system(overrides, {v: stale[v]})]
            errors.append(f"cache: with {patch or 'no patch'} on over the base, a stale {', '.join(leaks) or 'variable'} "
                          f"from an earlier turn prints in the System Prompt; the Main Prompt must blank it")
    if VOLATILE.search(strip_setvar_bodies(system)):
        errors.append('cache: the System Prompt contains a per-turn macro')
    story = preset.get('context', {}).get('story_string', '')
    if story and story.find('wiBefore') < story.find('mesExamples'):
        errors.append('cache: World Info comes before the static card fields in the story string')
    return totals, errors


def main():
    paths = [Path(p) for p in sys.argv[1:]] or DEFAULT_PRESETS
    failed = False
    for path in paths:
        preset = json.loads(path.read_text(encoding='utf-8'))
        kind = 'Text Completions' if 'sysprompt' in preset else 'Chat Completions'
        print(f'=== {path.name} ({kind})')
        totals, errors = (analyse_tc if 'sysprompt' in preset else analyse_cc)(preset, path.name)
        print('Totals:')
        for label, value in totals.items():
            print(f'  {label:26} {value:5}')
        if errors:
            failed = True
            print('FAILED:')
            for e in errors:
                print('  -', e)
        else:
            print('OK: budget, wiring and cache checks all pass.')
        print()
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
