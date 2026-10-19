import json, sys, copy, random, re, itertools
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
sys.path.insert(0, S + '/spec/frozen')
import aria_budget as ab
W = S + '/chibi/work/G5judge'
g5 = json.load(open(f'{W}/cand.json', encoding='utf-8'))
CC = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
cc = copy.deepcopy(CC)
by = {p['identifier']: p for p in cc['prompts']}
for f in [f'{S}/chibi/final/G{i}.json' for i in (1, 2, 3, 4)] + [f'{S}/chibi/final/G6.json']:
    for pid, p in json.load(open(f, encoding='utf-8'))['prompts'].items():
        by[pid]['content'] = p['content']
for pid, p in g5['prompts'].items():
    by[pid]['content'] = p['content']
order = [r['identifier'] for r in cc['prompt_order'][1]['order']]
name = {pid: by[pid].get('name', pid) for pid in by}
TIME, FATE, BONDS = '5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa', 'acc2177a-34e4-4941-93a2-b80bc18b8c91', '5506d699-fb00-49ce-a631-73b3f0036eae'
LC = '15b770cf-6049-5f3b-b25d-be09728a65d5'
GATE = [pid for pid in by if name[pid].startswith('🚪')][0]
base = {r['identifier'] for r in cc['prompt_order'][1]['order']} - {pid for pid in by if name[pid].startswith(('🌳', '🌿', '🩹')) or 'twin' in name[pid]} - {'enhanceDefinitions'}
problems = 0
for t, f, b in itertools.product([0, 1], repeat=3):
    en = set(base) - {TIME, FATE, BONDS}
    en |= ({TIME} if t else set()) | ({FATE} if f else set()) | ({BONDS} if b else set())
    for imp in (False, True):
        r, st = ab.simulate_cc(cc, en, seed=3, impersonate=imp)
        for pid in (TIME, FATE, BONDS):
            if pid in r:
                txt = r[pid]
                bad = [m for m in ('  ', ' \n', '\n\n', '{{', '}}', ' .', ' ,', ' ;') if m in txt]
                if bad or txt != txt.strip():
                    problems += 1; print('PROBLEM', name[pid], t, f, b, imp, bad)
        if not imp and LC in r:
            lc = r[LC]
            ledger = [l for l in lc.split('\n') if l.startswith(('- Fate:', '- Bonds:', '- Ledger:'))]
            gate = [l for l in r[GATE].split('\n') if l.startswith(('- Ledger:', 'Fate dice'))]
            head = re.search(r'then (\d+) dashed lines', lc)
            dashed = len([l for l in lc.split('\n') if l.startswith('- ') and l != '- go'])
            if head and int(head.group(1)) != dashed:
                problems += 1; print('COUNT MISMATCH', t, f, b, head.group(1), dashed)
            print(f'T{t} F{f} B{b}: plan {[l[:14] for l in ledger]} gate {[l[:22] for l in gate]} count {head.group(1) if head else "-"}={dashed}')
print('problems:', problems)
# show a full render of the three modules once
r, st = ab.simulate_cc(cc, base, seed=3)
for pid in (TIME, FATE, BONDS):
    print('=====', name[pid]); print(r[pid])
