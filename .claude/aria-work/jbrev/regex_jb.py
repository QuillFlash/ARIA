#!/usr/bin/env python3
"""Run every plan-handling regex script (CC and the TC regex file) on model outputs that carry a plan with and without
the JB's Role and Frank lines. Each script must treat both the same way: if it removes or folds the plan without the
JB lines, it must remove or fold the whole plan with them too (no Role/Frank line left behind in the visible text).
"""
import json, re, sys
from pathlib import Path

ROOT = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
S = ROOT / '.claude/aria-work'
sys.path.insert(0, str(ROOT / 'tools'))
import aria_budget as ab  # noqa: E402

FIN = json.loads((S / 'jb/final.json').read_text(encoding='utf-8'))
JBL = [l.replace('{{user}}', 'Lewis') for l in FIN['lines']]


def to_py(js):
    m = re.fullmatch(r'/(.*)/([a-z]*)', js, re.S)
    f = 0
    for ch in m.group(2):
        f |= {'i': re.I, 'm': re.M, 's': re.S, 'g': 0, 'u': 0}[ch]
    return re.compile(m.group(1), f), 'g' in m.group(2)


def js_repl(rep):
    # JS $1 -> Python \1 ; $& -> \g<0>
    rep = rep.replace('\\', '\\\\')
    rep = re.sub(r'\$(\d+)', r'\\g<\1>', rep)
    return rep.replace('$&', r'\g<0>')


def apply(script, text):
    rx, g = to_py(script['findRegex'])
    return rx.sub(js_repl(script['replaceString']), text, count=0 if g else 1)


plan_core = ['- OOC: none.', '- Scene: kitchen, both standing; Mira holds a mug.', '- Knows: Mira saw the letter.',
             '- Mode: realism; persona-true; each plea new.', '- Voice: Mira, wary; low register.',
             '- Move: Mira sets the mug down and asks.', '- Ledger: 🎲 q1 hp2.']
tail = ['- Fresh: the kettle ticks as it cools.', '- Check: lists in ones or twos.', '- go']
reply = 'Mira sets the mug down. "Who sent it?"'
variants = {}
for jb in (False, True):
    plan = plan_core + (JBL if jb else []) + tail
    variants[('untagged', jb)] = '\n'.join(plan) + '\n' + reply
    variants[('thinking', jb)] = '<thinking>\n' + '\n'.join(plan) + '\n</thinking>\n' + reply
    variants[('logic_core', jb)] = '<logic_core>\n' + '\n'.join(plan) + '\n</logic_core>\n' + reply
    # an echoed template (tags mode), the way a model copies the Logic Core's own last message
    variants[('echo', jb)] = ('<thinking> opens the reply, then 12 dashed lines, then go.\n'
                              'Lines are fragments that paraphrase what anyone said.\n' + '\n'.join(plan) +
                              '\n</thinking> closes on the line after go. The reply starts on the line after that: header if <header_instructions>.'
                              '\nEvery response starts with <thinking>.\n' + reply)

problems = 0
for label, scripts in (('CC', json.loads((ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json").read_text(encoding='utf-8'))['extensions']['regex_scripts']),
                       ('TC', json.loads((ROOT / 'regex/ARIA 1.0 Regex Scripts (Text Completions).json').read_text(encoding='utf-8')))):
    for s in scripts:
        if s.get('disabled'):
            continue
        for kind in ('untagged', 'thinking', 'logic_core', 'echo'):
            a, b = variants[(kind, False)], variants[(kind, True)]
            try:
                ra, rb = apply(s, a), apply(s, b)
            except re.error as e:
                print('COMPILE', label, s['scriptName'], e)
                problems += 1
                break
            changed_a, changed_b = ra != a, rb != b
            leftover = [l for l in JBL if l in rb] if changed_b else []
            plan_left_a = '- Scene:' in ra
            plan_left_b = '- Scene:' in rb
            if changed_a != changed_b or plan_left_a != plan_left_b or (changed_b and leftover and not plan_left_b):
                problems += 1
                print(f'DIFF {label} {s["scriptName"][:70]} [{kind}] no-JB changed={changed_a} plan_left={plan_left_a} | '
                      f'JB changed={changed_b} plan_left={plan_left_b} leftover={len(leftover)}')
            # Role/Frank must not survive when the plan around them is removed
            if changed_b and not plan_left_b and any(l[:12] in rb for l in JBL):
                problems += 1
                print(f'LEFTOVER {label} {s["scriptName"][:70]} [{kind}]')
print('problems:', problems)
