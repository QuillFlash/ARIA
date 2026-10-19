#!/usr/bin/env python3
"""Global estimate for the G5 judge: snapshot CC with G1-G4 finals, a G5 file, a G6 file and a stand-in Chibi JB (55 tokens),
run through the frozen checker. usage: global_est.py G5.json [G6.json]"""
import json, sys, copy, io, contextlib
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
sys.path.insert(0, S + '/spec/frozen')
import aria_budget as ab
CC = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
JB_LINES = "- Role: " + "x" * 98 + "\n- Frank: " + "y" * 103   # stand-in, 55 tokens
HOLD = 'dc8b1acb-9a7e-5a43-b9aa-38e7b70662a3'
FREAKY = '4537b57d-e002-586d-a4c9-233740c51605'


def load(p):
    return json.load(open(p, encoding='utf-8'))


def build_cc(g5, g6):
    cc = copy.deepcopy(CC)
    by = {p['identifier']: p for p in cc['prompts']}
    files = [f'{S}/chibi/final/G{i}.json' for i in (1, 2, 3, 4)] + [g5] + ([g6] if g6 else [])
    for f in files:
        for pid, p in load(f)['prompts'].items():
            by[pid]['content'] = p['content']
    jid = 'jb-standin'
    jb = dict(by[HOLD])
    jb.update(identifier=jid, name='🔓 Jailbreak (needs Adult Context)',
              content='{{// stand-in}}{{trim}}\n{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::' + JB_LINES + '}}{{/if}}')
    i = [p['identifier'] for p in cc['prompts']].index(FREAKY)
    cc['prompts'].insert(i + 1, jb)
    order = cc['prompt_order'][1]['order']
    k = [r['identifier'] for r in order].index(FREAKY)
    order.insert(k + 1, {'identifier': jid, 'enabled': False})
    # Chibi ships Fate and Time & Place OFF
    for row in order:
        nm = by.get(row['identifier'], {}).get('name', '')
        if nm.startswith(('🎲', '⏰')):
            row['enabled'] = False
    return cc


if __name__ == '__main__':

    args = [a for a in sys.argv[1:] if a != "-v"]
    g5 = args[0]
    g6 = args[1] if len(args) > 1 else f'{S}/chibi/drafts/G6.json'
    cc = build_cc(g5, g6)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        totals, errors = ab.analyse_cc(cc)
    print('G5:', g5)
    print('G6:', g6)
    if '-v' in sys.argv:
        print(buf.getvalue())
    for k, v in totals.items():
        print(f'  {k:22} {v}')
    errs = [e for e in errors if 'over the' not in e]
    print('  errors:', errs or 'none (budget errors ignored)')
    # JB stand-in is only printed if the Logic Core counts it: the snapshot Logic Cores don't have the JB counter/print,
    # but G3 final does. Report whether ariaJb printed.
