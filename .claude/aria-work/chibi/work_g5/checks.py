import json, sys, io, contextlib
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
SRC = W + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
SRCTC = W + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
draft = json.load(open(sys.argv[1], encoding='utf-8'))

def swap(preset, d):
    by = {p['identifier']: p for p in preset['prompts']}
    n = 0
    for k, v in d['prompts'].items():
        for pid in by:
            if pid == k or pid.startswith(k) or k.startswith(pid):
                by[pid]['content'] = v['content']; n += 1
    return n

def quiet(fn, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = fn(*a)
    return r

# 1. CC snapshot + G5 only
cc = json.load(open(SRC, encoding='utf-8'))
print('CC snapshot unchanged:', quiet(ab.analyse_cc, cc)[1] or 'no errors')
swap(cc, draft)
tot, err = quiet(ab.analyse_cc, cc)
print('CC snapshot + G5:', tot, '|', err or 'no errors')
# 2. + G1-G4
cc2 = json.load(open(SRC, encoding='utf-8'))
for i in (1, 2, 3, 4):
    swap(cc2, json.load(open(W + f'/chibi/drafts/G{i}.json', encoding='utf-8')))
swap(cc2, draft)
tot, err = quiet(ab.analyse_cc, cc2)
print('CC snapshot + G1-G4 + G5:', tot, '|', err)
# 3. TC: replace the three blocks in the raw system prompt text
tc = json.load(open(SRCTC, encoding='utf-8'))
sp = tc['sysprompt']['content']
def seg(start, end):
    a = sp.index(start) + len(start); b = sp.index(end, a); return a, b
tsrc = open('tc_time_draft.txt', encoding='utf-8').read()
fsrc = open('tc_fate_draft.txt', encoding='utf-8').read()
bsrc = open('tc_bonds_draft.txt', encoding='utf-8').read()
new = sp
for (s0, e0), repl in (((('{{#if .aria-time-place}}'), '{{/if}}{{#if .aria-fate}}'), tsrc),
                       ((('{{#if .aria-fate}}'), '{{/if}}{{#if .aria-bonds}}'), fsrc),
                       ((('{{#if .aria-bonds}}'), '{{/if}}{{#if .aria-patch-glm}}'), bsrc)):
    a = new.index(s0) + len(s0); b = new.index(e0, a)
    new = new[:a] + repl + new[b:]
tc['sysprompt']['content'] = new
tot, err = quiet(ab.analyse_tc, tc)
print('TC snapshot + G5 blocks:', tot, '|', err or 'no errors')
tc0 = json.load(open(SRCTC, encoding='utf-8'))
print('TC snapshot unchanged:', quiet(ab.analyse_tc, tc0)[0])
