#!/usr/bin/env python3
"""total.py [g5draft.json]: swap the G1-G4 drafts (and optionally a G5 draft) into an in-memory copy of the snapshot CC,
then print the per-entry tokens of the fully-ON path the way the frozen checker computes it."""
import json, sys, copy, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
SRC = W + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
cc = json.load(open(SRC, encoding='utf-8'))
def swap(preset, draftfile):
    d = json.load(open(draftfile, encoding='utf-8'))
    by = {p['identifier']: p for p in preset['prompts']}
    n = 0
    for k, v in d['prompts'].items():
        for pid in by:
            if pid == k or pid.startswith(k) or k.startswith(pid):
                by[pid]['content'] = v['content']; n += 1
    return n
use = sys.argv[1:] or []
files = [W + f'/chibi/drafts/G{i}.json' for i in (1, 2, 3, 4)] + use
for f in files:
    print('swapped', swap(cc, f), 'from', f.split('/')[-1])
totals, errors = ab.analyse_cc(cc)
print(totals)
print('errors:', errors[:6])
