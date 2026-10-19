import json, sys, re
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools')
import aria_budget as ab
def T(r): return sum(len(t) for t in r.values()) / 4
F = {'full': R + "/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",
     'chibi': R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"}
pre = {'aria-freaky': {'aria-adult': 'on'}, 'aria-jailbreak': {'aria-adult': 'on', 'aria-logic-core': 'on'},
       'aria-thinking-tags': {'aria-logic-core': 'on'}}
res = {}
for ed, f in F.items():
    P = json.load(open(f)); sh = dict(ab.SWITCH.findall(P['sysprompt']['content']))
    for lc in ('shipped', 'lc_on', 'lc_off'):
        for s in sh:
            base = dict(sh)
            if lc == 'lc_on': base['aria-logic-core'] = 'on'
            if lc == 'lc_off': base['aria-logic-core'] = 'off'
            base |= pre.get(s, {}) if lc != 'lc_off' else {k: v for k, v in pre.get(s, {}).items() if k != 'aria-logic-core'}
            if s == 'aria-flash-gate': base['aria-patch-glm'] = 'on' if False else base['aria-patch-glm']
            on = dict(base) | {s: 'on'}; off = dict(base) | {s: 'off'}
            res[(ed, lc, s)] = T(ab.simulate_tc(P, on, 1)[0]) - T(ab.simulate_tc(P, off, 1)[0])
names = list(dict.fromkeys(k[2] for k in res))
print(f"{'switch':24} | full shipped | full LC on | chibi shipped(LC on) | chibi LC off")
for s in names:
    print(f"{s:24} | {res[('full','shipped',s)]:8.1f} | {res[('full','lc_on',s)]:8.1f} | {res[('chibi','shipped',s)]:8.1f} | {res[('chibi','lc_off',s)]:8.1f}")
