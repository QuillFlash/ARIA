import json, sys
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools')
import aria_budget as ab
F = {'full': R + "/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",
     'chibi': R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"}
for ed, f in F.items():
    P = json.load(open(f)); sh = dict(ab.SWITCH.findall(P['sysprompt']['content']))
    patches = [s for s in sh if s.startswith('aria-patch')]
    base = {s: 'on' for s in sh if not s.startswith('aria-patch')} | {p: 'off' for p in patches}
    T = lambda o: sum(ab.tokens(t) for t in ab.simulate_tc(P, o, 1)[0].values())
    b = T(base)
    print(ed, 'base', b, {p: T(base | {p: 'on'}) for p in patches})
    # tally: deepseek with LC on, fate/bonds combos
    for combo in [('off','off'),('on','off'),('off','on'),('on','on')]:
        o = dict(sh) | {'aria-logic-core':'on','aria-patch-deepseek':'on','aria-fate':combo[0],'aria-bonds':combo[1]}
        r = ab.simulate_tc(P, o, 1)[0]
        tl = [l for l in r['Post-History'].split('\n') if l.startswith('- Tally')]
        print('  tally fate=%s bonds=%s:' % combo, [round(len(l)/4) for l in tl])
