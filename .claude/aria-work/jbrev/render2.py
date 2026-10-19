#!/usr/bin/env python3
"""Reviewer's render matrix for the 🔓 Jailbreak in CC and TC, against HEAD, with the checker's own simulators.

For every configuration the working-tree render must equal HEAD's render of the same configuration, except that when
the JB should be active (JB on, an adult mode on, a Logic Core on, not an Impersonate turn) the Logic Core gains exactly
the two approved lines directly before '- Fresh:', its line count grows by 2 and the gate's plan cue says the same.
Also: the dashed-line count equals the '- ' lines before '- go'; system-block entries render the same on a later turn
with stale variables.
"""
import itertools, json, multiprocessing as mp, re, subprocess, sys, time
from pathlib import Path

ROOT = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
S = ROOT / '.claude/aria-work'
sys.path.insert(0, str(ROOT / 'tools'))
import aria_budget as ab  # noqa: E402

CCN = "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
TCN = "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"


def head(name):
    return json.loads(subprocess.run(['git', '-C', str(ROOT), 'show', f'HEAD:{name}'], capture_output=True, check=True).stdout.decode())


CC = json.loads((ROOT / CCN).read_text(encoding='utf-8'))
CC0 = head(CCN)
TC = json.loads((ROOT / TCN).read_text(encoding='utf-8'))
TC0 = head(TCN)
FIN = json.loads((S / 'jb/final.json').read_text(encoding='utf-8'))
JBL = [l.replace('{{user}}', 'User') for l in FIN['lines']]
INSERT = '\n' + '\n'.join(JBL) + '\n- Fresh:'

prompts = {p['identifier']: p for p in CC['prompts']}
nm = {i: p['name'] for i, p in prompts.items()}
pid = lambda pre: next(i for i in prompts if i.startswith(pre))
JB, FREAKY, TAGS = pid('05f6e90d'), pid('4537b57d'), pid('303f26f5')
LC, TWIN, GATE = pid('15b770cf'), pid('591b8c15'), 'jailbreak'
FATE, BONDS, FLASH, HOLD = pid('acc2177a'), pid('5506d699'), pid('2e3e7f63'), pid('dc8b1acb')
PATCH = {nm[i].split(': ', 1)[1]: i for i in prompts if nm[i].startswith('🩹')}
shipped = {r['identifier'] for r in CC['prompt_order'][1]['order'] if r['enabled']}
BASE = (shipped - {LC, TWIN, TAGS, FATE, BONDS, FLASH, HOLD}) | {pid('5dcccd11'), pid('2a2e12d0'), pid('b7b6ab7f')}
PATCH_SETS = [[]] + [[PATCH[k]] for k in sorted(PATCH) if k != 'Gemini 3.8 Flash'] + [[PATCH['Gemini 3.8 Flash'], PATCH['Gemini All-In-One']]]
SETTERS = set(re.findall(r'\{\{setvar::([\w-]+)::', '\n'.join(p.get('content') or '' for p in CC['prompts'])))
# gemini38Patch is left out: at HEAD nothing blanks it, so a stale value always reaches Gemini All-In-One (pre-existing,
# reported separately, not part of the JB work)
STALE = {v: 'stale value from an earlier turn' for v in (SETTERS | {'ariaJb', 'ariaJbLines'}) - {'gemini38Patch'}}
COUNT = re.compile(r'(then|writes) (\d+) dashed lines')


def plan_check(text):
    """Return (claimed N, dashed lines before '- go', labels) or raise."""
    lines = text.split('\n')
    gi = lines.index('- go')
    dashed = [l for l in lines[:gi] if l.startswith('- ')]
    m = COUNT.search(text)
    return int(m.group(2)), dashed


def bump(text, k):
    """Raise the first 'N dashed lines' in text by k."""
    return COUNT.sub(lambda m: f'{m.group(1)} {int(m.group(2)) + k} dashed lines', text, count=1)


