import json, sys
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools')
import aria_budget as ab
F = {'full': R + "/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",
     'chibi': R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"}
for ed, f in F.items():
    P = json.load(open(f)); sh = dict(ab.SWITCH.findall(P['sysprompt']['content']))
    T = lambda o: sum(len(t) for t in ab.simulate_tc(P, o, 1)[0].values())/4
    base = dict(sh) | {'aria-logic-core': 'on'}
    def ds(o): return T(o | {'aria-patch-deepseek': 'on'}) - T(o | {'aria-patch-deepseek': 'off'})
    d0 = ds(base | {'aria-fate': 'off', 'aria-bonds': 'off'})
    for fb in [('on','off'),('off','on'),('on','on')]:
        print(ed, 'fate=%s bonds=%s' % fb, round(ds(base | {'aria-fate': fb[0], 'aria-bonds': fb[1]}) - d0, 1))
