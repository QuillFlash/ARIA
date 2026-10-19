#!/usr/bin/env python3
"""Mutation test for matrix.py: plant known JB bugs in in-memory copies of CC and TC and confirm the checks flag each."""
import copy, itertools, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/jbrev2')
import matrix as M  # noqa: E402

CC_GOOD, TC_GOOD = M.CC, M.TC
JB, IMP, MAIN, LC, TWIN = M.JB, M.IMP, 'main', M.LC, M.TWIN


def cc_mut(fn):
    cc = copy.deepcopy(CC_GOOD)
    P = {p['identifier']: p for p in cc['prompts']}
    fn(P)
    return cc


def tc_mut(fn):
    tc = copy.deepcopy(TC_GOOD)
    fn(tc['sysprompt'])
    return tc


def rep(pid, old, new, count=1):
    def f(P):
        assert old in P[pid]['content'], (pid, old)
        P[pid]['content'] = P[pid]['content'].replace(old, new, count)
    return f


def both(old, new):
    def f(P):
        for pid in (LC, TWIN):
            rep(pid, old, new)(P)
    return f


CC_MUTANTS = {
    'Impersonation Turn blank removed': rep(IMP, '{{setvar::ariaJb::}}', ''),
    'Main blank for ariaJb removed': rep(MAIN, '{{setvar::ariaJb::}}', ''),
    'ariaJbLines says 3': rep(JB, '{{setvar::ariaJbLines::2}}', '{{setvar::ariaJbLines::3}}'),
    'twin counter removed': rep(TWIN, '{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}', ''),
    'print after Fresh': both('{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}- Fresh: one or two details new to the chat, seen or heard and tied to an act; card features only when the scene turns to them.\n',
                              '- Fresh: one or two details new to the chat, seen or heard and tied to an act; card features only when the scene turns to them.\n{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}'),
    'condition dropped (prints without an adult mode)': lambda P: (rep(JB, '{{#if .ariaModeLine}}', '')(P), rep(JB, '}}{{/if}}', '}}')(P)),
    'literal backslash-n join': rep(JB, '.\n- Frank:', '.\\n- Frank:'),
    'stray newline rendered by the JB entry': rep(JB, '{{/if}}', '{{/if}}\n'),
    'per-turn macro in the JB entry': rep(JB, '{{trim}}\n', '{{trim}}\n{{roll::d20}}'),
}
TC_MUTANTS = {
    'TC stray newline before the block': lambda s: s.__setitem__('content', s['content'].replace('{{/if}}{{#if .aria-jailbreak}}', '{{/if}}\n{{#if .aria-jailbreak}}', 1)),
    'TC counter removed': lambda s: s.__setitem__('post_history', s['post_history'].replace('{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}', '', 1)),
    'TC block ignores ariaModeLine': lambda s: s.__setitem__('content', s['content'].replace('{{#if .aria-jailbreak}}{{#if .ariaModeLine}}', '{{#if .aria-jailbreak}}{{#if .aria-jailbreak}}', 1)),
    'TC Main blank removed': lambda s: s.__setitem__('content', s['content'].replace('{{setvar::ariaJb::}}', '', 1)),
}

# a compact but covering subset of the matrix
cc_cases = [(c, imp) for c in itertools.product([LC, TWIN, None], [True, False], ['', 'A', 'F'], [True, False], ['', 'fb'],
                                                [()], [False], [False]) for imp in (False, True)]
seq_cfg = list(itertools.product([LC, None], [True, False], ['', 'A'], [True, False], ['fb'], [()], [False], [False]))
seq_cases = [(a, i1, b, i2) for a in seq_cfg for b in seq_cfg for i1 in (False, True) for i2 in (False, True)
             if sum(x != y for x, y in zip(a, b)) <= 1]
tc_cases = list(itertools.product([True, False], [True, False], [True, False], [True, False], [True, False], [True], [True],
                                  [False], [False], [None], [True]))


def run_cc():
    n = sum(len(M.cc_case(x)[0]) for x in cc_cases) + sum(len(M.cc_seq(x)) for x in seq_cases)
    return n


def run_tc():
    return sum(len(M.tc_case(x)[0]) for x in tc_cases)


base_cc, base_tc = run_cc(), run_tc()
print(f'unmutated: CC {base_cc} problems, TC {base_tc} problems (expect 0)')
missed = []
for name, fn in CC_MUTANTS.items():
    M.CC = cc_mut(fn)
    M.P = {p['identifier']: p for p in M.CC['prompts']}
    n = run_cc()
    print(f'  CC mutant {name!r}: {n} problems flagged')
    if n == 0:
        missed.append(name)
M.CC, M.P = CC_GOOD, {p['identifier']: p for p in CC_GOOD['prompts']}
for name, fn in TC_MUTANTS.items():
    M.TC = tc_mut(fn)
    n = run_tc()
    print(f'  TC mutant {name!r}: {n} problems flagged')
    if n == 0:
        missed.append(name)
print('missed mutants:', missed or 'none')
