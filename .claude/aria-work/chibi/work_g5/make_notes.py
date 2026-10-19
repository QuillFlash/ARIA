#!/usr/bin/env python3
import sys, importlib
sys.path.insert(0, '.')
import menus as M, final_texts as F, t
importlib.reload(M)

def cost_restore(i, mod, old, new):
    base = t.n({"Fate": M.FATE, "Bonds": M.BONDS, "Time": M.TIME}[mod])
    x = M.apply({"Fate": M.FATE, "Bonds": M.BONDS, "Time": M.TIME}[mod], old, new)
    return t.n(x) - base

def cost_cut(i, mod, old, new):
    base = t.n({"Fate": M.FATE, "Bonds": M.BONDS, "Time": M.TIME}[mod])
    x = M.apply({"Fate": M.FATE, "Bonds": M.BONDS, "Time": M.TIME}[mod], old, new)
    return base - t.n(x)

def q(s):
    return '«' + s.replace('\n', '⏎') + '»'

restore_lines = []
for i, mod, desc, old, new in M.RESTORE:
    c = cost_restore(i, mod, old, new)
    restore_lines.append(f"{i} (+{c:.0f}) {desc}: replace {q(old)} with {q(new)}")
cut_lines = []
cum = 0.0
for i, mod, desc, old, new in M.CUT:
    c = cost_cut(i, mod, old, new)
    cum += c
    cut_lines.append(f"{i} (-{c:.1f}, cumulative -{cum:.1f}) {desc}: replace {q(old)} with {q(new)}")

import json, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab, est as E, build_final as B, variants as V
importlib.reload(B); importlib.reload(V)
def tkn(text):
    return round(len(ab.render(text, {}, random.Random(1))) / 4)
prim = B.assemble()
TIME = tkn(prim['5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa']['content']); FATE = tkn(prim['acc2177a-34e4-4941-93a2-b80bc18b8c91']['content']); BONDS = tkn(prim['5506d699-fb00-49ce-a631-73b3f0036eae']['content'])
fl = V.pack(V.FLOOR_TIME, V.FLOOR_FATE, V.FLOOR_BONDS)['prompts']; fu = V.pack(V.FULL_TIME, V.FULL_FATE, V.FULL_BONDS)['prompts']
LT, LF, LB = (tkn(fl[k]['content']) for k in ('5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa', 'acc2177a-34e4-4941-93a2-b80bc18b8c91', '5506d699-fb00-49ce-a631-73b3f0036eae'))
FT, FF, FB = (tkn(fu[k]['content']) for k in ('5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa', 'acc2177a-34e4-4941-93a2-b80bc18b8c91', '5506d699-fb00-49ce-a631-73b3f0036eae'))
def est_total(pack):
    cc = E.load()
    for i in (1, 2, 3, 4):
        E.swap(cc, E.W + f'/chibi/drafts/G{i}.json')
    by = {p['identifier']: p for p in cc['prompts']}
    for k, v in pack.items():
        by[k]['content'] = v['content']
    base, _, _ = E.everything_on(cc, blank_g6=True)
    return base + 407 + 55
EST, ESTL, ESTF = est_total(prim), est_total(fl), est_total(fu)
K9 = round(sum(cost_cut(*c[:1], *c[1:2], *c[3:5]) for c in M.CUT[:9]))
vals = dict(TIME=TIME, FATE=FATE, BONDS=BONDS, TOTAL=TIME+FATE+BONDS+88+24, OVER=TIME+FATE+BONDS+88+24-605, FT=FT, FF=FF, FB=FB, FTOT=FT+FF+FB+112,
            LT=LT, LF=LF, LB=LB, LTOT=LT+LF+LB+112, EST=EST, ESTL=ESTL, ESTF=ESTF, K9=K9, ESTK=EST-K9)
head = open('notes_head.txt', encoding='utf-8').read().strip()
for k, v in vals.items():
    head = head.replace('@' + k + '@C', f'{v:,}').replace('@' + k + '@', str(v))
tail = open('notes_tail.txt', encoding='utf-8').read().strip()
notes = head + "\n\n" + "RESTORE MENU (tokens added; ⏎ marks a line break; each item is a replacement in the primary's text, listed in the order I would restore them when there is room. Items that share an anchor are alternatives or merge by hand: F1m or F1 and F2 all insert before the ledger line, F3s is the short form of F3, F6b a part of F6, B1 a part of B2, and F4 plus F15 read «Deferred expires at 6 (a MINOR may revive one; deferred twice returns as MAJOR), each end leaving Residue.»). " + \
    "\n".join(restore_lines) + "\n\n" + \
    "CUT MENU (tokens saved by removing text from the primary; lowest regret first; every item is a real mechanic or tester fix, only the cheapest to lose; K1 to K9 give -44, which puts the estimate at about 2,999). " + \
    "\n".join(cut_lines) + "\n\n" + tail
open('notes.txt', 'w', encoding='utf-8').write(notes)
print(len(notes), 'characters')
