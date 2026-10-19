import json, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab
ROOT = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/'
tc = json.load(open('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/jbdocs2/head/tc.json', encoding='utf-8'))
sw = dict(ab.SWITCH.findall(tc['sysprompt']['content']))
def T(over):
    r, st = ab.simulate_tc(tc, over, seed=1)
    return sum(ab.tokens(t) for t in r.values())
shipped = dict(sw)
lc = shipped | {'aria-logic-core': 'on'}
print('shipped', T(shipped), ' +LC', T(lc) - T(shipped))
for s in sw:
    if s in ('aria-logic-core',):
        continue
    base_off = dict(shipped); base_off[s] = 'off'
    base_on = dict(shipped); base_on[s] = 'on'
    d_ship = T(base_on) - T(base_off)
    lo = dict(lc); lo[s] = 'off'; ln = dict(lc); ln[s] = 'on'
    d_lc = T(ln) - T(lo)
    extra = ''
    if s in ('aria-freaky', 'aria-jailbreak'):
        a0 = dict(lc) | {'aria-adult': 'on', s: 'off'}; a1 = dict(lc) | {'aria-adult': 'on', s: 'on'}
        extra = f'  (+adult, LC on: {T(a1) - T(a0)})'
        a0 = dict(shipped) | {'aria-adult': 'on', s: 'off'}; a1 = dict(shipped) | {'aria-adult': 'on', s: 'on'}
        extra += f'  (+adult, LC off: {T(a1) - T(a0)})'
    if s == 'aria-thinking-tags':
        a0 = dict(lc) | {s: 'off'}; a1 = dict(lc) | {s: 'on'}
        extra = f' tags on vs off with LC: {T(a1) - T(a0)}'
    print(f'{s:24} shipped-delta {d_ship:5}   LC-on-delta {d_lc:5}{extra}')
