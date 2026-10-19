import json, re, sys, copy, random, io, contextlib
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
CC = S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
cc = json.load(open(CC, encoding='utf-8'))
def load(g):
    return json.load(open(f'{S}/chibi/drafts/{g}.json', encoding='utf-8'))
def swap(preset, draft):
    n = 0
    for p in preset['prompts']:
        if p['identifier'] in draft['prompts']:
            p['content'] = draft['prompts'][p['identifier']]['content']; n += 1
    return n
groups = sys.argv[1:] or ['G1', 'G2', 'G3', 'G4']
cc2 = copy.deepcopy(cc)
for g in groups:
    d = load(g) if g != 'G6' else json.load(open(S + '/g6c/G6.check.json', encoding='utf-8'))
    print(g, 'swapped', swap(cc2, d))
prompts = {p['identifier']: p for p in cc2['prompts']}
order = cc2['prompt_order'][1]['order']
name = {pid: prompts[pid].get('name', pid) for pid in prompts}
by_prefix = lambda *pre: {pid for pid in prompts if name[pid].startswith(pre)}
patches = by_prefix('🩹')
skip_all_on = by_prefix('🌳', '🌿') | {pid for pid in prompts if 'twin' in name[pid]} | {'enhanceDefinitions'} | patches
no_patch = {row['identifier'] for row in order} - skip_all_on
res = {}
for pid in patches:
    r, _ = ab.simulate_cc(cc2, no_patch | {pid}, seed=1)
    res[name[pid]] = sum(ab.tokens(t) for t in r.values())
big = max(res, key=res.get)
print('everything ON, largest patch', big, res[big])
r, _ = ab.simulate_cc(cc2, no_patch | {[p for p in patches if name[p] == big][0]}, seed=1)
for pid, t in r.items():
    print(f'  {ab.tokens(t):5} {name[pid]}')
