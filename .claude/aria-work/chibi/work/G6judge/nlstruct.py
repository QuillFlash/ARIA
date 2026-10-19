import json, sys, difflib
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
from aria_budget import take_macro
from rows import IDS
def struct(s):
    out, i = [], 0
    while i < len(s):
        if s.startswith('{{', i):
            j = take_macro(s, i); m = s[i+2:j-2]
            if m.startswith('//'): out.append('COMMENT')
            elif m.startswith(('setvar::', 'addvar::')):
                kind, rest = m.split('::', 1); name, _, b = rest.partition('::')
                out.append(f'{kind}::{name}['); out += ['  ' + x for x in struct(b)]; out.append(']')
            elif m in ('user', 'char'): out.append('TXT')
            else: out.append(m)
            i = j
        elif s[i] == '\n':
            out.append('NL'); i += 1
        else:
            if not out or out[-1] != 'TXT': out.append('TXT')
            i += 1
    # collapse TXT runs
    res = []
    for x in out:
        if x == 'TXT' and res and res[-1] == 'TXT': continue
        res.append(x)
    return res
src = json.load(open('src_g6.json', encoding='utf-8'))['prompts']
fin = json.load(open(sys.argv[1], encoding='utf-8'))['prompts']
for k, pid in IDS.items():
    a, b = struct(src[pid]['content']), struct(fin[pid]['content'])
    if a == b: print('SAME ', k); continue
    print('DIFF ', k)
    for l in difflib.unified_diff(a, b, 'source', 'final', lineterm='', n=1):
        print('     ', l)
