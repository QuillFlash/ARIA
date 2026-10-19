"""Structural diff: Chibi Marinara vs ARIA Marinara (everything except section content and the expected metadata)."""
import json, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/build/chibi_mar')
from common import *
A = load(ARIA_MAR); C = load(CHIBI_MAR)
def walk(a, c, path):
    if type(a) != type(c):
        print('TYPE', path, type(a).__name__, type(c).__name__); return
    if isinstance(a, dict):
        if list(a.keys()) != list(c.keys()):
            print('KEYS', path, list(a.keys()), list(c.keys()))
        for k in a:
            if k in c: walk(a[k], c[k], path + '.' + k)
    elif isinstance(a, list):
        if len(a) != len(c): print('LEN', path, len(a), len(c))
        for i, (x, y) in enumerate(zip(a, c)): walk(x, y, '%s[%d]' % (path, i))
    elif a != c:
        s = path
        if path.endswith('.content'):
            print('CONTENT', path); return
        print('DIFF', path, repr(a)[:150], '=>', repr(c)[:150])
walk(A, C, '')
raw = CHIBI_MAR.read_text(encoding='utf-8')
print('round trip exact:', json.dumps(C, ensure_ascii=False, indent='\t') == raw, '; trailing newline:', raw.endswith('\n'))
p = C['data']['preset']
print('id', p['id'], len(p['id']), '| ARIA id', A['data']['preset']['id'], len(A['data']['preset']['id']))
ids = set()
for key in C['data']:
    v = C['data'][key]
    if isinstance(v, list):
        for it in v:
            if isinstance(it, dict) and 'presetId' in it: ids.add(it['presetId'])
            if isinstance(it, dict) and 'id' in it and it['id'] in json.dumps(A['data'][key]): pass
print('child presetIds', ids)
print('raw contains ARIA id anywhere:', A['data']['preset']['id'] in raw)
print('dates', C.get('exportedAt'), p.get('createdAt'), p.get('updatedAt'))
for k in C:
    if k != 'data': print('top', k, repr(C[k])[:100])
for k in C['data']:
    print('data key', k, type(C['data'][k]).__name__, len(C['data'][k]) if hasattr(C['data'][k], '__len__') else '')
