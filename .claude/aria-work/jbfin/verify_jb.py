#!/usr/bin/env python3
"""Render-level verification of the JB (Role and Frank) in CC and TC, using the checker's own simulators."""
import itertools, json, re, subprocess, sys, time
from pathlib import Path

ROOT = Path("/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA")
S = ROOT / ".claude/aria-work"
sys.path.insert(0, str(ROOT / 'tools'))
import aria_budget as ab
from aria_budget import simulate_cc, simulate_tc, tokens

CCP = ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
TCP = ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
fin = json.loads((S / 'jb/final.json').read_text(encoding='utf-8'))
JBL = [l.replace('{{user}}', 'User') for l in fin['lines']]   # the way the checker renders {{user}}


def head(p):
    out = subprocess.run(['git', '-C', str(ROOT), 'show', 'HEAD:' + p.name], capture_output=True)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout.decode('utf-8'))


cc, cc0 = json.loads(CCP.read_text(encoding='utf-8')), head(CCP)
tc, tc0 = json.loads(TCP.read_text(encoding='utf-8')), head(TCP)

fails = []
counts = {}


def ok(group, cond, msg):
    counts[group] = counts.get(group, 0) + 1
    if not cond:
        fails.append(f'[{group}] {msg}')


def plan(text):
    """(dashed lines before '- go', the N the text claims, all lines before '- go')."""
    lines = text.split('\n')
    gi = next(i for i, l in enumerate(lines) if l.strip() == '- go')
    dashed = [l for l in lines[:gi] if l.startswith('- ')]
    m = re.search(r'(\d+) dashed lines', text)
    return dashed, int(m.group(1)), lines[:gi]


def check_plan(group, label, text, jb_expected, adult_mode):
    dashed, claimed, _ = plan(text)
    ok(group, len(dashed) == claimed, f'{label}: text claims {claimed} dashed lines but {len(dashed)} lines start "- " before "- go"')
    names = [re.match(r'- ([^:]+):', l).group(1) if re.match(r'- ([^:]+):', l) else '?' for l in dashed]
    ok(group, '?' not in names, f'{label}: a plan line has no label: {names}')
    has_role, has_frank = 'Role' in names, 'Frank' in names
    if jb_expected:
        ok(group, has_role and has_frank, f'{label}: Role/Frank lines missing; plan labels {names}')
        if has_role and has_frank:
            ri = names.index('Role')
            ok(group, names[ri + 1] == 'Frank', f'{label}: Frank does not directly follow Role: {names}')
            ok(group, dashed[ri] == JBL[0] and dashed[ri + 1] == JBL[1], f'{label}: JB line text differs from the approved lines')
            ok(group, names[ri + 2] == 'Fresh', f'{label}: the line after Frank is not Fresh: {names}')
            if 'Ledger' in names:
                ok(group, names.index('Ledger') == ri - 1, f'{label}: Ledger is not directly before Role: {names}')
            ok(group, ri > names.index('Move'), f'{label}: Role comes before Move: {names}')
    else:
        ok(group, not has_role and not has_frank, f'{label}: JB line printed although it should not: {names}')
    ok(group, len(set(names)) == len(names), f'{label}: duplicate labels {names}')
    return claimed


# ================================================================ CC
prompts = {p['identifier']: p for p in cc['prompts']}
nm = {i: p['name'] for i, p in prompts.items()}
pid8 = lambda s: next(i for i in prompts if i.startswith(s))
ADULT, FREAKY, JB = 'nsfw', pid8('4537b57d'), pid8('05f6e90d')
TAGS, LC, TWIN = pid8('303f26f5'), pid8('15b770cf'), pid8('591b8c15')
FATE, BONDS, FLASH, HOLD = pid8('acc2177a'), pid8('5506d699'), pid8('2e3e7f63'), pid8('dc8b1acb')
patches = {i for i in prompts if nm[i].startswith('🩹')}
byp = {nm[i].split(': ', 1)[-1]: i for i in patches}
shipped = {r['identifier'] for r in cc['prompt_order'][1]['order'] if r['enabled']}
strip = {LC, TWIN, TAGS, ADULT, FREAKY, JB, FATE, BONDS, FLASH, HOLD} | patches
assert 'GLM' in byp and 'DeepSeek' in byp and 'Gemini All-In-One' in byp and 'MiMo V2.6 Flash' in byp, byp
EXTRAS = {
    'none': set(),
    'GLM': {byp['GLM']},
    'DeepSeek+Flash+Hold': {byp['DeepSeek'], FLASH, HOLD},
    'Gemini-AIO': {byp['Gemini All-In-One']},
    'MiMoFlash+Hold': {byp['MiMo V2.6 Flash'], HOLD},
}


def cc_enabled(lc, tags, adult, freaky, jb, fate, bonds, extra):
    en = set(shipped) - strip
    en |= {lc}
    for flag, i in ((tags, TAGS), (adult, ADULT), (freaky, FREAKY), (jb, JB), (fate, FATE), (bonds, BONDS)):
        if flag:
            en.add(i)
    return en | EXTRAS[extra]


