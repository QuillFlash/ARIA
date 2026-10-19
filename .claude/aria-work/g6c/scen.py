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

def run(label, extra_patches, drop=(), imp=False, show=('Logic Core', 'Gate', 'patch')):
    drop_ids = {pid for pid in prompts if any(d in name[pid] for d in drop)}
    ids = (no_patch - drop_ids) | {pid for pid in patches if any(e in name[pid] for e in extra_patches)}
    r, st = ab.simulate_cc(cc, ids, seed=1, impersonate=imp)
    print('=' * 100); print(label)
    tot = sum(ab.tokens(t) for t in r.values())
    print('total tokens', tot)
    lc = [k for k in r if name[k] == '🧠 The Logic Core']
    g = [k for k in r if name[k] == '🚪 Last-Mile Gate']
    if lc and 'Logic Core' in show:
        txt = r[lc[0]]
        i = txt.find('- Voice:'); j = txt.find('- Fresh:')
        print('--- plan (Voice .. Fresh)'); print(txt[i:j])
    if g and 'Gate' in show:
        txt = r[g[0]]
        i = txt.find('- Knows'); 
        print('--- gate (tail)'); print(txt[txt.find('- Secrets'):])
    for k in r:
        if name[k].startswith('🩹') and 'patch' in show:
            print('--- patch text:', name[k]); print(r[k])
    return r

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'glm':
        run('GLM + Flash Gate + Hold (all ON)', ['GLM'])
    elif which == 'ds_noflash':
        run('DeepSeek without Flash Gate', ['DeepSeek'], drop=['Flash Gate'])
    elif which == 'gem':
        run('Gemini AIO + 3.8 Flash', ['Gemini All-In-One', 'Gemini 3.8'])
    elif which == 'mimo':
        run('MiMo Flash + Flash Gate', ['MiMo V2.6 Flash'])
