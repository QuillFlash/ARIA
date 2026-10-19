import json, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
from paths import *
d = json.load(open(CC, encoding='utf-8'))
by = {p['identifier']: p for p in d['prompts']}
for k in (CODEX, GATE):
    p = by[k]
    print('=====', k, p.get('name'), 'role', p.get('role'), 'pos', p.get('injection_position'), 'depth', p.get('injection_depth'))
    print(p['content'])
    print()
