#!/usr/bin/env python3
"""ARIA Marinara parity checker.

Renders a Chat Completions preset and its Marinara Engine Edition twin with the same settings, then compares what the
model would read, line by line. The Chat Completions file is the reference: every toggle it offers should exist in the
Marinara file as a choice-block option, and the rendered prompt should match once the formatting differences the two
hosts force are set aside (the CC variable resets, Marinara's agent protocol, dice values and blank lines).

What it checks:
  1. Toggle coverage: every CC entry a user can switch maps to a Marinara choice option (TOGGLE_MAP below), and every
     section a choice gates is enabled in the Marinara file, so picking the option actually sends it.
  2. Defaults: the toggles CC ships ON are the options Marinara's defaultChoices pick.
  3. Rendered parity: for a matrix of settings (defaults, every model patch, the Flash Gate, Character Hold, the
     hardener, adult modes, tags and Reduce Reasoning, the system-role twin), the rendered system block and the
     post-history block match.

Usage: python3 tools/marinara_parity.py [--show N]        (the two Base pairs: full and Chibi)
       python3 tools/marinara_parity.py CC.json MARINARA.json [--show N]
--show N prints up to N differing lines per configuration (default 6); --random N adds N random settings (one plan,
one patch, a tags entry, a Reduce entry and random add-ons); --assume-enabled renders the choice-gated
sections as if they were switched on, to compare the text apart from the switches.

The Marinara renderer follows Marinara Engine's macro engine (packages/shared/src/utils/macro-engine.ts): {{trim}} is
removed, not newline-eating, each section's output is trimmed as a whole, `contains` is a case-insensitive substring
test, and `==` compares case-insensitively. It covers the macros ARIA's Marinara files use and nothing more.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aria_budget as ab  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# CC entry name prefix -> (Marinara choice variable, option value). Multi-select choices list the value when it is on.
TOGGLE_MAP = [
    ('🔞 Adult Context', 'adult_mode', 'ADULT'),
    ('😈 Freaky Override', 'adult_mode', 'FREAKY'),
    ('👀 Hybrid POV', 'pov_style', 'HYBRID'),
    ('🎬 Voice & Scene Engine', 'core_modules', 'SCENE'),
    ('🎭 NPC Voice & Emotions', 'core_modules', 'NPCVOICE'),
    ('🖋️ Anti-Slop Codex', 'core_modules', 'ANTISLOP'),
    ('👃 Scent Occasions', 'core_modules', 'SCENT'),
    ('🐺 Anthro Vocals', 'core_modules', 'ANTHRO'),
    ('🔦 Flash Gate', 'core_modules', 'FLASH'),
    ('🧷 Character Hold', 'core_modules', 'HOLD'),
    ('🧪 Auto-Routing Quality Hardener', 'core_modules', 'HARDENER'),
    ('⏰ Time & Place', 'world_engine', 'TIME'),
    ('🎲 Fate & Chekhov Ledger', 'world_engine', 'FATE'),
    ('🥰 Bonds Lite', 'world_engine', 'BONDS'),
    ('🩹 Model Patch: Claude 5', 'model_patch', 'CLAUDE'),
    ('🩹 Model Patch: Gemini All-In-One', 'model_patch', 'GEMINI'),
    ('🩹 Model Patch: Gemini 3.8 Flash', 'model_patch', 'GEMINI38'),
    ('🩹 Model Patch: GLM 5.4', 'model_patch', 'GLM54'),
    ('🩹 Model Patch: GLM', 'model_patch', 'GLM'),
    ('🩹 Model Patch: Kimi / Qwen', 'model_patch', 'KIMIQWEN'),
    ('🩹 Model Patch: MiMo V2.6 Pro', 'model_patch', 'MIMOPRO'),
    ('🩹 Model Patch: MiMo V2.6 Flash', 'model_patch', 'MIMOFLASH'),
    ('🩹 Model Patch: DeepSeek', 'model_patch', 'DEEPSEEK'),
    ('🧠 The Logic Core (system-role twin)', 'logic_core', 'SYSTEM'),
    ('🧠 The Logic Core', 'logic_core', 'ASSISTANT'),
    ('👹 Demons of Delusion Jailbreak', 'logic_core', 'JAILBREAK'),
    ('👹 Demons of Delusion Small Jailbreak', 'logic_core', 'JAILBREAK_SMALL'),
    ('👹 Demons of Delusion Small Gemini Jailbreak', 'logic_core', 'JAILBREAK_GEMINI'),
    ('👹 Demons of Delusion Small Claude Jailbreak', 'logic_core', 'JAILBREAK_CLAUDE'),
    ('🏷️ Logic Core Tags', 'logic_options', 'THINKTAGS'),
    ('🏷️ Gemini 4 Argon Thinking Tags Enforcer', 'logic_options', 'THOUGHTTAGS'),
    ('Reduce Reasoning (Gemini 4 HNC)', 'logic_options', 'LEASH'),
    ('Reduce Reasoning', 'logic_options', 'REDUCE'),
]
# CC entries that are notes for the user, markers, or host plumbing, with no Marinara choice of their own.
NO_CHOICE = ('🌳', '🌿', '🍃', '⚡', '📖', '🪞', '🚪', 'Post-History Instructions', 'Enhance Definitions')
MULTI = {'core_modules', 'world_engine', 'logic_options'}


def cc_toggle(name):
    """The choice for one CC entry: the longest TOGGLE_MAP prefix that matches the whole name or a name followed by a
    space or a parenthesis, so 'Reduce Reasoning' never claims 'Reduce Reasoning (Gemini 4 HNC)'."""
    best = None
    for prefix, var, value in TOGGLE_MAP:
        if name == prefix or name.startswith(prefix + ' ') or name.startswith(prefix + ' (') or \
                (name.startswith(prefix) and not name[len(prefix):].strip(' ✨')):
            if best is None or len(prefix) > len(best[0]):
                best = (prefix, var, value)
    return best[1:] if best else None


# ---------------------------------------------------------------- Marinara macro rendering

def _split_top(cond, op):
    """Split a condition on a boolean operator that sits outside parentheses and quotes."""
    parts, depth, quote, start, i = [], 0, None, 0, 0
    while i < len(cond):
        ch = cond[i]
        if quote:
            quote = None if ch == quote else quote
        elif ch in '"\'':
            quote = ch
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        elif depth == 0 and cond.startswith(op, i):
            parts.append(cond[start:i])
            i += len(op)
            start = i
            continue
        i += 1
    parts.append(cond[start:])
    return parts


def eval_cond(cond, env):
    cond = cond.strip()
    ors = _split_top(cond, '||')
    if len(ors) > 1:
        return any(eval_cond(c, env) for c in ors)
    ands = _split_top(cond, '&&')
    if len(ands) > 1:
        return all(eval_cond(c, env) for c in ands)
    if cond.startswith('(') and cond.endswith(')'):
        return eval_cond(cond[1:-1], env)
    m = re.fullmatch(r'([\w.{}:-]+)\s*(==|!=|not contains|contains)\s*"([^"]*)"', cond)
    if m:
        left = env_value(m.group(1), env).strip().lower()
        right = m.group(3).strip().lower()
        return {'==': left == right, '!=': left != right,
                'contains': right in left, 'not contains': right not in left}[m.group(2)]
    if cond.startswith('!'):
        return not eval_cond(cond[1:], env)
    value = env_value(cond, env)
    return bool(value.strip()) and not re.fullmatch(r'(false|0|no|off|null|undefined)', value.strip(), re.I)


def env_value(name, env):
    name = name.strip()
    if name.startswith('{{') and name.endswith('}}'):
        name = name[2:-2]
    value = env.get(name, '')
    if isinstance(value, list):
        return ', '.join(value)
    return str(value)


def _branches(s, j):
    """For an #if whose body starts at s[j], return ([(cond_or_None, text)], end_index)."""
    depth, i, cuts = 1, j, []
    while i < len(s):
        if re.match(r'\{\{#if\s', s[i:]):
            depth += 1
        elif s.startswith('{{/if}}', i):
            depth -= 1
            if depth == 0:
                cuts.append((None, i))
                break
        elif depth == 1 and (m := re.match(r'\{\{else(?: if ([^}]*))?\}\}', s[i:])):
            cuts.append((m.group(1), i, i + m.end()))
            i += m.end()
            continue
        i += 1
    else:
        raise ValueError('unclosed {{#if}}')
    out, start, cond = [], j, 'FIRST'
    for cut in cuts:
        out.append((cond, s[start:cut[1]]))
        if len(cut) == 3:
            cond, start = (cut[0] if cut[0] is not None else 'ELSE'), cut[2]
    return out, cuts[-1][1] + len('{{/if}}')


