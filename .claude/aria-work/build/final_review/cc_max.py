import json, sys, random
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools')
import aria_budget as ab
for f in sys.argv[1:]:
    P = json.load(open(R + '/' + f)); cap = ab.budget_for(f)
    prompts = {p['identifier']: p for p in P['prompts']}; nm = {k: v.get('name', '') for k, v in prompts.items()}
    order = [r['identifier'] for r in P['prompt_order'][1]['order']]
    patches = [p for p in order if nm[p].startswith('🩹')]
    g38 = [p for p in patches if '3.8' in nm[p]][0]; aio = [p for p in patches if 'All-In-One' in nm[p]][0]
    lcs = [p for p in order if nm[p].startswith('🧠 The Logic Core')]
    impt = [p for p in order if nm[p].startswith('🪞')][0]
    fixed_off = {p for p in order if nm[p].startswith(('🌳', '🌿')) or p == 'enhanceDefinitions'}
    others = [p for p in order if p not in patches and p not in lcs and p not in fixed_off and not prompts[p].get('marker') and p != impt]
    imp_set = ab.tokens(ab.render(P.get('impersonation_prompt') or '', {}, random.Random(1)))
    best = []
    for pset in [[p] for p in patches] + [[aio, g38], []]:
        for lc in lcs:
            for imp in (False, True):
                def score(en):
                    r, _ = ab.simulate_cc(P, en | {impt}, 1, impersonate=imp)
                    return sum(ab.tokens(t) for t in r.values()) + (imp_set if imp else 0)
                cur = set(others) | set(pset) | {lc}; v = score(cur); improved = True
                while improved:
                    improved = False
                    for a in others:
                        w = score(cur ^ {a})
                        if w > v: cur, v, improved = cur ^ {a}, w, True
                best.append((v, '+'.join(nm[p][15:] for p in pset) or 'none', 'twin' if 'twin' in nm[lc] else 'plain', 'imp' if imp else 'normal', [nm[p] for p in set(others) - cur]))
    best.sort(reverse=True)
    print('===', f[38:], 'cap', cap)
    for b in best[:6]: print('  ', b)
    print('  OK' if best[0][0] <= cap else '  OVER CAP')
