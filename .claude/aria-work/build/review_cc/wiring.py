#!/usr/bin/env python3
"""Review check 1, 2 and 5 for Chibi CC: wiring against ARIA's current CC, content against the finals, JSON hygiene.

usage: python3 wiring.py [CHIBI_CC] [--cuts cuts.json]
"""
import json, sys
from pathlib import Path

REPO = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
W = REPO / '.claude/aria-work'
sys.path.insert(0, str(W / 'spec'))
from skeleton import skeleton  # noqa: E402

ARIA = REPO / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
CHIBI = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else \
    REPO / "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"
FATE = 'acc2177a-34e4-4941-93a2-b80bc18b8c91'
TIME = '5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa'
JB_ID = '05f6e90d-b30b-48d5-b2bf-26a6e45faffa'
LC = '15b770cf-6049-5f3b-b25d-be09728a65d5'
TW = '591b8c15-985e-59f1-8c90-59e7cae236ae'

problems = []


def bad(msg):
    problems.append(msg)
    print('FAIL ', msg)


def strip_comments(s):
    out, i = [], 0
    while i < len(s):
        if s.startswith('{{//', i):
            depth, j = 0, i
            while True:
                if s.startswith('{{', j):
                    depth += 1; j += 2
                elif s.startswith('}}', j):
                    depth -= 1; j += 2
                    if depth == 0:
                        break
                else:
                    j += 1
            i = j
            continue
        out.append(s[i]); i += 1
    return ''.join(out)


raw_a = open(ARIA, encoding='utf-8', newline='').read()
raw_c = open(CHIBI, encoding='utf-8', newline='').read()
A = json.loads(raw_a)
C = json.loads(raw_c)

# 5. hygiene
if json.dumps(C, ensure_ascii=False, indent=4) != raw_c:
    bad('Chibi CC does not round-trip as json.dumps(indent=4, ensure_ascii=False)')
if raw_c.endswith('\n'):
    bad('Chibi CC ends with a newline')
if json.dumps(A, ensure_ascii=False, indent=4) != raw_a:
    bad('ARIA CC does not round-trip (reference)')
if '\r' in raw_c:
    bad('CR characters in Chibi CC')
print('hygiene checked: round trip, no trailing newline, no CR')

# top-level keys
ka, kc = list(A.keys()), list(C.keys())
if ka != kc:
    bad(f'top-level key order differs: {ka} vs {kc}')
for k in ka:
    if k in ('prompts', 'prompt_order'):
        continue
    if A.get(k) != C.get(k):
        print(f'NOTE top-level {k!r} differs:\n   ARIA : {A.get(k)!r}\n   Chibi: {C.get(k)!r}')

# prompts
pa = A['prompts']; pc = C['prompts']
if [p['identifier'] for p in pa] != [p['identifier'] for p in pc]:
    bad('prompt identifiers or their order differ')
by_a = {p['identifier']: p for p in pa}
by_c = {p['identifier']: p for p in pc}
for p in pc:
    q = by_a.get(p['identifier'])
    if q is None:
        continue
    if list(p.keys()) != list(q.keys()):
        bad(f"{p['identifier']}: key order {list(p.keys())} vs ARIA {list(q.keys())}")
    for k in q:
        if k == 'content':
            continue
        if p.get(k) != q.get(k):
            bad(f"{p['identifier']} {p.get('name')}: {k} differs: {p.get(k)!r} vs ARIA {q.get(k)!r}")
    sa, sc = skeleton(q.get('content') or ''), skeleton(p.get('content') or '')
    if sa != sc:
        import difflib
        bad(f"{p['identifier']} {p.get('name')}: skeleton differs from ARIA's current CC")
        for line in difflib.unified_diff(sa, sc, 'ARIA', 'Chibi', lineterm='', n=1):
            print('      ', line)
print('prompts compared:', len(pc))

# prompt_order
if len(A['prompt_order']) != len(C['prompt_order']):
    bad('prompt_order length differs')
if A['prompt_order'][0] != C['prompt_order'][0]:
    bad('prompt_order[0] differs')
