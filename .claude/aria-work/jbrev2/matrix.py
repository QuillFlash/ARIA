#!/usr/bin/env python3
"""Reviewer's behaviour matrix for the 🔓 Jailbreak, CC and TC, differential against HEAD with the checker's simulators.

Per configuration:
- every rendered entry equals HEAD's render of the same configuration, except: while the JB is active (JB on, an adult
  mode on, a Logic Core on, not Impersonate) the Logic Core gains exactly the approved lines directly before '- Fresh:'
  with its 'N dashed lines' raised by N_JB, and with Tags on the gate cue is raised by the same N_JB;
- 'N dashed lines' equals the '- ' lines before '- go', and the gate cue (Tags on) repeats it;
- the JB lines print exactly when the JB is active, right after Ledger (when present) and right before Fresh;
- no JB text outside the Logic Cores; the JB entry renders empty;
- cache: system-block entries render the same on a later turn with stale variables (compared with HEAD, so pre-existing
  issues are told apart).
Turn sequences: a second turn carrying the first turn's variables (as SillyTavern's chat variables persist) must render
exactly like a fresh second turn, for every switch of Adult, Freaky, JB, Logic Core, Tags and Impersonate between turns.
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


CC, CC0 = json.loads((ROOT / CCN).read_text(encoding='utf-8')), head(CCN)
TC, TC0 = json.loads((ROOT / TCN).read_text(encoding='utf-8')), head(TCN)
FIN = json.loads((S / 'jb/final.json').read_text(encoding='utf-8'))
JBL = [l.replace('{{user}}', 'User') for l in FIN['lines']]
NJB = len(JBL)
LABELS = tuple(f'- {x}:' for x in FIN['labels'])

P = {p['identifier']: p for p in CC['prompts']}
NM = {i: p['name'] for i, p in P.items()}
pid = lambda pre: next(i for i in P if i.startswith(pre))
JB, FREAKY, TAGS = pid('05f6e90d'), pid('4537b57d'), pid('303f26f5')
LC, TWIN, GATE, IMP = pid('15b770cf'), pid('591b8c15'), 'jailbreak', pid('379e3c22')
FATE, BONDS, FLASH, HOLD, TIME = pid('acc2177a'), pid('5506d699'), pid('2e3e7f63'), pid('dc8b1acb'), pid('5dcccd11')
PATCH = {NM[i].split(': ', 1)[1]: i for i in P if NM[i].startswith('🩹')}
SHIPPED = {r['identifier'] for r in CC['prompt_order'][1]['order'] if r['enabled']}
BASE = (SHIPPED - {LC, TWIN, TAGS, FATE, BONDS, FLASH, HOLD, IMP}) | {TIME, pid('2a2e12d0'), pid('b7b6ab7f'), pid('939286fd'), IMP}
PATCH_SETS = [()] + [(PATCH[k],) for k in sorted(PATCH)] + [(PATCH['Gemini 3.8 Flash'], PATCH['Gemini All-In-One'])]
CC_SETTERS = set(re.findall(r'\{\{setvar::([\w-]+)::', '\n'.join(p.get('content') or '' for p in CC['prompts'])))
STALE = {v: 'stale value from an earlier turn' for v in CC_SETTERS | {'logicCoreLines'}}
STALE['logicCoreLines'] = '42'
COUNT = re.compile(r'(then|writes) (\d+) dashed lines')
CUE = re.compile(r'Begin with <thinking>, then (\d+) dashed lines')


def bump(text, k, which=COUNT):
    return which.sub(lambda m: m.group(0).replace(m.group(m.lastindex), str(int(m.group(m.lastindex)) + k)), text, count=1)


def plan_lines(text):
    lines = text.split('\n')
    if '- go' not in lines:
        return None, None
    dashed = [l for l in lines[:lines.index('- go')] if l.startswith('- ')]
    m = COUNT.search(text)
    return (int(m.group(2)) if m else None), dashed


def cc_enabled(c, with_jb=True):
    lc, tags, adult, jb, world, patches, hold, flash = c
    en = set(BASE) | set(patches)
    for flag, i in ((lc, lc), (tags, TAGS), ('A' in adult, 'nsfw'), ('F' in adult, FREAKY), ('f' in world, FATE),
                    ('b' in world, BONDS), (hold, HOLD), (flash, FLASH), (jb and with_jb, JB)):
        if flag and i:
            en.add(i)
    return en


def cc_checks(c, imp, r, r0, st, label):
    lc, tags, adult, jb = c[:4]
    errs = []
    active = bool(jb and adult and lc and not imp)
    if JB in r and r[JB] != '':
        errs.append('JB entry renders text')
    if set(r) - {JB} != set(r0):
        errs.append('entry set differs from HEAD')
    for k, h in r0.items():
        w = r.get(k)
        if active and k == lc:
            exp = bump(h, NJB)
            exp = exp.replace('\n- Fresh:', '\n' + '\n'.join(JBL) + '\n- Fresh:', 1) if exp.count('\n- Fresh:') == 1 else None
            if w != exp:
                errs.append('Logic Core is not HEAD + JB lines before Fresh + count')
        elif active and k == GATE and tags:
            if w != bump(h, NJB, CUE):
                errs.append('gate cue is not HEAD + JB count')
        elif w != h:
            errs.append(f'{NM.get(k, k)} differs from HEAD')
    if lc and lc in r:
        n, dashed = plan_lines(r[lc])
        if dashed is None or n != len(dashed):
            errs.append(f'plan claims {n}, has {dashed and len(dashed)} dashed lines')
        else:
            has = [l for l in dashed if l.startswith(LABELS)]
            if active and has != JBL:
                errs.append(f'JB lines wrong: {has}')
            elif active:
                names = [l.split(':', 1)[0][2:] for l in dashed]
                i = names.index(FIN['labels'][0])
                after_ok = names[i:i + NJB + 1] == FIN['labels'] + ['Fresh']
                before = names[i - 1]
                before_ok = before == 'Ledger' if 'Ledger' in names else before in ('Move', 'Fate', 'Bonds', 'Tally')
                if not (after_ok and before_ok):
                    errs.append(f'JB position {names}')
            elif has:
                errs.append('JB lines while inactive')
            if tags:
                g = CUE.search(r.get(GATE, ''))
                if not g or int(g.group(1)) != n:
                    errs.append(f'gate cue {g and g.group(1)} vs plan {n}')
    outside = '\n'.join(v for k, v in r.items() if k not in (LC, TWIN))
    if any(lab in outside for lab in LABELS) or 'adult-fiction game master' in outside:
        errs.append('JB text outside the Logic Cores')
    if st.get('ariaJb') and not (jb and adult):
        errs.append('ariaJb set although JB off or no adult mode')
    return errs, active


def cc_case(args):
    c, imp = args
    label = f'lc={NM.get(c[0], None) and NM[c[0]][:22]} tags={c[1]} adult={c[2] or "-"} jb={c[3]} world={c[4] or "-"} patch={[NM[p][14:] for p in c[5]]} hold={c[6]} flash={c[7]} imp={imp}'
    en, en0 = cc_enabled(c), cc_enabled(c, with_jb=False)
    r, st = ab.simulate_cc(CC, en, seed=1, impersonate=imp)
    r0, _ = ab.simulate_cc(CC0, en0, seed=1, impersonate=imp)
    errs, active = cc_checks(c, imp, r, r0, st, label)
    # cache: a later turn with stale variables and other dice; compare with HEAD's behaviour for the same config
    r2, _ = ab.simulate_cc(CC, en, seed=99, state=STALE, impersonate=imp)
    r02, _ = ab.simulate_cc(CC0, en0, seed=99, state={k: v for k, v in STALE.items() if k not in ('ariaJb', 'ariaJbLines')}, impersonate=imp)
    sysw = {k for k in r if (P[k].get('injection_position') or 0) == 0 and r[k] != r2.get(k)}
    sysh = {k for k in r0 if (P[k].get('injection_position') or 0) == 0 and r0[k] != r02.get(k)}
    for k in sysw - sysh:
        errs.append(f'cache (new): {NM[k]} differs between turns')
    pre = [f'cache (pre-existing at HEAD): {NM[k]}' for k in sorted(sysh)]
    return [f'{e} | {label}' for e in errs], active, pre


def cc_seq(args):
    """Two turns; turn 2 carries turn 1's variables. Turn 2 must equal a fresh render of its config."""
    c1, imp1, c2, imp2 = args
    _, st1 = ab.simulate_cc(CC, cc_enabled(c1), seed=1, impersonate=imp1)
    r2, _ = ab.simulate_cc(CC, cc_enabled(c2), seed=2, state=st1, impersonate=imp2)
    f2, _ = ab.simulate_cc(CC, cc_enabled(c2), seed=2, impersonate=imp2)
    _, st10 = ab.simulate_cc(CC0, cc_enabled(c1, False), seed=1, impersonate=imp1)
    r20, _ = ab.simulate_cc(CC0, cc_enabled(c2, False), seed=2, state=st10, impersonate=imp2)
    f20, _ = ab.simulate_cc(CC0, cc_enabled(c2, False), seed=2, impersonate=imp2)
    bad_w = {k for k in f2 if r2.get(k) != f2[k]}
    bad_h = {k for k in f20 if r20.get(k) != f20[k]}
    out = []
    for k in sorted(bad_w - bad_h):
        out.append(f'stale state changes {NM[k]} on turn 2 | {c1} imp={imp1} -> {c2} imp={imp2}')
    jb_lines_2 = [l for k in (LC, TWIN) if k in r2 for l in r2[k].split('\n') if l.startswith(LABELS)]
    want = bool(c2[3] and c2[2] and c2[0] and not imp2)
    if bool(jb_lines_2) != want:
        out.append(f'turn 2 JB lines {bool(jb_lines_2)} expected {want} | {c1} imp={imp1} -> {c2} imp={imp2}')
    return out


