"""Rebuild each live file from its pre-change snapshot with only the intended raw-text replacements and compare byte for byte."""
import json
from rxlib import *


def esc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


def rd(path):
    return open(path, encoding='utf-8', newline='').read()


OLD = r'(?:[ \t]*When this turn asks for [^\n]{0,300}?Ledger lines\.)?'
NEW = r'(?:[ \t]*(?:When this turn asks for [^\n]{0,300}?Ledger lines|For a message written as [^\n]{0,300}? line)\.)?'
ok = True

# CC: Fix 1 + Fix 3 + Fix 4 (NPC Voice comment)
exp = rd(SNAP_CC)
f1o = "{{setvar::ariaJbLines::}}\n{{trim}}\nYou are the narrator and game master"
f1n = "{{setvar::ariaJbLines::}}{{setvar::gemini38Patch::}}\n{{trim}}\nYou are the narrator and game master"
assert exp.count(esc(f1o)) == 1
exp = exp.replace(esc(f1o), esc(f1n))
assert exp.count(esc(OLD)) == 5
exp = exp.replace(esc(OLD), esc(NEW))
f4o, f4n = "Leave this ON; it costs about 300 tokens.", "Leave this ON; it costs about 350 tokens."
assert exp.count(esc(f4o)) == 1
exp = exp.replace(esc(f4o), esc(f4n))
live = rd(CCFILE)
print('CC  live == snapshot + Fix 1 + Fix 3 (x5) + Fix 4 (x1):', live == exp); ok &= live == exp
d = json.loads(live); assert json.dumps(d, ensure_ascii=False, indent=4) == live

# TC regex: Fix 3
exp = rd(SNAP_RX)
assert exp.count(esc(OLD)) == 5
exp = exp.replace(esc(OLD), esc(NEW))
live = rd(RXFILE)
print('TC regex live == snapshot + Fix 3 (x5):', live == exp); ok &= live == exp
d = json.loads(live); assert json.dumps(d, ensure_ascii=False, indent=4) == live

# TC: Fix 4 (two comments); the snapshot is the TC as it stood before my edits
exp = rd(W + '/build/orig/TC.json')
for o, n in (("Great for 24B+ models, costs about 325 tokens a turn.", "Great for 24B+ models, costs about 405 tokens a turn."),
             ("moods and instincts). About 360 tokens.", "moods and instincts). About 350 tokens.")):
    assert exp.count(esc(o)) == 1
    exp = exp.replace(esc(o), esc(n))
live = rd(TCFILE)
print('TC  live == snapshot + Fix 4 (x2)                     :', live == exp); ok &= live == exp
d = json.loads(live); assert json.dumps(d, ensure_ascii=False, indent=4) == live

# the two CC / TC copies of the four scripts are identical, all 31 findRegex strings equal across the files
cc = json.loads(rd(CCFILE))['extensions']['regex_scripts']
tcx = json.loads(rd(RXFILE))
print('CC and TC regex copies identical for scripts 0, 1, 2, 24:', all(cc[i] == tcx[i] for i in (0, 1, 2, 24)))
print('all 31 findRegex strings equal between the two files   :', [s['findRegex'] for s in cc] == [s['findRegex'] for s in tcx])
print('REPLACEMENT COUNTS: Fix 1 = 1, Fix 3 = 5 per file (scripts 0,1,2 once; 24 twice), Fix 4 = 1 in CC and 2 in TC')
print('ALL BYTE-EXACT' if ok else 'MISMATCH')
