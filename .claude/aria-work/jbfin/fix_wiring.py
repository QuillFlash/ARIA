#!/usr/bin/env python3
"""Raw-text fixes for the JB wiring gaps (COMMON.md rule 7: find json.dumps(old)[1:-1] in the raw text,
assert the occurrence count, replace with json.dumps(new)[1:-1]). Never re-dumps CC or TC."""
import json
from pathlib import Path

ROOT = Path("/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA")
CCP = ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
TCP = ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"


def enc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


def rep(raw, old, new, count=1, label=''):
    o, n = enc(old), enc(new)
    got = raw.count(o)
    assert got == count, f'{label}: expected {count} occurrence(s) of the old text, found {got}'
    assert o != n
    return raw.replace(o, n)


def rep_raw(raw, old, new, count=1, label=''):
    """For structure that is not inside a JSON string value (numbers, keys): exact raw text."""
    got = raw.count(old)
    assert got == count, f'{label}: expected {count} occurrence(s) of the raw text, found {got}'
    return raw.replace(old, new)


def load(p):
    return p.read_text(encoding='utf-8')


def save(p, raw):
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(raw)


RUN_MID = '{{setvar::ariaModeLine::}}{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}{{setvar::ariaScentGate::}}'
RUN_MID_FIXED = '{{setvar::ariaModeLine::}}{{setvar::ariaScentGate::}}'
RUN_END = '{{setvar::ariaPatchTally::}}{{setvar::ariaPatchJoins::}}\n{{trim}}\nYou are the narrator and game master'
RUN_END_FIXED = '{{setvar::ariaPatchTally::}}{{setvar::ariaPatchJoins::}}{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}\n{{trim}}\nYou are the narrator and game master'

# ---------------------------------------------------------------- CC
raw = load(CCP)
before = json.loads(raw)

# A. the two plan lines are joined by a real newline, not by a literal backslash and n
raw = rep(raw, 'nervous cards stay nervous.\\n- Frank:', 'nervous cards stay nervous.\n- Frank:', 1, 'CC join')

# B. injection_order is Character Hold's 100 (JB.md: the other values are the same as Character Hold's)
raw = rep_raw(raw,
              'explicitly in those terms.}}{{/if}}",\n            "injection_position": 0,\n            "injection_depth": 4,\n            "injection_order": 0,\n',
              'explicitly in those terms.}}{{/if}}",\n            "injection_position": 0,\n            "injection_depth": 4,\n            "injection_order": 100,\n',
              1, 'CC injection_order')

# C. the two blanks are appended to the end of the Main Prompt's blanking run
raw = rep(raw, RUN_MID, RUN_MID_FIXED, 1, 'CC main blanks (remove mid-run)')
raw = rep(raw, RUN_END, RUN_END_FIXED, 1, 'CC main blanks (append)')

after = json.loads(raw)

# only the intended things changed
changed = []
for pb, pa in zip(before['prompts'], after['prompts']):
    for k in pb:
        if pb[k] != pa[k]:
            changed.append((pb['name'], k))
assert before['prompt_order'] == after['prompt_order']
assert before['extensions'] == after['extensions']
assert [k for k in before if before[k] != after[k]] == ['prompts']
print('CC changed fields:', changed)
assert sorted(changed) == sorted([('⚡ ARIA Main Prompt', 'content'), ('🔓 Jailbreak (needs Adult Context)', 'content'),
                                  ('🔓 Jailbreak (needs Adult Context)', 'injection_order')]), changed
save(CCP, raw)

# ---------------------------------------------------------------- TC
raw = load(TCP)
before = json.loads(raw)

# C'. the same blanks appended to the end of the TC Main Prompt's blanking run
raw = rep(raw, RUN_MID, RUN_MID_FIXED, 1, 'TC main blanks (remove mid-run)')
raw = rep(raw, RUN_END, RUN_END_FIXED, 1, 'TC main blanks (append)')

# E. no stray newline between the freaky block and the Jailbreak block
raw = rep(raw, '</freaky_override>\n{{/if}}\n{{#if .aria-jailbreak}}', '</freaky_override>\n{{/if}}{{#if .aria-jailbreak}}', 1, 'TC stray newline')

after = json.loads(raw)
assert [k for k in before if before[k] != after[k]] == ['sysprompt']
assert [k for k in before['sysprompt'] if before['sysprompt'][k] != after['sysprompt'][k]] == ['content']
save(TCP, raw)
print('TC: only sysprompt.content changed')
print('done')
