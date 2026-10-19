import json, re, sys, copy, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
CC = S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
draft = json.load(open(sys.argv[1] if len(sys.argv) > 1 else S + '/g6c/G6.check.json', encoding='utf-8'))
cc = json.load(open(CC, encoding='utf-8'))

def analyse(preset, label):
    prompts = {p['identifier']: p for p in preset['prompts']}
    order = preset['prompt_order'][1]['order']
    name = {pid: prompts[pid].get('name', pid) for pid in prompts}
    by_prefix = lambda *pre: {pid for pid in prompts if name[pid].startswith(pre)}
    patches = by_prefix('🩹')
    skip_all_on = by_prefix('🌳', '🌿') | {pid for pid in prompts if 'twin' in name[pid]} | {'enhanceDefinitions'} | patches
    no_patch = {row['identifier'] for row in order} - skip_all_on
    print('==', label)
    res = {}
    for pid in sorted(patches, key=lambda p: name[p]):
        r, _ = ab.simulate_cc(preset, no_patch | {pid}, seed=1)
        res[pid] = sum(ab.tokens(t) for t in r.values())
        print(f'  {res[pid]:5}  everything ON with {name[pid]}')
    r0, _ = ab.simulate_cc(preset, no_patch, seed=1)
    base = sum(ab.tokens(t) for t in r0.values())
    print(f'  {base:5}  everything ON without any patch (includes Flash Gate and Hold)')
    big = max(res, key=res.get)
    print('  largest:', name[big], res[big])
    return res, base

analyse(cc, 'SNAPSHOT (ARIA 1.0)')
cc2 = copy.deepcopy(cc)
for p in cc2['prompts']:
    if p['identifier'] in draft['prompts']:
        p['content'] = draft['prompts'][p['identifier']]['content']
analyse(cc2, 'WITH G6 DRAFT')
