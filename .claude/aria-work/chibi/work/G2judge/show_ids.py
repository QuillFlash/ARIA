import json, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
from paths import *
d = json.load(open(CC, encoding='utf-8'))
for p in d['prompts']:
    if any(p['identifier'].startswith(x) for x in sys.argv[1:]):
        print('=====', p['identifier'], p.get('name'))
        print(p.get('content'))
        print()
