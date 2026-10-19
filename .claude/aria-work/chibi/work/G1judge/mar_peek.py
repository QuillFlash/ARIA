import json, re, sys
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
m = open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json", encoding='utf-8').read()
d = json.loads(m)
print(list(d.keys()))
kws = ['impersonation_turn', 'reasoning_constraints', 'Story Language', 'Custom Player Instructions', '# Reference', "This turn's POV", 'Elara', 'While reasoning']
def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + '/' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + f'[{i}]')
    elif isinstance(o, str):
        yield path, o
for path, s in walk(d):
    for kw in kws:
        i = s.find(kw)
        if i >= 0:
            print(kw, '|', path, '|', repr(s[max(0, i - 120):i + 160]))
            print()