def render_marinara(s, env, roll='7'):
    out, i = [], 0
    while i < len(s):
        if not s.startswith('{{', i):
            out.append(s[i])
            i += 1
            continue
        j = ab.take_macro(s, i)
        m = s[i + 2:j - 2]
        if m.startswith('//') or m == 'trim':
            pass
        elif m.startswith('#if '):
            branches, end = _branches(s, j)
            first_cond = m[4:]
            for cond, text in branches:
                c = first_cond if cond == 'FIRST' else cond
                if c == 'ELSE' or eval_cond(c, env):
                    out.append(render_marinara(text, env, roll))
                    break
            j = end
        elif m.startswith('setvar::'):
            name, _, value = m[len('setvar::'):].partition('::')
            env[name] = render_marinara(value, env, roll)
        elif m.startswith('addvar::'):
            name, _, value = m[len('addvar::'):].partition('::')
            value = render_marinara(value, env, roll)
            cur = str(env.get(name, ''))
            try:
                env[name] = str(int(cur) + int(value)) if cur.strip() and value.strip() else cur + value
            except ValueError:
                env[name] = cur + value
        elif m.startswith('getvar::'):
            out.append(str(env.get(m[len('getvar::'):], '')))
        elif m.startswith('roll:'):
            out.append(roll)
        elif m == 'user':
            out.append('User')
        elif m == 'char':
            out.append('Char')
        elif m == 'newline':
            out.append('\n')
        else:
            out.append(s[i:j])
        i = j
    return ''.join(out)