t0 = time.time()
n_cases = 0
for lc, tags, (adult, freaky), jb, fate, bonds, extra, imp in itertools.product(
        (LC, TWIN), (False, True), ((0, 0), (1, 0), (1, 1), (0, 1)), (False, True), (False, True), (False, True), EXTRAS, (False, True)):
    n_cases += 1
    en = cc_enabled(lc, tags, adult, freaky, jb, fate, bonds, extra)
    label = f'CC {"twin" if lc == TWIN else "assistant"} | tags {"on" if tags else "off"} | adult {adult} freaky {freaky} jb {int(jb)} | fate {int(fate)} bonds {int(bonds)} | {extra} | {"impersonate" if imp else "normal"}'
    r, st = simulate_cc(cc, en, 1, impersonate=imp)
    mode = bool(adult or freaky)
    jb_expected = jb and mode and not imp
    claimed = check_plan('CC plan', label, r[lc], jb_expected, mode)
    full = '\n'.join(r.values())
    if not jb_expected:
        ok('CC no JB text', 'adult-fiction game master' not in full and 'sex stays between adults' not in full and 'Role:' not in full and 'Frank:' not in full,
           f'{label}: JB text leaked into a render')
    # the other Logic Core is off, so its text must not be in the render
    ok('CC one core', (TWIN if lc == LC else LC) not in r, f'{label}: both Logic Cores rendered')
    # with Tags on, the Logic Core hands the gate a one-line cue that repeats the count: it must be the same N
    gate = pid8('jailbrea')
    cue = re.findall(r'(\d+) dashed lines', r[gate])
    if tags:
        ok('CC gate cue count', cue == [str(claimed)], f'{label}: the gate cue says {cue}, the plan has {claimed} dashed lines')
    else:
        ok('CC gate cue count', cue == [], f'{label}: the gate names a dashed-line count with Tags off: {cue}')
    # differential: the same case with the JB entry off
    if jb:
        en_off = en - {JB}
        r_off, st_off = simulate_cc(cc, en_off, 1, impersonate=imp)
        c_off = plan(r_off[lc])[1]
        ok('CC count delta', claimed - c_off == (len(JBL) if jb_expected else 0), f'{label}: N with JB {claimed} vs without {c_off}')
        # nothing but the JB entry and the Logic Core's plan differ
        norm = lambda t: re.sub(r'\d+ dashed lines', 'N dashed lines', t)
        diff_ids = {i for i in r if norm(r[i]) != norm(r_off.get(i, ''))} - {JB}
        ok('CC isolation', diff_ids <= {lc}, f'{label}: JB changed other entries beyond the count: {[nm[i] for i in diff_ids]}')
        if not jb_expected:
            ok('CC JB-inert identical', all(r[i] == r_off[i] for i in r_off) and r.get(JB, '') == '',
               f'{label}: the JB entry changed a render although it should be inert (JB entry text: {r.get(JB)!r})')
    else:
        # JB off: byte-identical to HEAD, which has no JB at all
        r0, _ = simulate_cc(cc0, en, 1, impersonate=imp)
        ok('CC identical to HEAD (JB off)', r == r0, f'{label}: differs from HEAD although the JB is off: {[nm[i] for i in r if r[i] != r0.get(i)]}')
    # stale-state cache check: relative entries identical across turns
    if jb and not imp and lc == LC and extra == 'none' and fate and bonds:
        stale = {v: 'stale value from an earlier turn' for v in ('ariaJb', 'ariaJbLines', 'ariaModeLine', 'logicCoreLines')}
        a, _ = simulate_cc(cc, en, 1)
        b, _ = simulate_cc(cc, en, 99, state=stale)
        for i in a:
            if (prompts[i].get('injection_position') or 0) == 0:
                ok('CC cache (system block)', a[i] == b.get(i), f'{label}: {nm[i]} differs between turns')
print(f'CC matrix: {n_cases} cases in {time.time() - t0:.0f}s')

# the two Logic Cores are identical after their comments
tail = lambda t: t.split('}}{{trim}}', 1)[1]
ok('CC cores identical', tail(prompts[LC]['content']) == tail(prompts[TWIN]['content']), 'the two Logic Cores differ after their comments')
ok('CC cores identical', prompts[LC]['content'].count('{{trim}}') == prompts[TWIN]['content'].count('{{trim}}'), 'trim count differs')