# ---------------------------------------------------------------- TC
TCP = TC['sysprompt']
SW = dict(ab.SWITCH.findall(TCP['content']))
TC_PATCHES = sorted(s for s in SW if s.startswith('aria-patch'))
CL_OLD = 'with no Fate, Bonds, Ledger or Layers line.'
CL_NEW = 'with no Fate, Bonds, Ledger, Layers, %s line.' % ' or '.join(FIN['labels'])
TC_SETTERS = set(re.findall(r'\{\{setvar::([\w-]+)::', TCP['content'] + TCP['post_history']))
TC_STALE = {v: 'stale value from an earlier turn' for v in TC_SETTERS} | {'logicCoreLines': '42'}


def tc_ov(c, with_jb=True):
    lc, tags, adult, freaky, jb, fate, bonds, hold, flash, patch, others = c
    on = lambda b: 'on' if b else 'off'
    ov = {s: (on(others) if s not in ('aria-time-place',) else 'on') for s in SW if not s.startswith('aria-patch')}
    ov |= {p: 'off' for p in TC_PATCHES}
    ov |= {'aria-logic-core': on(lc), 'aria-thinking-tags': on(tags), 'aria-adult': on(adult), 'aria-freaky': on(freaky),
           'aria-fate': on(fate), 'aria-bonds': on(bonds), 'aria-character-hold': on(hold), 'aria-flash-gate': on(flash)}
    if with_jb:
        ov['aria-jailbreak'] = on(jb)
    else:
        ov.pop('aria-jailbreak', None)
    if patch:
        ov[patch] = 'on'
    return ov