def choice_gated(section):
    """True when a section's whole content sits behind a choice-block condition (so the choice alone decides)."""
    return bool(re.match(r'\{\{#if (\w+) (==|!=|contains) "', section['content'] or '')) and \
        not (section['content'] or '').startswith('{{#if state_mode')


def simulate_marinara(mar, choices, assume_enabled=False):
    """Render one normal (not Impersonate) turn: ordered sections, then depth sections, as Marinara assembles them.
    assume_enabled renders the choice-gated sections as if they were switched on, to compare content apart from the
    switches."""
    env = {k: v for k, v in choices.items()}
    env['lastGenerationType'] = 'normal'
    sections = {s['id']: s for s in mar['sections']}
    order = json.loads(mar['preset']['sectionOrder'])
    rendered = {}
    for phase in ('ordered', 'depth'):
        for sid in order:
            s = sections[sid]
            on = s['enabled'] in (True, 'true') or (assume_enabled and choice_gated(s))
            if not on or s['isMarker'] in (True, 'true'):
                continue
            if (s['injectionPosition'] or 'ordered') != phase:
                continue
            rendered[s['name']] = render_marinara(s['content'] or '', env).strip()
    return rendered


# ---------------------------------------------------------------- comparison

def normalise(text):
    text = re.sub(r'\{\{roll:[^}]*\}\}|\b\d{1,2}\b(?= \|| *$)', 'N', text, flags=re.M)
    lines = [re.sub(r'\s+', ' ', ln).strip() for ln in text.split('\n')]
    return [ln for ln in lines if ln]


def fixed_dice(cc):
    """A copy of a CC preset whose {{roll::...}} macros all read 7, the value the Marinara renderer uses."""
    cc = json.loads(json.dumps(cc))
    for p in cc['prompts']:
        if p.get('content'):
            p['content'] = re.sub(r'\{\{roll::[^}]*\}\}', '7', p['content'])
    return cc


def cc_blocks(cc, enabled, seed=1):
    rendered, _ = ab.simulate_cc(fixed_dice(cc), enabled, seed)
    prompts = {p['identifier']: p for p in cc['prompts']}
    sysb, post = [], []
    for pid, text in rendered.items():
        (post if (prompts[pid].get('injection_position') or 0) == 1 else sysb).append(text)
    return sysb, post


def mar_blocks(mar, choices, assume_enabled=False):
    rendered = simulate_marinara(mar, choices, assume_enabled)
    sections = {s['name']: s for s in mar['sections']}
    sysb, post = [], []
    for name, text in rendered.items():
        (post if sections[name]['injectionPosition'] == 'depth' else sysb).append(text)
    return sysb, post


HOST_ONLY = [  # rendered lines that exist on one host by design
    re.compile(r'^<agent_context_protocol>|^</agent_context_protocol>'),
    re.compile(r'^Fate dice: A N \| B N \| C N$'),
]


