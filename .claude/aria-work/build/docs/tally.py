import json, sys
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools')
import aria_budget as ab
def T(r): return sum(len(t) for t in r.values()) / 4
F = {'full': R + "/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",
     'chibi': R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"}
for ed, f in F.items():
    P = json.load(open(f)); sh = dict(ab.SWITCH.findall(P['sysprompt']['content']))
    def flip(extra, patch='aria-patch-deepseek', lc='on'):
        base = dict(sh) | {'aria-logic-core': lc} | extra
        return T(ab.simulate_tc(P, base | {patch: 'on'}, 1)[0]) - T(ab.simulate_tc(P, base | {patch: 'off'}, 1)[0])
    n = flip({}); fa = flip({'aria-fate': 'on'}); bo = flip({'aria-bonds': 'on'}); both = flip({'aria-fate': 'on', 'aria-bonds': 'on'})
    print(ed, 'deepseek LC on: none', n, 'fate', fa - n, 'bonds', bo - n, 'both', both - n)
    # Joins line cost: deepseek with flash-gate on vs off
    fg = flip({'aria-flash-gate': 'on'})
    print('   with flash gate on: ', fg, ' diff', fg - n)
    # runs line cost: flash gate flip with/without deepseek
    def fgflip(patch):
        base = dict(sh) | {'aria-logic-core': 'on'} | ({patch: 'on'} if patch else {})
        return T(ab.simulate_tc(P, base | {'aria-flash-gate': 'on'}, 1)[0]) - T(ab.simulate_tc(P, base | {'aria-flash-gate': 'off'}, 1)[0])
    print('   flash gate flip: no patch', fgflip(None), 'glm', fgflip('aria-patch-glm'), 'deepseek', fgflip('aria-patch-deepseek'))