def cc_case(args):
    lc, tags, adult, jb, world, patches, hold, flash, imp = args
    errs = []
    en = set(BASE) | set(patches)
    if lc: en.add(lc)
    if tags: en.add(TAGS)
    if 'A' in adult: en.add('nsfw')
    if 'F' in adult: en.add(FREAKY)
    if 'f' in world: en.add(FATE)
    if 'b' in world: en.add(BONDS)
    if hold: en.add(HOLD)
    if flash: en.add(FLASH)
    en0 = set(en)
    if jb: en.add(JB)
    label = f'lc={lc and nm[lc][:20]} tags={tags} adult={adult} jb={jb} world={world} patch={[nm[p][14:] for p in patches]} hold={hold} flash={flash} imp={imp}'
    r, st = ab.simulate_cc(CC, en, seed=1, impersonate=imp)
    r0, _ = ab.simulate_cc(CC0, en0, seed=1, impersonate=imp)
    active = bool(jb and adult and lc and not imp)
    if JB in r and r[JB] != '':
        errs.append(f'JB entry renders text: {r[JB]!r} | {label}')
    if set(r) - {JB} != set(r0):
        errs.append(f'rendered entry set differs from HEAD | {label}')
    for k in r0:
        w, h = r.get(k), r0[k]
        if active and k == lc:
            exp = bump(h, 2)
            if exp.count('\n- Fresh:') != 1:
                errs.append(f'Fresh anchor count {exp.count(chr(10) + "- Fresh:")} | {label}')
            exp = exp.replace('\n- Fresh:', INSERT)
            if w != exp:
                errs.append(f'Logic Core is not HEAD + 2 JB lines before Fresh + count+2 | {label}')
        elif active and k == GATE and tags:
            if w != bump(h, 2):
                errs.append(f'gate cue is not HEAD count + 2 | {label}')
        elif w != h:
            errs.append(f'{nm[k]} differs from HEAD | {label}')
    if lc and lc in r:
        n, dashed = plan_check(r[lc])
        if n != len(dashed):
            errs.append(f'claims {n} dashed lines, has {len(dashed)} | {label}')
        has = [l for l in dashed if l.startswith(('- Role:', '- Frank:'))]
        if active and has != JBL:
            errs.append(f'JB lines wrong: {has} | {label}')
        if not active and has:
            errs.append(f'JB lines printed while inactive | {label}')
        if tags:
            g = re.search(r'Begin with <thinking>, then (\d+) dashed lines', r.get(GATE, ''))
            if not g or int(g.group(1)) != n:
                errs.append(f'gate cue {g and g.group(1)} vs plan {n} | {label}')
        if active:
            names = [re.match(r'- ([^:]+):', l).group(1) for l in dashed]
            i = names.index('Role')
            if names[i + 1:i + 3] != ['Frank', 'Fresh'] or ('Ledger' in names and names[i - 1] != 'Ledger'):
                errs.append(f'JB position {names} | {label}')
            if names.index('Move') > i:
                errs.append(f'JB before Move {names} | {label}')
    all_text = '\n'.join(v for k, v in r.items() if k not in (LC, TWIN))
    if 'Role:' in all_text or 'Frank:' in all_text:
        errs.append(f'JB text outside the Logic Cores | {label}')
    if jb and st.get('ariaJb') and not adult:
        errs.append(f'ariaJb set without an adult mode | {label}')
    # cache: a later turn, different dice, stale variables
    if jb:
        r2, _ = ab.simulate_cc(CC, en, seed=99, state=STALE, impersonate=imp)
        for k in r:
            if (prompts[k].get('injection_position') or 0) == 0 and r[k] != r2.get(k):
                errs.append(f'cache: {nm[k]} differs between turns | {label}')
    return errs, active, (len(r[lc]) if lc and lc in r else 0)


TCP = TC['sysprompt']
SWITCHES = dict(ab.SWITCH.findall(TCP['content']))
TC_PATCHES = [s for s in SWITCHES if s.startswith('aria-patch')]
CL_OLD = 'with no Fate, Bonds, Ledger or Layers line.'
CL_NEW = 'with no Fate, Bonds, Ledger, Layers, Role or Frank line.'
TC_SETTERS = set(re.findall(r'\{\{setvar::([\w-]+)::', TCP['content'] + TCP['post_history']))
TC_STALE = {v: 'stale value from an earlier turn' for v in TC_SETTERS}


