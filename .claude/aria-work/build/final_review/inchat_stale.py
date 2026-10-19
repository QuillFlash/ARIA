import json, sys, random, itertools
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools'); import aria_budget as ab
P = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"))
pr = {p['identifier']: p for p in P['prompts']}; nm = {k: v['name'] for k, v in pr.items()}
order = [r['identifier'] for r in P['prompt_order'][1]['order']]
patches = [p for p in order if nm[p].startswith('🩹')]; lcs = [p for p in order if nm[p].startswith('🧠 The Logic Core')]
fixed_off = {p for p in order if nm[p].startswith(('🌳', '🌿')) or p == 'enhanceDefinitions'}
others = [p for p in order if p not in patches and p not in lcs and p not in fixed_off and not pr[p].get('marker')]
rng = random.Random(3); prev = {}; bad = 0; n = 0
g38 = [p for p in patches if '3.8' in nm[p]][0]; aio = [p for p in patches if 'All-In-One' in nm[p]][0]
for pset, lc, imp, rep in itertools.product([[p] for p in patches] + [[aio, g38], []], lcs + [None], (False, True), range(6)):
    en = {o for o in others if rng.random() < 0.6} | {'main'} | set(pset) | ({lc} if lc else set())
    a, st = ab.simulate_cc(P, en, 1, impersonate=imp)
    b, _ = ab.simulate_cc(P, en, 1, state=prev, impersonate=imp)
    n += 1
    if a != b:
        bad += 1; print('CC leak', [nm[p] for p in a if a[p] != b.get(p)], [nm[p] for p in pset], imp)
    prev = st
print('ARIA CC', n, 'turn pairs, leaks', bad)
T = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"))
sh = dict(ab.SWITCH.findall(T['sysprompt']['content'])); tp = [s for s in sh if s.startswith('aria-patch')]
prev = {}; bad = 0; n = 0
for patch, rep in itertools.product(tp + [None], range(60)):
    ov = {s: ('on' if rng.random() < 0.6 else 'off') for s in sh if s not in tp} | {p: 'off' for p in tp} | ({patch: 'on'} if patch else {})
    a, st = ab.simulate_tc(T, ov, 1); b, _ = ab.simulate_tc(T, ov, 1, state=prev); n += 1
    if a != b: bad += 1; print('TC leak', patch, [k for k in a if a[k] != b[k]])
    prev = st
print('ARIA TC', n, 'turn pairs, leaks', bad)
