import json, sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
d = json.load(open(sys.argv[1], encoding='utf-8'))
state0 = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
tot = 0
for pid, p in d['prompts'].items():
    st = dict(state0)
    out = ab.render(p['content'], st, random.Random(1))
    print('=' * 20, p['name'], len(out) / 4)
    for l in out.split('\n'):
        print(f'{len(l)/4:6.1f}  {l[:110]}')