oa, oc = A['prompt_order'][1], C['prompt_order'][1]
if [k for k in oa] != [k for k in oc] or oa.get('character_id') != oc.get('character_id'):
    bad('prompt_order[1] keys differ')
ra, rc = oa['order'], oc['order']
if [r['identifier'] for r in ra] != [r['identifier'] for r in rc]:
    bad('prompt_order[1] identifiers differ')
for x, y in zip(ra, rc):
    want = False if x['identifier'] in (FATE, TIME) else x['enabled']
    if x['identifier'] in (FATE, TIME) and x['enabled'] is not True:
        print('NOTE ARIA ships', x['identifier'], 'off already')
    if y['enabled'] != want or list(y.keys()) != list(x.keys()):
        bad(f"order row {x['identifier']} {by_c[x['identifier']].get('name')}: enabled {y['enabled']} (want {want})")
print('prompt_order checked: Fate and Time off, everything else as ARIA')

# Logic Cores identical after comments
lc, tw = strip_comments(by_c[LC]['content']), strip_comments(by_c[TW]['content'])
lc_t, tw_t = lc.lstrip('\n'), tw.lstrip('\n')
if lc != tw:
    import difflib
    bad('the two Logic Cores differ after their comments')
    for line in difflib.unified_diff(lc.split('\n'), tw.split('\n'), 'LC', 'twin', lineterm='', n=0):
        print('      ', line)
else:
    print('Logic Cores identical after comments (exact)')

# JB entry
jb = by_c[JB_ID]['content']
if '\\n' in jb:
    bad('JB entry content contains a literal backslash-n')
body = strip_comments(jb)
import re
m = re.search(r'\{\{setvar::ariaJb::(.*?)\}\}\{\{/if\}\}$', body, re.S)
if not m or m.group(1).count('\n') != 1:
    bad('JB entry: ariaJb body does not hold two lines joined by a real newline')
else:
    print('JB entry: two lines joined by a real newline')

# regex scripts
if A.get('extensions') != C.get('extensions'):
    bad('extensions (regex scripts) differ from ARIA CC')
else:
    # byte-identical: both files round-trip, so equal order-preserving dumps mean equal raw text
    same = json.dumps(A['extensions'], ensure_ascii=False, indent=4) == json.dumps(C['extensions'], ensure_ascii=False, indent=4)
    print('extensions identical as objects;', 'raw identical (order kept)' if same else 'KEY ORDER DIFFERS')
    if not same:
        bad('extensions key order differs')

# 2. content vs finals
fin = {}
for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6'):
    d = json.loads((W / 'chibi/final' / f'{g}.json').read_text(encoding='utf-8'))
    for pid, p in d['prompts'].items():
        fin[pid] = p['content']
jbf = json.loads((W / 'chibi/final/JB.json').read_text(encoding='utf-8'))
fin[JB_ID] = (jbf['cc_comment'] + '{{trim}}\n{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::'
              + jbf['lines'][0] + '\n' + jbf['lines'][1] + '}}{{/if}}')
MB_OLD = '{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}\n{{trim}}'
MB_NEW = '{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}{{setvar::gemini38Patch::}}\n{{trim}}'
assert fin['main'].count(MB_OLD) == 1
fin['main'] = fin['main'].replace(MB_OLD, MB_NEW)
cuts = []
if '--cuts' in sys.argv:
    cuts = json.loads(open(sys.argv[sys.argv.index('--cuts') + 1], encoding='utf-8').read())
for c in cuts:
    t = fin[c['id']]
    assert t.count(c['old']) == 1, c
    fin[c['id']] = t.replace(c['old'], c['new'])
for p in pc:
    pid = p['identifier']
    if pid in fin:
        if (p.get('content') or '') != fin[pid]:
            bad(f"{pid} {p.get('name')}: content differs from its final (or recorded change)")
    else:
        if (p.get('content') or '') != (by_a[pid].get('content') or ''):
            bad(f"{pid} {p.get('name')}: not in the finals, and differs from ARIA CC")
not_in_fin = [by_c[p['identifier']].get('name') for p in pc if p['identifier'] not in fin]
print('prompts not covered by finals (must equal ARIA):', not_in_fin)
print()
print('RESULT:', 'OK' if not problems else f'{len(problems)} problem(s)')