def strip_host_only(lines):
    return [ln for ln in lines if not any(p.search(ln) for p in HOST_ONLY)]


def cc_config(cc, overrides):
    """CC enabled ids: the shipped toggles, with overrides {entry name prefix: bool}; an exact name wins over a
    prefix, so '🧠 The Logic Core' never switches its system-role twin."""
    prompts = {p['identifier']: p for p in cc['prompts']}
    enabled = {r['identifier'] for r in cc['prompt_order'][1]['order'] if r['enabled']}
    for prefix, on in overrides.items():
        exact = [pid for pid, p in prompts.items() if (p.get('name') or '') == prefix]
        hits = exact or [pid for pid, p in prompts.items() if (p.get('name') or '').startswith(prefix)][:1]
        for pid in hits:
            (enabled.add if on else enabled.discard)(pid)
    return enabled


def choices_for(cc, enabled):
    """The Marinara choices that mirror a set of enabled CC entries."""
    prompts = {p['identifier']: p for p in cc['prompts']}
    ch = {'adult_mode': 'NONE', 'pov_style': 'NONE', 'core_modules': [], 'world_engine': [], 'model_patch': 'NONE',
          'logic_core': 'NONE', 'logic_options': [], 'state_mode': 'NONE'}
    picks = [cc_toggle(prompts[pid].get('name') or '') for pid in enabled]
    for var, value in filter(None, picks):
        if var in MULTI:
            if value not in ch[var]:
                ch[var].append(value)
        elif var == 'adult_mode':
            ch[var] = 'FREAKY' if 'FREAKY' in (value, ch[var]) else value
        elif var == 'model_patch':
            # Gemini 3.8 Flash runs together with Gemini All-In-One in CC; Marinara's GEMINI38 option holds both
            ch[var] = 'GEMINI38' if 'GEMINI38' in (value, ch[var]) else value
        elif var == 'logic_core':
            # a jailbreak replaces The Logic Core, so with both on the jailbreak is the plan that runs
            if ch[var] == 'NONE' or value.startswith('JAILBREAK'):
                ch[var] = value
        else:
            ch[var] = value
    return ch


MATRIX = [
    ('shipped defaults', {}),
    ('adult', {'🔞': True}),
    ('adult + freaky', {'🔞': True, '😈': True}),
    ('anthro', {'🐺': True}),
    ('no POV', {'👀': False}),
    ('Flash Gate', {'🔦': True}),
    ('Character Hold', {'🧷': True}),
    ('hardener', {'🧪': True}),
    ('tags', {'🏷️ Logic Core Tags': True}),
    ('Argon tags', {'🏷️ Gemini 4 Argon': True}),
    ('reduce', {'Reduce Reasoning': True}),
    ('tags + reduce', {'🏷️ Logic Core Tags': True, 'Reduce Reasoning': True}),
    ('leash', {'Reduce Reasoning (Gemini 4 HNC)': True}),
    ('system-role twin', {'🧠 The Logic Core (system-role twin)': True, '🧠 The Logic Core': False}),
    ('Fate only', {'🥰': False}),
    ('Bonds only', {'🎲': False}),
    ('no Fate, Bonds, Time', {'🎲': False, '🥰': False, '⏰': False}),
]
PATCHES = ['🩹 Model Patch: Claude 5', '🩹 Model Patch: Gemini All-In-One', '🩹 Model Patch: GLM 5.4',
           '🩹 Model Patch: GLM', '🩹 Model Patch: Kimi / Qwen', '🩹 Model Patch: MiMo V2.6 Pro',
           '🩹 Model Patch: MiMo V2.6 Flash', '🩹 Model Patch: DeepSeek']