def tc_case(args):
    lc, tags, adult, freaky, jb, fate, bonds, hold, flash, patch = args
    errs = []
    onoff = lambda b: 'on' if b else 'off'
    ov = {s: 'on' for s in SWITCHES if not s.startswith('aria-patch')} | {p: 'off' for p in TC_PATCHES}
    ov.update({'aria-logic-core': onoff(lc), 'aria-thinking-tags': onoff(tags), 'aria-adult': onoff(adult),
               'aria-freaky': onoff(freaky), 'aria-jailbreak': onoff(jb), 'aria-fate': onoff(fate),
               'aria-bonds': onoff(bonds), 'aria-character-hold': onoff(hold), 'aria-flash-gate': onoff(flash)})
    if patch:
        ov[patch] = 'on'
    ov0 = {k: v for k, v in ov.items() if k != 'aria-jailbreak'}
    label = f'lc={lc} tags={tags} adult={adult} freaky={freaky} jb={jb} fate={fate} bonds={bonds} hold={hold} flash={flash} patch={patch}'
    r, st = ab.simulate_tc(TC, ov, 1)
    r0, _ = ab.simulate_tc(TC0, ov0, 1)
    active = bool(jb and (adult or freaky) and lc)
    if r['System Prompt'] != r0['System Prompt']:
        errs.append(f'System Prompt differs from HEAD | {label}')
    h = r0['Post-History']
    if lc:
        if h.count(CL_OLD) != 1:
            errs.append(f'closing sentence anchor | {label}')
        h = h.replace(CL_OLD, CL_NEW)
    if active:
        h = bump(h, 2)
        if h.count('\n- Fresh:') != 1:
            errs.append(f'Fresh anchor | {label}')
        h = h.replace('\n- Fresh:', INSERT)
        if tags:
            # the plan cue at the very end
            h = re.sub(r'(Begin with <thinking>, then )(\d+)( dashed lines)', lambda m: f'{m.group(1)}{int(m.group(2)) + 2}{m.group(3)}', h)
    if r['Post-History'] != h:
        errs.append(f'Post-History is not HEAD + expected change | {label}')
    if lc:
        n, dashed = plan_check(r['Post-History'])
        if n != len(dashed):
            errs.append(f'claims {n} dashed lines, has {len(dashed)} | {label}')
        has = [l for l in dashed if l.startswith(('- Role:', '- Frank:'))]
        if active and has != JBL:
            errs.append(f'JB lines wrong {has} | {label}')
        if not active and has:
            errs.append(f'JB lines while inactive | {label}')
        cue = re.search(r'Begin with <thinking>, then (\d+) dashed lines', r['Post-History'])
        if tags and (not cue or int(cue.group(1)) != n):
            errs.append(f'cue mismatch | {label}')
    if 'Role:' in r['System Prompt'] or 'Frank:' in r['System Prompt']:
        errs.append(f'JB text in the System Prompt | {label}')
    if not lc and ('Role:' in r['Post-History'] or 'Frank:' in r['Post-History']):
        errs.append(f'JB text with the core off | {label}')
    if jb:
        r2, _ = ab.simulate_tc(TC, ov, 99, state=TC_STALE)
        if r2['System Prompt'] != r['System Prompt']:
            errs.append(f'cache: System Prompt differs between turns | {label}')
    return errs, active, len(r['Post-History'])


def main():
    t = time.time()
    cc_cases = list(itertools.product([LC, TWIN, None], [True, False], ['', 'A', 'F', 'AF'], [True, False],
                                      ['', 'f', 'b', 'fb'], PATCH_SETS, [False, True], [False, True], [False, True]))
    tc_cases = list(itertools.product([True, False], [True, False], [True, False], [True, False], [True, False],
                                      [True, False], [True, False], [True, False], [True, False], [None] + TC_PATCHES))
    with mp.Pool(4) as pool:
        cc_res = pool.map(cc_case, cc_cases, chunksize=64)
        tc_res = pool.map(tc_case, tc_cases, chunksize=32)
    for name, cases, res in (('CC', cc_cases, cc_res), ('TC', tc_cases, tc_res)):
        errs = [e for es, _, _ in res for e in es]
        act = sum(1 for _, a, _ in res if a)
        kinds = {}
        for e in errs:
            k = e.split(' | ')[0]
            kinds[k] = kinds.get(k, 0) + 1
        for k, v in sorted(kinds.items(), key=lambda kv: -kv[1])[:10]:
            print(f'   kind x{v}: {k}')
        print(f'{name}: {len(cases)} cases, {act} with the JB active, {len(errs)} problems; longest Logic Core render {max(x for _, _, x in res)} chars')
        for e in errs[:15]:
            print('   ', e)
    print(f'{time.time() - t:.0f}s')


if __name__ == '__main__':
    main()