# ================================================================ TC
system = tc['sysprompt']['content']
shipped_tc = dict(ab.SWITCH.findall(system))
tc_patches = sorted(s for s in shipped_tc if s.startswith('aria-patch'))
assert 'aria-patch-glm' in tc_patches
TC_EXTRAS = {
    'none': {},
    'glm': {'aria-patch-glm': 'on'},
    'deepseek+flash+hold': {'aria-patch-deepseek': 'on', 'aria-flash-gate': 'on', 'aria-character-hold': 'on'},
    'kimi': {'aria-patch-kimi-qwen': 'on'},
    'mimoflash+hold': {'aria-patch-mimo-flash': 'on', 'aria-character-hold': 'on'},
}
t0 = time.time()
n_tc = 0
for tags, (adult, freaky), jb, fate, bonds, extra in itertools.product(
        ('on', 'off'), ((0, 0), (1, 0), (1, 1), (0, 1)), ('on', 'off'), ('on', 'off'), ('on', 'off'), TC_EXTRAS):
    n_tc += 1
    ov = {k: 'off' for k in shipped_tc if k.startswith('aria-patch')} | {
        'aria-logic-core': 'on', 'aria-thinking-tags': tags, 'aria-adult': 'on' if adult else 'off', 'aria-freaky': 'on' if freaky else 'off',
        'aria-jailbreak': jb, 'aria-fate': fate, 'aria-bonds': bonds} | TC_EXTRAS[extra]
    label = f'TC tags {tags} | adult {adult} freaky {freaky} jb {jb} | fate {fate} bonds {bonds} | {extra}'
    r, st = simulate_tc(tc, ov, 1)
    mode = bool(adult or freaky)
    jb_expected = jb == 'on' and mode
    claimed = check_plan('TC plan', label, r['Post-History'], jb_expected, mode)
    full = '\n'.join(r.values())
    if not jb_expected:
        ok('TC no JB text', 'adult-fiction game master' not in full and 'sex stays between adults' not in full and '- Role:' not in full and '- Frank:' not in full,
           f'{label}: JB text leaked into a render')
    else:
        ok('TC JB text only in the plan', r['System Prompt'].count('adult-fiction game master') == 0, f'{label}: JB text rendered in the System Prompt')
    ok('TC closing sentence', "plan only User's move, with no Fate, Bonds, Ledger, Layers, Role or Frank line." in r['Post-History'], f'{label}: closing sentence missing')
    if jb == 'on':
        ov_off = dict(ov) | {'aria-jailbreak': 'off'}
        r_off, _ = simulate_tc(tc, ov_off, 1)
        c_off = plan(r_off['Post-History'])[1]
        ok('TC count delta', claimed - c_off == (len(JBL) if jb_expected else 0), f'{label}: N with JB {claimed} vs without {c_off}')
        ok('TC isolation', r['System Prompt'] == r_off['System Prompt'], f'{label}: the JB changed the System Prompt')
        if not jb_expected:
            ok('TC JB-inert identical', r == r_off, f'{label}: the JB switch changed a render although no mode line is set')
    else:
        r0, _ = simulate_tc(tc0, {k: v for k, v in ov.items() if k != 'aria-jailbreak'}, 1)
        NEW_END, OLD_END = 'with no Fate, Bonds, Ledger, Layers, Role or Frank line.', 'with no Fate, Bonds, Ledger or Layers line.'
        r_norm = {k: v.replace(NEW_END, OLD_END) for k, v in r.items()}
        ok('TC identical to HEAD (JB off)', r_norm == r0, f'{label}: differs from HEAD although the JB is off, beyond the closing sentence')
# TC with aria-logic-core off: no plan, no JB lines anywhere
for adult, jb in itertools.product(('on', 'off'), ('on', 'off')):
    ov = dict(shipped_tc) | {'aria-logic-core': 'off', 'aria-adult': adult, 'aria-jailbreak': jb}
    r, _ = simulate_tc(tc, ov, 1)
    ok('TC core off', 'adult-fiction game master' not in '\n'.join(r.values()), f'TC core off, adult {adult}, jb {jb}: JB text rendered')
    r0, _ = simulate_tc(tc0, {k: v for k, v in ov.items() if k != 'aria-jailbreak'}, 1)
    ok('TC core off', r == r0, f'TC core off, adult {adult}, jb {jb}: differs from HEAD')
# TC cache: the System Prompt must not change between turns, with the JB on
stale = {v: 'stale value from an earlier turn' for v in ('ariaJb', 'ariaJbLines', 'ariaModeLine', 'logicCoreLines')}
ov = {k: 'on' for k in shipped_tc if not k.startswith('aria-patch')} | {k: 'off' for k in shipped_tc if k.startswith('aria-patch')}
a, _ = simulate_tc(tc, ov, 1)
b, _ = simulate_tc(tc, ov, 99, state=stale)
ok('TC cache', a['System Prompt'] == b['System Prompt'], 'TC System Prompt renders differently between turns with everything on')
print(f'TC matrix: {n_tc} cases in {time.time() - t0:.0f}s')

# ================================================================ report
print()
for g, n in counts.items():
    bad = sum(1 for f in fails if f.startswith(f'[{g}]'))
    print(f'{"PASS" if not bad else "FAIL"}  {g}: {n - bad}/{n} checks')
print()
if fails:
    print(f'{len(fails)} FAILURES, first 25:')
    for f in fails[:25]:
        print('  ', f)
    sys.exit(1)
print('all checks passed')