def tc_case(c):
    lc, tags, adult, freaky, jb = c[:5]
    label = f'lc={lc} tags={tags} adult={adult} freaky={freaky} jb={jb} fate={c[5]} bonds={c[6]} hold={c[7]} flash={c[8]} patch={c[9]} others={c[10]}'
    errs = []
    r, st = ab.simulate_tc(TC, tc_ov(c), 1)
    r0, _ = ab.simulate_tc(TC0, tc_ov(c, False), 1)
    active = bool(jb and (adult or freaky) and lc)
    if r['System Prompt'] != r0['System Prompt']:
        errs.append('System Prompt differs from HEAD')
    h = r0['Post-History']
    if lc:
        if h.count(CL_OLD) != 1:
            errs.append('closing sentence anchor missing at HEAD')
        h = h.replace(CL_OLD, CL_NEW, 1)
    if active:
        h = bump(h, NJB)
        h = h.replace('\n- Fresh:', '\n' + '\n'.join(JBL) + '\n- Fresh:', 1)
        if tags:
            h = bump(h, NJB, CUE)
    if r['Post-History'] != h:
        errs.append('Post-History is not HEAD + the expected change')
    if lc:
        n, dashed = plan_lines(r['Post-History'])
        if dashed is None or n != len(dashed):
            errs.append(f'plan claims {n}, has {dashed and len(dashed)}')
        else:
            has = [l for l in dashed if l.startswith(LABELS)]
            if active and has != JBL:
                errs.append(f'JB lines wrong {has}')
            if not active and has:
                errs.append('JB lines while inactive')
            if active and has == JBL:
                names = [l.split(':', 1)[0][2:] for l in dashed]
                i = names.index(FIN['labels'][0])
                if names[i:i + NJB + 1] != FIN['labels'] + ['Fresh'] or ('Ledger' in names and names[i - 1] != 'Ledger'):
                    errs.append(f'JB position {names}')
            g = CUE.search(r['Post-History'])
            if tags and (not g or int(g.group(1)) != n):
                errs.append('cue mismatch')
    if any(lab in r['System Prompt'] for lab in LABELS):
        errs.append('JB text in the System Prompt')
    if not lc and any(lab in r['Post-History'] for lab in LABELS):
        errs.append('JB text with the core off')
    r2, _ = ab.simulate_tc(TC, tc_ov(c), 99, state=TC_STALE)
    r02, _ = ab.simulate_tc(TC0, tc_ov(c, False), 99, state={k: v for k, v in TC_STALE.items() if k not in ('ariaJb', 'ariaJbLines')})
    if r2['System Prompt'] != r['System Prompt'] and r02['System Prompt'] == r0['System Prompt']:
        errs.append('cache (new): System Prompt differs between turns')
    # stale state must not reach the post-history either (the blanks run first)
    if r2['Post-History'] != ab.simulate_tc(TC, tc_ov(c), 99)[0]['Post-History']:
        errs.append('stale state reaches the Post-History')
    return [f'{e} | {label}' for e in errs], active


