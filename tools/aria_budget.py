#!/usr/bin/env python3
"""ARIA budget and cache checker.

Simulates SillyTavern turns for ARIA's Chat Completions and Text Completions
presets, counts the rendered tokens (characters / 4, comments stripped) for a
few configurations, and fails when something would break the budget, the
wiring or prompt caching.

Usage: python3 tools/aria_budget.py [preset.json ...]   (no arguments: both ARIA presets)
"""
import json
import random
import re
import sys
from pathlib import Path

BUDGET = 4500
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PRESETS = [
    ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json",
    ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",
]
VOLATILE = re.compile(r'\{\{(roll|random|pick|time|date|weekday|isotime|isodate|idle_duration|lastMessage|'
                      r'lastCharMessage|lastUserMessage|lastMessageId|currentSwipeId|char|group|charIfNotGroup|input)\b')
HTML_TAGS = {'details', 'summary', 'thinking', 'think', 'br', 'b', 'span', 'div'}
FALSE_WORDS = {'', 'off', 'false', '0'}


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
    setters = set(re.findall(r'\{\{setvar::([\w-]+)::', raw_all)) | set(re.findall(r'\{\{\.([\w-]+)\s*=', raw_all))
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


def analyse_cc(preset):
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
    skip_all_on = by_prefix('🌳', '🌿') | {pid for pid in prompts if 'twin' in name[pid] or name[pid] == 'Reduce Reasoning'}
    skip_all_on |= {'enhanceDefinitions'} | patches
    largest_patch = max(patches, key=lambda pid: tokens(render(prompts[pid]['content'], {}, random.Random(0))), default=None)
    all_on = {row['identifier'] for row in order} - skip_all_on | ({largest_patch} if largest_patch else set())

    totals = {}
    for label, enabled in (('core', core), ('shipped default', shipped), ('everything ON', all_on)):
        rendered, _ = simulate_cc(preset, enabled, seed=1)
        totals[label] = sum(tokens(t) for t in rendered.values())
        if label == 'everything ON':
            print('Per-entry tokens with everything ON:')
            for pid, text in rendered.items():
                print(f'  {tokens(text):5}  {name[pid]}')
    imp, _ = simulate_cc(preset, all_on, seed=1, impersonate=True)
    normal, _ = simulate_cc(preset, all_on, seed=1)
    # SillyTavern also appends the preset's own impersonation_prompt setting on Impersonate turns
    imp_setting = tokens(render(preset.get('impersonation_prompt') or '', {}, random.Random(1)))
    totals['Impersonate adds'] = sum(tokens(t) for t in imp.values()) - totals['everything ON'] + \
        sum(tokens(normal[pid]) for pid in normal if pid not in imp) + imp_setting
    if totals['everything ON'] > BUDGET:
        errors.append(f"everything ON is {totals['everything ON']} tokens, over the {BUDGET} budget")

    rendered, _ = simulate_cc(preset, all_on, seed=1)
    named = {name[pid]: t for pid, t in rendered.items()}
    main_text = named.get(name.get('main', ''), '')
    raw_all = '\n'.join(p.get('content') or '' for p in preset['prompts'])
    wiring, setters = wiring_errors(named, main_text, raw_all)
    errors += wiring
    # The same wiring check over every Logic Core shape: Tags ON and OFF, normal and Impersonate, each model patch,
    # the assistant Logic Core, its system-role twin, or neither. With Tags ON nothing may name <logic_core>: the plan opens on
    # the fence tag, and a second tag there is what models copied.
    tags_ids = by_prefix('🏷️')
    lc_ids = {pid for pid in prompts if name[pid].startswith('🧠 The Logic Core')}
    base = all_on - patches - tags_ids - lc_ids
    seen = set(errors)
    for tags_on in (True, False):
        for imp in (False, True):
            for patch in sorted(patches) + [None]:
                for lc in sorted(lc_ids) + [None]:
                    enabled = base | ({patch} if patch else set()) | (tags_ids if tags_on else set()) | ({lc} if lc else set())
                    r, _ = simulate_cc(preset, enabled, seed=1, impersonate=imp)
                    label = f"Tags {'ON' if tags_on else 'OFF'}, {'Impersonate' if imp else 'normal'}, {name[lc] if lc else 'no Logic Core'}, {name[patch] if patch else 'no patch'}"
                    nm = {name[pid]: t for pid, t in r.items()}
                    found, _ = wiring_errors(nm, nm.get(name.get('main', ''), ''), raw_all)
                    if tags_on:
                        if re.search(r'</?logic_core', '\n'.join(r.values())):
                            found.append('Tags ON render names <logic_core>')
                    for e in found:
                        if e not in seen:
                            seen.add(e)
                            errors.append(f'{e} ({label})')
    errors += order_errors([(name[r['identifier']], prompts[r['identifier']].get('content') or '') for r in order
                            if r['identifier'] in prompts])
    blanked = set(re.findall(r'\{\{setvar::([\w-]+)::\}\}', prompts['main']['content']))
    for v in sorted(v for v in setters if v.startswith('aria') and v not in blanked):
        errors.append(f'splice variable not blanked by the Main Prompt: {v}')

    stale = {v: 'stale value from an earlier turn' for v in setters}
    a, _ = simulate_cc(preset, all_on, seed=1)
    b, _ = simulate_cc(preset, all_on, seed=99, state=stale)
    for pid in a:
        p = prompts[pid]
        relative = (p.get('injection_position') or 0) == 0
        if relative and a[pid] != b.get(pid):
            errors.append(f'cache: {name[pid]} renders differently between turns')
        if relative and VOLATILE.search(strip_setvar_bodies(p.get('content') or '')):
            errors.append(f'cache: {name[pid]} contains a per-turn macro in the system block')
        if relative and p.get('injection_trigger'):
            errors.append(f'cache: {name[pid]} has generation triggers, so the system block changes on some turns')
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


