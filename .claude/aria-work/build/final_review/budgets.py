import json, sys, itertools, io, contextlib
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools')
import aria_budget as ab
FILES = ["Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",
         "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json", "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"]
def tot(r): return sum(ab.tokens(t) for t in r.values())
for f in FILES:
    P = json.load(open(R + '/' + f)); cap = ab.budget_for(f)
    with contextlib.redirect_stdout(io.StringIO()):
        totals, errs = (ab.analyse_tc if 'sysprompt' in P else ab.analyse_cc)(P, f)
    print('===', f[38:], 'cap', cap, totals, 'errors', errs)
    if 'sysprompt' in P:
        sw = dict(ab.SWITCH.findall(P['sysprompt']['content']))
        patches = [s for s in sw if s.startswith('aria-patch')]
        others = [s for s in sw if s not in patches]
        best = (0, None)
        for patch in patches + [None]:
            cur = {s: 'on' for s in others} | {p: 'off' for p in patches} | ({patch: 'on'} if patch else {})
            v = tot(ab.simulate_tc(P, cur, 1)[0])
            improved = True
            while improved:  # hill-climb on single and pair flips
                improved = False
                for a, b in itertools.combinations_with_replacement(others, 2):
                    t = dict(cur); 
                    for s in {a, b}: t[s] = 'off' if t[s] == 'on' else 'on'
                    w = tot(ab.simulate_tc(P, t, 1)[0])
                    if w > v: cur, v, improved = t, w, True
            off = [s for s in others if cur[s] == 'off']
            print(f'  {patch or "no patch":24} local max {v}  (switches off at max: {off})')
            best = max(best, (v, patch))
        print('  TRUE MAX', best, 'OK' if best[0] <= cap else 'OVER CAP')
        lean = tot(ab.simulate_tc(P, sw, 1)[0]); print('  lean/shipped', lean)
    else:
        prompts = {p['identifier']: p for p in P['prompts']}; nm = {k: v.get('name', '') for k, v in prompts.items()}
        order = [r['identifier'] for r in P['prompt_order'][1]['order']]
        patches = [p for p in order if nm[p].startswith('🩹')]
        g38 = [p for p in patches if '3.8' in nm[p]][0]; aio = [p for p in patches if 'All-In-One' in nm[p]][0]
        lcs = [p for p in order if nm[p].startswith('🧠 The Logic Core')]
        fixed_off = {p for p in order if nm[p].startswith(('🌳', '🌿')) or p == 'enhanceDefinitions'}
        others = [p for p in order if p not in patches and p not in lcs and p not in fixed_off and not prompts[p].get('marker')]
        best = (0, None)
        for pset in [[p] for p in patches] + [[aio, g38], []]:
            for lc in lcs:
                for imp in (False, True):
                    cur = set(others) | set(pset) | {lc}
                    def score(en):
                        r, _ = ab.simulate_cc(P, en, 1, impersonate=imp)
                        extra = ab.tokens(ab.render(P.get('impersonation_prompt') or '', {}, __import__('random').Random(1))) if imp else 0
                        return tot(r) + extra
                    v = score(cur); improved = True
                    while improved:
                        improved = False
                        for a in others:
                            t = cur ^ {a}
                            w = score(t)
                            if w > v: cur, v, improved = t, w, True
                    label = '+'.join(nm[p][15:] for p in pset) or 'no patch'
                    best = max(best, (v, label, nm[lc][-12:], imp))
            print(f'  {label:40} best over LC/imp {max(best[0] for _ in [0])}') if False else None
        print('  TRUE MAX', best, 'OK' if best[0] <= cap else 'OVER CAP')
        print('  shipped', totals.get('shipped default'))
