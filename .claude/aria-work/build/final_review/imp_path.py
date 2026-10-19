import json, sys, random
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools')
import aria_budget as ab
f = sys.argv[1]
P = json.load(open(R + '/' + f))
prompts = {p['identifier']: p for p in P['prompts']}; nm = {k: v.get('name', '') for k, v in prompts.items()}
order = [r['identifier'] for r in P['prompt_order'][1]['order']]
patches = [p for p in order if nm[p].startswith('🩹')]
glm = [p for p in patches if 'GLM' in nm[p]][0]
lcs = [p for p in order if nm[p].startswith('🧠 The Logic Core')]
fixed_off = {p for p in order if nm[p].startswith(('🌳', '🌿')) or p == 'enhanceDefinitions'}
others = [p for p in order if p not in patches and p not in lcs and p not in fixed_off and not prompts[p].get('marker')]
imp_set = ab.tokens(ab.render(P.get('impersonation_prompt') or '', {}, random.Random(1)))
for lc in lcs:
    en = set(others) | {glm, lc}
    n, _ = ab.simulate_cc(P, en, 1)
    i, _ = ab.simulate_cc(P, en, 1, impersonate=True)
    print(nm[lc], 'normal', sum(ab.tokens(t) for t in n.values()), 'imp', sum(ab.tokens(t) for t in i.values()), '+setting', imp_set)
    for pid in order:
        a, b = n.get(pid), i.get(pid)
        if a != b:
            print(f'   {nm[pid][:40]:40} normal {ab.tokens(a or "")} imp {ab.tokens(b or "")}  trig={prompts[pid].get("injection_trigger")} pos={prompts[pid].get("injection_position")}')
# what the checker's all_on is
with __import__('contextlib').redirect_stdout(__import__('io').StringIO()):
    pass
print('in others but not in checker no_patch?')
skip = {p for p in prompts if nm[p].startswith(('🌳', '🌿')) or 'twin' in nm[p]} | {'enhanceDefinitions'} | set(patches)
no_patch = set(order) - skip
print([nm[p] for p in set(others) - no_patch], [nm[p] for p in no_patch - set(others)])
