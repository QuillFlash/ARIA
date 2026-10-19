#!/usr/bin/env python3
"""est.py [g5.json]: estimate the final Chibi fully-ON total. Swaps G1-G4 (+ optional G5 draft) into the snapshot CC,
computes the checker's 'everything ON', then replaces the (uncompressed) G6 cost by its targets and adds the JB plan lines."""
import json, sys, copy, random, re
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
SRC = W + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"

def load():
    return json.load(open(SRC, encoding='utf-8'))

def swap(preset, draftfile):
    d = json.load(open(draftfile, encoding='utf-8'))
    by = {p['identifier']: p for p in preset['prompts']}
    n = 0
    for k, v in d['prompts'].items():
        for pid in by:
            if pid == k or pid.startswith(k) or k.startswith(pid):
                by[pid]['content'] = v['content']; n += 1
    return n

def everything_on(preset, blank_g6=False):
    prompts = {p['identifier']: p for p in preset['prompts']}
    name = {pid: prompts[pid].get('name', pid) for pid in prompts}
    order = preset['prompt_order'][1]['order']
    patches = {pid for pid in prompts if name[pid].startswith('🩹')}
    skip_all_on = {pid for pid in prompts if name[pid].startswith(('🌳', '🌿')) or 'twin' in name[pid]} | {'enhanceDefinitions'} | patches
    no_patch = {row['identifier'] for row in order} - skip_all_on
    def patch_cost(pid):
        r, _ = ab.simulate_cc(preset, no_patch | {pid}, seed=1)
        return sum(ab.tokens(t) for t in r.values())
    largest = max(patches, key=patch_cost)
    all_on = no_patch | {largest}
    if blank_g6:
        # drop the G6 modules entirely: the patches (already out), the Flash Gate and Character Hold
        for pid in list(all_on):
            if name[pid].startswith(('🔦', '🧷')) or pid == largest:
                all_on.discard(pid)
    r, _ = ab.simulate_cc(preset, all_on, seed=1)
    return sum(ab.tokens(t) for t in r.values()), name[largest], {name[k]: ab.tokens(v) for k, v in r.items()}

if __name__ == '__main__':
    cc = load()
    for i in (1, 2, 3, 4):
        swap(cc, W + f'/chibi/drafts/G{i}.json')
    for f in sys.argv[1:]:
        print('G5 swap:', swap(cc, f))
    full, largest, per = everything_on(cc)
    base, _, per2 = everything_on(cc, blank_g6=True)
    g6 = full - base
    print(f'everything ON with G6 at source size: {full} (largest patch {largest})')
    print(f'without the G6 modules (patch, Flash Gate, Hold): {base}  -> G6 source cost {g6}')
    print('G6 at its ceilings: 407, JB plan lines: 55')
    print('ESTIMATED FINAL (G1-G4 drafts, this G5, G6 at ceilings, JB at ceiling):', base + 407 + 55)
    for k in ('⏰ Time & Place', '🎲 Fate & Chekhov Ledger', '🥰 Bonds Lite', '🧠 The Logic Core', '🚪 Last-Mile Gate'):
        print(f'   {k}: {per2.get(k)}')