def analyse_tc(preset):
    errors = []
    system = preset['sysprompt']['content']
    shipped = dict(SWITCH.findall(system))
    if not shipped:
        errors.append('no aria-* switches found in the System Prompt')
    patches = [s for s in shipped if s.startswith('aria-patch')]

    def patch_cost(p):
        on = {s: 'off' for s in shipped} | {p: 'on'}
        off = {s: 'off' for s in shipped}
        r_on, _ = simulate_tc(preset, on, 1)
        r_off, _ = simulate_tc(preset, off, 1)
        return tokens(r_on['System Prompt']) - tokens(r_off['System Prompt'])

    largest = max(patches, key=patch_cost, default=None)
    all_on = {s: 'on' for s in shipped if not s.startswith('aria-patch')} | {p: ('on' if p == largest else 'off') for p in patches}
    roomy = dict(shipped) | {'aria-logic-core': 'on', 'aria-fate': 'on', 'aria-time-place': 'on'}

    totals = {}
    for label, overrides in (('shipped (lean, 32k)', shipped), ('+ Logic Core, Fate, Time', roomy), ('everything ON', all_on)):
        rendered, _ = simulate_tc(preset, overrides, seed=1)
        totals[label] = sum(tokens(t) for t in rendered.values())
        if label == 'everything ON':
            print('Tokens with everything ON:')
            for part, text in rendered.items():
                print(f'  {tokens(text):5}  {part}')
    if totals['everything ON'] > BUDGET:
        errors.append(f"everything ON is {totals['everything ON']} tokens, over the {BUDGET} budget")

    rendered, _ = simulate_tc(preset, all_on, seed=1)
    raw_all = system + '\n' + (preset['sysprompt'].get('post_history') or '')
    wiring, setters = wiring_errors(rendered, rendered['System Prompt'], raw_all, 'the System Prompt')
    errors += wiring
    # Every Logic Core shape: tags on and off, Logic Core on and off, with each patch alone; with tags on nothing may
    # name <logic_core>
    seen = set(errors)
    for tags in ('on', 'off'):
      for lc in ('on', 'off'):
        for patch in patches + [None]:
            overrides = dict(all_on) | {p: 'off' for p in patches} | {'aria-thinking-tags': tags, 'aria-logic-core': lc}
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
    for overrides in (shipped, all_on):
        a, _ = simulate_tc(preset, overrides, seed=1)
        b, _ = simulate_tc(preset, overrides, seed=99, state=stale)
        if a['System Prompt'] != b['System Prompt']:
            errors.append('cache: the System Prompt renders differently between turns')
            break
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
        totals, errors = (analyse_tc if 'sysprompt' in preset else analyse_cc)(preset)
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
