"""Every block condition in Chibi Marinara, classified; flags a bare {{#if name}} (TRUE in Marinara)."""
import json, re, sys
from collections import Counter
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/build/chibi_mar')
from common import *
path = Path(sys.argv[1]) if len(sys.argv) > 1 else CHIBI_MAR
C = load(path)
vars_ = {cb['variableName']: [o['value'] for o in json.loads(cb['options'])] for cb in C['data']['choiceBlocks']}
multi = {cb['variableName']: cb['multiSelect'] for cb in C['data']['choiceBlocks']}
cnt = Counter(); bad = []
ATOM = re.compile(r'^\s*(\w+)\s*(==|!=|contains|not contains)\s*"([^"]*)"\s*$')
for s in C['data']['sections']:
    for m in re.finditer(r'\{\{(#if|else if|#unless|if)\s+([^}]*?)\}\}', s['content']):
        kind, cond = m.groups()
        for atom in re.split(r'\s*(?:&&|\|\|)\s*', cond):
            a = ATOM.match(atom)
            if not a:
                bad.append((s['name'], kind, cond)); continue
            v, op, val = a.groups()
            if v not in vars_:
                bad.append((s['name'], 'unknown var', cond)); continue
            if val not in vars_[v]:
                bad.append((s['name'], 'unknown value %s for %s' % (val, v), cond))
            if ('contains' in op) != (multi[v] == 'true'):
                bad.append((s['name'], 'op/multi mismatch', cond))
            cnt[(v, op, val)] += 1
    for m in re.finditer(r'\{\{([#/]?\w+)', s['content']):
        cnt['macro:' + m.group(1)] += 1
print('bad conditions:', bad)
print('choice values never tested:', [(v, x) for v, xs in vars_.items() for x in xs
       if not any(k[0] == v and k[2] == x for k in cnt if isinstance(k, tuple))])
print(sorted(k for k in cnt if isinstance(k, str)))
print({v: vars_[v] for v in vars_})
