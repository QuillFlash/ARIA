import json, sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
from paths import *
import aria_budget as ab
d = json.load(open(CC, encoding='utf-8'))
by = {p['identifier']: p for p in d['prompts']}
for row in d['prompt_order'][1]['order']:
    p = by[row['identifier']]
    c = p.get('content') or ''
    print(f"{row['enabled']!s:5} pos{p.get('injection_position') or 0} {p.get('role','?'):9} {ab.tokens(ab.render(c, {}, random.Random(1))):5} {p['identifier'][:12]:12} {p.get('name')}")
