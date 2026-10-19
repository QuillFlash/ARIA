import json, sys
from pathlib import Path
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab
def total(r): return sum(ab.tokens(t) for t in r.values())
path = sys.argv[1]
preset = json.loads(Path(path).read_text(encoding='utf-8'))
system = preset['sysprompt']['content']
shipped = dict(ab.SWITCH.findall(system))
def t(o): return total(ab.simulate_tc(preset, o, 1)[0])
print('Logic Core cost over shipped (tags on):', t(dict(shipped)|{'aria-logic-core':'on'}) - t(shipped))
print('Logic Core cost over shipped (tags off):', t(dict(shipped)|{'aria-logic-core':'on','aria-thinking-tags':'off'}) - t(dict(shipped)|{'aria-thinking-tags':'off'}))
print('module own cost (Logic Core OFF) / with Logic Core ON:')
for s in shipped:
    if s in ('aria-logic-core','aria-thinking-tags'): continue
    if s.startswith('aria-patch'): continue
    flip = 'off' if shipped[s]=='on' else 'on'
    a = dict(shipped); b = dict(shipped); b[s] = flip
    d0 = abs(t(a)-t(b))
    a2 = dict(a)|{'aria-logic-core':'on'}; b2 = dict(b)|{'aria-logic-core':'on'}
    d1 = abs(t(a2)-t(b2))
    print(f'  {s:22} {d0:5}   {d1:5}')
