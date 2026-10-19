import json, sys
from pathlib import Path
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab

def total(r): return sum(ab.tokens(t) for t in r.values())
path = sys.argv[1]
preset = json.loads(Path(path).read_text(encoding='utf-8'))
system = preset['sysprompt']['content']
shipped = dict(ab.SWITCH.findall(system))
print('shipped switches:', {k: v for k, v in shipped.items()})
base_off = {s: 'off' for s in shipped}
def t(o): return total(ab.simulate_tc(preset, o, 1)[0])
print('all off:', t(base_off))
print('shipped:', t(shipped))
# marginal cost of each switch when added on top of "shipped" with the Logic Core on (so plan lines count)
lc = dict(shipped) | {'aria-logic-core': 'on'}
print('shipped + logic core:', t(lc), ' logic core cost over shipped:', t(lc) - t(shipped))
for s in shipped:
    if s in ('aria-logic-core',):
        continue
    on = dict(lc) | {s: 'on'}
    off = dict(lc) | {s: 'off'}
    d = t(on) - t(off)
    print(f'  {s:24} shipped={shipped[s]:3}  marginal (with Logic Core on): {d:5}')
# Logic core alone, tags off
a = dict(shipped) | {'aria-logic-core': 'on'}
b = dict(shipped) | {'aria-logic-core': 'on', 'aria-thinking-tags': 'off'}
print('tags on vs off (logic core on):', t(a) - t(b))
