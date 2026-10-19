#!/usr/bin/env python3
"""Swap the G4 draft into in-memory copies of the snapshot CC and TC and run the frozen checker on both."""
import copy, json, re, sys, io, contextlib
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab

SRC = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/src/'
CC = json.load(open(SRC + "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
TC = json.load(open(SRC + "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", encoding='utf-8'))
draft = json.load(open(sys.argv[1], encoding='utf-8'))


def quiet(fn, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = fn(*a)
    return r


def strip_comment_prefix(content):
    # source content = {{// ...}}{{trim}}\n body ; the body is what TC carries
    m = re.match(r'\{\{//.*?\}\}\{\{trim\}\}\n', content, flags=re.S)
    return content[m.end():] if m else content


base_cc_tot, base_cc_err = quiet(ab.analyse_cc, CC)
base_tc_tot, base_tc_err = quiet(ab.analyse_tc, TC)
print('BASELINE CC', base_cc_tot, base_cc_err)
print('BASELINE TC', base_tc_tot, base_tc_err)

cc = copy.deepcopy(CC)
by = {p['identifier']: p for p in cc['prompts']}
tc_sys = TC['sysprompt']['content']
for pid, new in draft['prompts'].items():
    old_body = strip_comment_prefix(by[pid]['content'])
    new_body = strip_comment_prefix(new['content'])
    by[pid]['content'] = new['content']
    n = tc_sys.count(old_body)
    if n != 1:
        print('TC: body of', new['name'], 'found', n, 'times'); sys.exit(1)
    tc_sys = tc_sys.replace(old_body, new_body)
tc = copy.deepcopy(TC)
tc['sysprompt']['content'] = tc_sys

cc_tot, cc_err = quiet(ab.analyse_cc, cc)
tc_tot, tc_err = quiet(ab.analyse_tc, tc)
print('SWAPPED CC', cc_tot, cc_err)
print('SWAPPED TC', tc_tot, tc_err)
new_cc = [e for e in cc_err if e not in base_cc_err]
new_tc = [e for e in tc_err if e not in base_tc_err]
print('NEW CC ERRORS:', new_cc)
print('NEW TC ERRORS:', new_tc)
