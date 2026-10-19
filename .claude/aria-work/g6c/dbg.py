import json, re, sys, copy, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
CC = S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
draft = json.load(open(S + '/g6c/G6.check.json', encoding='utf-8'))
cc = json.load(open(CC, encoding='utf-8'))
for p in cc['prompts']:
    if p['identifier'] in draft['prompts']:
        p['content'] = draft['prompts'][p['identifier']]['content']
prompts = {p['identifier']: p for p in cc['prompts']}
order = cc['prompt_order'][1]['order']
name = {pid: prompts[pid].get('name', pid) for pid in prompts}
by_prefix = lambda *pre: {pid for pid in prompts if name[pid].startswith(pre)}
patches = by_prefix('🩹')
skip_all_on = by_prefix('🌳', '🌿') | {pid for pid in prompts if 'twin' in name[pid]} | {'enhanceDefinitions'} | patches
no_patch = {row['identifier'] for row in order} - skip_all_on
which = sys.argv[1]
pid = [p for p in patches if which in name[p]][0]
r, st = ab.simulate_cc(cc, no_patch | {pid}, seed=1)
for k, t in r.items():
    print(f'{ab.tokens(t):5} {name[k]}')
print()
lc = [k for k in r if name[k] == '🧠 The Logic Core'][0]
print(r[lc])
print('-----')
g = [k for k in r if name[k] == '🚪 Last-Mile Gate'][0]
print(r[g])