def random_matrix(cc, n, seed=20261125):
    """n random settings: one plan (or none), one patch (or none), a tags entry, a Reduce entry, and random add-ons."""
    import random
    rng = random.Random(seed)
    names = sorted({(x.get('name') or '') for x in cc['prompts']})
    plans = ['🧠 The Logic Core', '🧠 The Logic Core (system-role twin)', None] + [n for n in names if 'Demons of Delusion' in n]
    patches = [None] + [p for p in PATCHES if p in names] + ['GEMINI38']
    tags = [None, '🏷️ Logic Core Tags', '🏷️ Gemini 4 Argon']
    reduces = [None, 'Reduce Reasoning', 'Reduce Reasoning (Gemini 4 HNC)']
    addons = ['🔞', '😈', '🐺', '🔦', '🧷', '🧪']
    shipped = ['👀', '🎬', '🎭', '🖋️', '👃', '⏰', '🎲', '🥰']
    out = []
    for k in range(n):
        o = {'🧠 The Logic Core': False}
        plan, patch, tag, red = rng.choice(plans), rng.choice(patches), rng.choice(tags), rng.choice(reduces)
        if plan:
            o[plan] = True
        if patch == 'GEMINI38':
            o['🩹 Model Patch: Gemini 3.8 Flash'] = o['🩹 Model Patch: Gemini All-In-One'] = True
        elif patch:
            o[patch] = True
        if tag:
            o[tag] = True
        if red:
            o[red] = True
        for a in addons:
            if rng.random() < 0.35:
                o[a] = True
        if o.get('😈'):
            o['🔞'] = True
        for s in shipped:
            if rng.random() < 0.2:
                o[s] = False
        out.append((f'random #{k}: ' + ', '.join(f'{"+" if v else "-"}{key}' for key, v in o.items()), o))
    return out


def check_pair(cc_path, mar_path, show=6, assume_enabled=False, random_n=0):
    cc = json.load(open(cc_path))
    mar = json.load(open(mar_path))['data']
    problems = []
    prompts = {p['identifier']: p for p in cc['prompts']}
    blocks = {c['variableName']: c for c in mar['choiceBlocks']}
    options = {v: {o['value'] for o in json.loads(c['options'])} for v, c in blocks.items()}
    defaults = json.loads(mar['preset']['defaultChoices'])

    # 1. coverage and defaults
    for row in cc['prompt_order'][1]['order']:
        name = prompts[row['identifier']].get('name') or row['identifier']
        if prompts[row['identifier']].get('marker') or name.startswith(NO_CHOICE) or 'Demons of Delusion' in name:
            continue
        hit = cc_toggle(name)
        if not hit:
            if prompts[row['identifier']].get('content'):
                problems.append(f'toggle: CC entry "{name}" has no Marinara choice mapping')
            continue
        var, value = hit
        if value not in options.get(var, set()):
            problems.append(f'toggle: CC entry "{name}" has no Marinara option {var}={value}')
            continue
        d = defaults.get(var)
        shipped_on = row['enabled']
        picked = (value in d) if isinstance(d, list) else (d == value or (var == 'adult_mode' and d == 'FREAKY'))
        if var in ('logic_core',) and name.startswith('🧠') and shipped_on and d != value:
            problems.append(f'default: CC ships "{name}" ON, Marinara defaults {var}={d}')
        elif var not in ('logic_core', 'model_patch', 'adult_mode') and shipped_on != picked:
            problems.append(f'default: CC ships "{name}" {"ON" if shipped_on else "off"}, Marinara defaults {var}={d}')
    jb_cc = sorted(p['name'] for p in cc['prompts'] if 'Demons of Delusion' in (p.get('name') or ''))
    jb_mar = sorted(s['name'] for s in mar['sections'] if 'Demons of Delusion' in s['name'])
    if jb_cc != jb_mar:
        problems.append(f'jailbreaks: CC offers {jb_cc}, Marinara offers {jb_mar}')
    for c in blocks.values():
        for o in json.loads(c['options']):
            if re.search(r'Frankenstein|Micro Chain', o['label']):
                problems.append(f'label: choice {c["variableName"]} option "{o["label"]}" still names the Frankenstein-era step')
        if re.search(r'Freaky Frankenstein 5|Micro swaps', c['question']):
            problems.append(f'label: choice {c["variableName"]} question still describes the Frankenstein-era step')
    for s in mar['sections']:
        gate = re.match(r'\{\{#if (\w+) (==|contains) "(\w+)"', s['content'] or '')
        if gate and s['enabled'] not in (True, 'true') and gate.group(1) != 'state_mode':
            problems.append(f'gating: section "{s["name"]}" is switched off, so picking {gate.group(1)}={gate.group(3)} sends nothing')

    # 2. rendered parity
    names = {(x.get('name') or '') for x in cc['prompts']}
    matrix = list(MATRIX) + [(p.split(': ', 1)[1], {p: True}) for p in PATCHES if p in names]
    matrix += [('GLM Flash: GLM + Flash Gate', {'🩹 Model Patch: GLM': True, '🔦': True}),
               ('DeepSeek + Flash Gate', {'🩹 Model Patch: DeepSeek': True, '🔦': True}),
               ('DeepSeek + hardener', {'🩹 Model Patch: DeepSeek': True, '🧪': True}),
               ('Gemini 3.8 Flash', {'🩹 Model Patch: Gemini 3.8 Flash': True, '🩹 Model Patch: Gemini All-In-One': True}),
               ('no plan', {'🧠 The Logic Core': False}),
               ('no plan + hardener', {'🧠 The Logic Core': False, '🧪': True}),
               ('no plan + DeepSeek + hardener', {'🧠 The Logic Core': False, '🩹 Model Patch: DeepSeek': True, '🧪': True})]
    rich = {'🔞': True, '😈': True, '🧷': True, '🔦': True}  # every module line a jailbreak reads
    for jb in sorted(n for n in names if 'Demons of Delusion' in n):
        off = {'🧠 The Logic Core': False, jb: True}
        matrix += [(f'{jb}', off),
                   (f'{jb} + tags + adult/freaky, Hold, Flash', {**off, **rich, '🏷️ Logic Core Tags': True}),
                   (f'{jb} + DeepSeek + hardener', {**off, '🩹 Model Patch: DeepSeek': True, '🧪': True}),
                   (f'{jb} + GLM + Bonds only', {**off, '🩹 Model Patch: GLM': True, '🎲': False}),
                   (f'{jb} + Argon tags + Fate only', {**off, '🏷️ Gemini 4 Argon': True, '🥰': False})]
    if random_n:
        matrix += random_matrix(cc, random_n)
    clean = 0
    for label, overrides in matrix:
        enabled = cc_config(cc, overrides)
        ch = choices_for(cc, enabled)
        cs, cp = cc_blocks(cc, enabled)
        ms, mp = mar_blocks(mar, ch, assume_enabled)
        diffs = []
        for part, a, b in (('system', cs, ms), ('post-history', cp, mp)):
            la = strip_host_only(normalise('\n'.join(a)))
            lb = strip_host_only(normalise('\n'.join(b)))
            only_cc = [ln for ln in la if ln not in lb]
            only_mar = [ln for ln in lb if ln not in la]
            diffs += [f'  {part} CC only:       {ln[:160]}' for ln in only_cc]
            diffs += [f'  {part} Marinara only: {ln[:160]}' for ln in only_mar]
        if diffs:
            problems.append(f'render [{label}] {len(diffs)} differing lines')
            problems += diffs[:show]
        else:
            clean += 1
    return problems, clean, len(matrix)


