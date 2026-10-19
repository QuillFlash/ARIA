import json, sys, copy, io, contextlib, re
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
sys.path.insert(0, S + '/spec/frozen')
import aria_budget as ab
W = S + '/chibi/work/G5judge'
CC = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
TC = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", encoding='utf-8'))
g5 = json.load(open(sys.argv[1], encoding='utf-8'))

def run_cc(files):
    cc = copy.deepcopy(CC)
    by = {p['identifier']: p for p in cc['prompts']}
    for f in files:
        for pid, p in json.load(open(f, encoding='utf-8'))['prompts'].items():
            by[pid]['content'] = p['content']
    for pid, p in g5['prompts'].items():
        by[pid]['content'] = p['content']
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        totals, errors = ab.analyse_cc(cc)
    return totals, errors

def run_tc():
    tc = copy.deepcopy(TC)
    s = tc['sysprompt']['content']
    for sw, key in (('aria-time-place', 'time_place_block'), ('aria-fate', 'fate_block'), ('aria-bonds', 'bonds_block')):
        src = open(f'{W}/tc_src_{ {"time_place_block":"time","fate_block":"fate","bonds_block":"bonds"}[key] }.txt', encoding='utf-8').read()
        old = '{{#if .' + sw + '}}' + src + '{{/if}}'
        assert s.count(old) == 1, (sw, s.count(old))
        s = s.replace(old, '{{#if .' + sw + '}}' + g5['tc'][key] + '{{/if}}')
    for sw, key in (('aria-time-place', 'switch_comment_time_place'), ('aria-fate', 'switch_comment_fate'), ('aria-bonds', 'switch_comment_bonds')):
        m = re.search(r'\{\{//[^}]*?\}\}(?=\{\{\.' + re.escape(sw) + r' = )', s)
        s = s[:m.start()] + g5['tc'][key] + s[m.end():]
    tc['sysprompt']['content'] = s
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        totals, errors = ab.analyse_tc(tc)
    return totals, errors, tc

t, e = run_cc([])
print('CC snapshot + G5 only:', t, '\n  errors:', e)
fin = [f'{S}/chibi/final/G{i}.json' for i in (1, 2, 3, 4)]
t, e = run_cc(fin)
print('CC snapshot + G1-G4 finals + G5:', t, '\n  errors:', e)
t, e = run_cc(fin + [f'{S}/chibi/drafts/G6.json'])
print('CC snapshot + G1-G4 finals + G5 + G6 draft:', t, '\n  errors:', e)
# baseline errors of the pristine snapshot for comparison
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    t0, e0 = ab.analyse_cc(copy.deepcopy(CC))
print('CC pristine snapshot:', t0, '\n  errors:', e0)
t, e, tc = run_tc()
print('TC snapshot + G5:', t, '\n  errors:', e)
with contextlib.redirect_stdout(io.StringIO()):
    t0, e0 = ab.analyse_tc(copy.deepcopy(TC))
print('TC pristine snapshot:', t0, '\n  errors:', e0)
json.dump(tc, open(f'{W}/tc_swapped.json', 'w', encoding='utf-8'), ensure_ascii=False)
