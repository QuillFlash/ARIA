#!/usr/bin/env python3
"""ARIA budget and cache checker.

Simulates one SillyTavern turn for the Chat Completions preset, counts the
rendered tokens (characters / 4, comments stripped) for three configurations,
and fails when something would break the budget, the wiring or prompt caching.

Usage: python3 tools/aria_budget.py [path/to/preset.json]
"""
import json
import random
import re
import sys
from pathlib import Path

BUDGET = 4500
DEFAULT_PRESET = Path(__file__).resolve().parent.parent / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
VOLATILE = re.compile(r'\{\{(roll|random|pick|time|date|weekday|isotime|isodate|idle_duration|lastMessage|'
                      r'lastCharMessage|lastUserMessage|lastMessageId|currentSwipeId|char|group|charIfNotGroup|input)\b')
HTML_TAGS = {'details', 'summary', 'thinking', 'think', 'br', 'b', 'span', 'div'}


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


def find_endif(s, i):
    """Return (start, end) of the {{/if}} matching an {{#if}} whose body starts at s[i]."""
    depth, j = 1, i
    while j < len(s):
        if s.startswith('{{#if', j):
            depth += 1
        elif s.startswith('{{/if}}', j):
            depth -= 1
            if depth == 0:
                return j, j + len('{{/if}}')
        j += 1
    raise ValueError('unclosed {{#if}}')


def render(s, state, rng):
    """Render the macros ARIA uses, roughly the way SillyTavern's macro engine does."""
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
        elif m.startswith('getvar::'):
            out.append(state.get(m[len('getvar::'):], ''))
        elif m.startswith('.') and '=' in m:
            name, _, value = m[1:].partition('=')
            state[name.strip()] = value.strip()
        elif m.startswith('#if'):
            cond = m[3:].strip().lstrip('.')
            k, end = find_endif(s, j)
            if state.get(cond, '').strip():
                out.append(render(s[j:k], state, rng))
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
    return re.sub(r'\n*[ \t]*\x00TRIM\x00[ \t]*\n*', '', text)


def strip_setvar_bodies(s):
    """Content with every setvar body removed, to find volatile macros that would render in place."""
    out, i = [], 0
    while i < len(s):
        if s.startswith('{{setvar::', i) or s.startswith('{{//', i):
            i = take_macro(s, i)
            continue
        out.append(s[i])
        i += 1
    return ''.join(out)


def simulate(preset, enabled, seed, state=None, impersonate=False):
    """Render one turn: relative entries top to bottom, then In-Chat entries. Returns {id: text}."""
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


def tokens(text):
    return round(len(text) / 4)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PRESET
    preset = json.loads(path.read_text(encoding='utf-8'))
    prompts = {p['identifier']: p for p in preset['prompts']}
    order = preset['prompt_order'][1]['order']
    name = {pid: prompts[pid].get('name', pid) for pid in prompts}
    errors = []

    # --- structure ---
    ids = [p['identifier'] for p in preset['prompts']]
    if len(ids) != len(set(ids)):
        errors.append('duplicate prompt identifiers')
    for row in order:
        if row['identifier'] not in prompts:
            errors.append(f"prompt_order names a missing prompt: {row['identifier']}")

    # --- configurations ---
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
        rendered, _ = simulate(preset, enabled, seed=1)
        totals[label] = sum(tokens(t) for t in rendered.values())
        if label == 'everything ON':
            print('Per-entry tokens with everything ON:')
            for pid, text in rendered.items():
                print(f'  {tokens(text):5}  {name[pid]}')
    imp, _ = simulate(preset, all_on, seed=1, impersonate=True)
    normal, _ = simulate(preset, all_on, seed=1)
    totals['Impersonate adds'] = sum(tokens(t) for t in imp.values()) - totals['everything ON'] + \
        sum(tokens(normal[pid]) for pid in normal if pid not in imp)
    print('\nTotals:')
    for label, value in totals.items():
        print(f'  {label:18} {value:5}')
    if totals['everything ON'] > BUDGET:
        errors.append(f"everything ON is {totals['everything ON']} tokens, over the {BUDGET} budget")

    # --- wiring: tags, labels, variables ---
    rendered, _ = simulate(preset, all_on, seed=1)
    text_all = '\n'.join(rendered.values())
    defined = {t for t in re.findall(r'<([A-Za-z_]+)>', text_all) if f'</{t}>' in text_all}
    for t in sorted(set(re.findall(r'<([A-Za-z_]+)>', text_all)) - defined - HTML_TAGS):
        errors.append(f'dangling tag reference <{t}>')
    main_text = rendered.get('main', '')
    labels = set(re.findall(r'\*\*([^*]+?):\*\*', main_text))
    for pid, t in rendered.items():
        if pid == 'main':
            continue
        # a label in the middle of a line points at the Main Prompt; one opening a line is a local heading
        for hit in re.finditer(r'\*\*([^*]+?):\*\*', t):
            line_start = t.rfind('\n', 0, hit.start()) + 1
            if re.fullmatch(r'[\s\-*#]*', t[line_start:hit.start()]):
                continue
            label = hit.group(1)
            if label not in labels:
                errors.append(f"{name[pid]} points at **{label}:**, which the Main Prompt does not define")
    raw_all = '\n'.join(p.get('content') or '' for p in preset['prompts'])
    setters = set(re.findall(r'\{\{setvar::([\w-]+)::', raw_all)) | set(re.findall(r'\{\{\.([\w-]+)\s*=', raw_all))
    readers = set(re.findall(r'\{\{getvar::([\w-]+)\}\}', raw_all)) | set(re.findall(r'\{\{#if \.([\w-]+)\}\}', raw_all))
    for v in sorted(readers - setters):
        errors.append(f'variable read but never set: {v}')
    for v in sorted(setters - readers):
        errors.append(f'variable set but never read: {v}')
    blanked = set(re.findall(r'\{\{setvar::([\w-]+)::\}\}', prompts['main']['content']))
    for v in sorted(v for v in setters if v.startswith('aria') and v not in blanked):
        errors.append(f'splice variable not blanked by the Main Prompt: {v}')

    # --- cache lint ---
    stale = {v: 'stale value from an earlier turn' for v in setters}
    a, _ = simulate(preset, all_on, seed=1)
    b, _ = simulate(preset, all_on, seed=99, state=stale)
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

    print()
    if errors:
        print('FAILED:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    print('OK: budget, wiring and cache checks all pass.')


if __name__ == '__main__':
    main()