def default_pairs():
    pairs = []
    for cc_pat, mar_pat in ((r"((?:(?! — ).)+) — \(Chat Completions\)\.json", r"((?:(?! — ).)+) — Marinara Engine Edition\.json"),
                            (r"((?:(?! — ).)+) — Chibi Edition \(Chat Completions\)\.json",
                             r"((?:(?! — ).)+) — Chibi Edition — Marinara Engine Edition\.json")):
        ccs = [f for f in (ROOT / 'presets' / 'Chat Completions' / 'Base').iterdir() if re.fullmatch(cc_pat, f.name)]
        mars = [f for f in (ROOT / 'presets' / 'Marinara Engine Edition' / 'Base').iterdir() if re.fullmatch(mar_pat, f.name)]
        if ccs and mars:
            pairs.append((max(ccs), max(mars)))
    return pairs


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    show = 6
    if '--show' in sys.argv:
        show = int(sys.argv[sys.argv.index('--show') + 1])
        args = [a for a in args if a != str(show)]
    pairs = [(Path(args[0]), Path(args[1]))] if len(args) == 2 else default_pairs()
    assume_enabled = '--assume-enabled' in sys.argv
    random_n = int(sys.argv[sys.argv.index('--random') + 1]) if '--random' in sys.argv else 0
    args = [a for a in args if a != str(random_n)]
    pairs = [(Path(args[0]), Path(args[1]))] if len(args) == 2 else default_pairs()
    failed = False
    for cc_path, mar_path in pairs:
        print(f'=== {cc_path.name}\n    vs {mar_path.name}')
        problems, clean, total = check_pair(cc_path, mar_path, show, assume_enabled, random_n)
        for p in problems:
            print(p)
        print(f'{clean}/{total} rendered configurations match')
        failed |= bool(problems)
        print()
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