def main():
    t = time.time()
    lcs = [LC, TWIN, None]
    cc_cases = [(c, imp) for c in itertools.product(lcs, [True, False], ['', 'A', 'F', 'AF'], [True, False],
                                                    ['', 'f', 'b', 'fb'], PATCH_SETS, [False, True], [False, True])
                for imp in (False, True)]
    seq_cfg = list(itertools.product([LC, TWIN, None], [True, False], ['', 'A', 'F'], [True, False], ['fb'], [()], [False], [False]))
    seq_cases = [(a, i1, b, i2) for a in seq_cfg for b in seq_cfg for i1 in (False, True) for i2 in (False, True)
                 if sum(x != y for x, y in zip(a, b)) <= 2]
    tc_cases = list(itertools.product([True, False], [True, False], [True, False], [True, False], [True, False], [True, False],
                                      [True, False], [True, False], [True, False], [None] + TC_PATCHES, [True]))
    tc_cases += list(itertools.product([True], [True, False], [True, False], [True, False], [True, False], [True], [True],
                                       [False], [False], [None, 'aria-patch-glm'], [False]))
    with mp.Pool(4) as pool:
        cc_res = pool.map(cc_case, cc_cases, chunksize=64)
        seq_res = pool.map(cc_seq, seq_cases, chunksize=64)
        tc_res = pool.map(tc_case, tc_cases, chunksize=32)
    cc_errs = [e for es, _, _ in cc_res for e in es]
    pre = sorted({p for _, _, ps in cc_res for p in ps})
    print(f'CC: {len(cc_cases)} cases, {sum(a for _, a, _ in cc_res)} with the JB active, {len(cc_errs)} problems')
    for e in cc_errs[:20]:
        print('   ', e)
    print(f'    pre-existing cache differences also present at HEAD (not from the JB): {pre}')
    seq_errs = [e for es in seq_res for e in es]
    print(f'CC turn sequences: {len(seq_cases)} pairs, {len(seq_errs)} problems')
    for e in seq_errs[:20]:
        print('   ', e)
    tc_errs = [e for es, _ in tc_res for e in es]
    print(f'TC: {len(tc_cases)} cases, {sum(a for _, a in tc_res)} with the JB active, {len(tc_errs)} problems')
    for e in tc_errs[:20]:
        print('   ', e)
    print(f'{time.time() - t:.0f}s')
    sys.exit(1 if cc_errs or seq_errs or tc_errs else 0)


if __name__ == '__main__':
    main()
