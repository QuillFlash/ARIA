import json, sys, re, random, itertools
from collections import Counter
sys.path.insert(0, '.')
import xed, aria_budget as ab
C, T, prompts, nm, order, MAP = xed.C, xed.T, xed.prompts, xed.nm, xed.order, xed.MAP
def pid(pre): return [p for p in prompts if nm[p].startswith(pre)]
LCP = [p for p in prompts if nm[p] == '🧠 The Logic Core'][0]; LCT = [p for p in prompts if nm[p] == '🧠 The Logic Core (system-role twin)'][0]
GATE = pid('🚪')[0]; IMPT = pid('🪞')[0]; RR = [p for p in prompts if nm[p].startswith('Reduce')][0]
PATCH = {'none': [], 'claude': pid('🩹 Model Patch: Claude'), 'g38': pid('🩹 Model Patch: Gemini 3.8'), 'aio': pid('🩹 Model Patch: Gemini All'),
         'aio+g38': pid('🩹 Model Patch: Gemini 3.8') + pid('🩹 Model Patch: Gemini All'), 'glm': pid('🩹 Model Patch: GLM'), 'kimi': pid('🩹 Model Patch: Kimi'),
         'mimopro': pid('🩹 Model Patch: MiMo V2.6 Pro'), 'mimoflash': pid('🩹 Model Patch: MiMo V2.6 Flash'), 'deepseek': pid('🩹 Model Patch: DeepSeek')}
assert all(len(v) == len(set(v)) for v in PATCH.values()) and len(PATCH['aio+g38']) == 2
EXTRA = [MAP[s] for s in ('aria-hybrid-pov', 'aria-npc-voice', 'aria-anthro', 'aria-scent', 'aria-time-place')] + [RR]
BASE = set(xed.ALWAYS) | {IMPT}
problems = Counter(); examples = {}
def bad(kind, label, detail=''):
    problems[kind] += 1
    examples.setdefault(kind, (label, detail[:300]))
HEAD = re.compile(r'then (\d+) dashed lines|Reasoning: (\d+) lines;')
def check_plan(text, label, tags, gate_text):
    m = HEAD.search(text)
    if not m: bad('no plan head', label, text[:200]); return
    n = int(m.group(1) or m.group(2))
    lines = text.split('\n')
    try: g = lines.index('- go')
    except ValueError: bad('no go line', label, text[-200:]); return
    dashed = [l for l in lines[:g] if l.startswith('- ')]
    if len(dashed) != n: bad('plan count', label, f'head {n} dashed {len(dashed)}')
    for l in dashed:
        if not re.match(r'- [A-Z][\w ]*:', l): bad('unlabelled plan line', label, l)
    cue = re.search(r'then (\d+) dashed lines, go and', gate_text or '')
    if tags and (not cue or int(cue.group(1)) != n): bad('tags cue', label, str(cue and cue.group(0)))
    if not tags and cue: bad('cue with tags off', label)
def check_text(t, label, strict):
    if '{{' in t or '}}' in t: bad('leftover macro', label, t[t.find('{{') - 40:t.find('{{') + 40])
    if '\\' in t: bad('backslash', label, t[t.find('\\') - 40:t.find('\\') + 40])
    if '  ' in t: bad('double space', label, t[t.find('  ') - 40:t.find('  ') + 40])
    if strict:
        if '\n\n' in t: bad('blank line', label, t[t.find('\n\n') - 40:t.find('\n\n') + 40])
        if t != t.strip(): bad('edge whitespace', label, repr(t[:20] + '...' + t[-20:]))
        for l in t.split('\n'):
            if re.search(r'[;,:]\s*$', l): bad('line ends on separator', label, l)
            if re.search(r' [.,;:]', l): bad('space before punctuation', label, l)
rng = random.Random(7)
n_cc = n_tc = 0
prev_state_cc = {}; prev_state_tc = {}
modes = {'none': set(), 'adult': {MAP['aria-adult']}, 'freaky': {MAP['aria-adult'], MAP['aria-freaky']}, 'freaky-only': {MAP['aria-freaky']}}
for lc, tags, mode, jb, fate, bonds, patch, flash, hold, imp in itertools.product(('plain', 'twin', 'none'), (1, 0), modes, (1, 0), (1, 0), (1, 0), PATCH, (1, 0), (1, 0), (0, 1)):
    en = set(BASE) | modes[mode] | set(PATCH[patch]) | {e for e in EXTRA if rng.random() < 0.5}
    if lc != 'none': en.add(LCP if lc == 'plain' else LCT)
    if tags: en.add(MAP['aria-thinking-tags'])
    if jb: en.add(MAP['aria-jailbreak'])
    if fate: en.add(MAP['aria-fate'])
    if bonds: en.add(MAP['aria-bonds'])
    if flash: en.add(MAP['aria-flash-gate'])
    if hold: en.add(MAP['aria-character-hold'])
    label = f'CC lc={lc} tags={tags} {mode} jb={jb} fate={fate} bonds={bonds} {patch} flash={flash} hold={hold} imp={imp}'
    r, st = ab.simulate_cc(C, en, 1, impersonate=bool(imp))
    n_cc += 1
    for p, t in r.items(): check_text(t, label + ' ' + nm[p], strict=p in (LCP, LCT, GATE))
    lct = r.get(LCP) or r.get(LCT)
    if lct: check_plan(lct, label, tags, r.get(GATE))
    elif lc != 'none': bad('logic core missing', label)
    jb_should = jb and mode in ('adult', 'freaky') and lc != 'none' and not imp
    if lct:
        has = '\n- Role:' in lct and '\n- Frank:' in lct
        if has != bool(jb_should): bad('JB print', label)
        if has and not re.search(r'\n- Role:[^\n]*\n- Frank:[^\n]*\n- Fresh:', lct): bad('JB position', label)
    # system block identical across turns: state left by the previous config, other seed
    r2, _ = ab.simulate_cc(C, en, 99, state=prev_state_cc, impersonate=bool(imp))
    for p in r:
        if (prompts[p].get('injection_position') or 0) == 0 and r[p] != r2.get(p): bad('system block changes with stale state', label, nm[p])
    r3, _ = ab.simulate_cc(C, en, 1, state=prev_state_cc, impersonate=bool(imp))
    for p in r:
        if r[p] != r3.get(p): bad('in-chat changes with stale state (same seed)', label, nm[p])
    prev_state_cc = st
print('CC renders', n_cc)
# ---------------- TC: matrix plus comparison with CC
sh = dict(ab.SWITCH.findall(T['sysprompt']['content']))
TPATCH = ['none', 'aria-patch-glm', 'aria-patch-kimi-qwen', 'aria-patch-mimo-pro', 'aria-patch-mimo-flash', 'aria-patch-deepseek']
GLUE_CLOSE = re.compile(r" For a message written as User, plan only User's move; skip any Fate, Bonds, Ledger, Layers, Role, Frank, Own words or POV line\.")
norm = lambda s: re.sub(r'\n+', '\n', s).strip()
for lcon, tags, mode, jb, fate, bonds, patch, flash, hold in itertools.product((1, 0), (1, 0), ('none', 'adult', 'freaky', 'freaky-only'), (1, 0), (1, 0), (1, 0), TPATCH, (1, 0), (1, 0)):
    ov = {s: 'off' for s in sh}
    for s in ('aria-hybrid-pov', 'aria-npc-voice', 'aria-anthro', 'aria-scent', 'aria-time-place'):
        ov[s] = 'on' if rng.random() < 0.5 else 'off'
    ov |= {'aria-logic-core': 'on' if lcon else 'off', 'aria-thinking-tags': 'on' if tags else 'off', 'aria-adult': 'on' if mode in ('adult', 'freaky') else 'off',
           'aria-freaky': 'on' if mode in ('freaky', 'freaky-only') else 'off', 'aria-jailbreak': 'on' if jb else 'off', 'aria-fate': 'on' if fate else 'off',
           'aria-bonds': 'on' if bonds else 'off', 'aria-flash-gate': 'on' if flash else 'off', 'aria-character-hold': 'on' if hold else 'off'}
    if patch != 'none': ov[patch] = 'on'
    label = f'TC lc={lcon} tags={tags} {mode} jb={jb} fate={fate} bonds={bonds} {patch} flash={flash} hold={hold}'
    t, st = ab.simulate_tc(T, ov, 1); n_tc += 1
    check_text(t['Post-History'], label + ' post', strict=True)
    check_text(t['System Prompt'], label + ' system', strict=False)
    ph = t['Post-History']
    if lcon:
        lcpart = ph.split('<final_gate>')[0]
        check_plan(lcpart, label, tags, ph)
        if not GLUE_CLOSE.search(lcpart): bad('TC closing glue missing', label)
        has = '\n- Role:' in lcpart
        if has != bool(jb and mode in ('adult', 'freaky')): bad('TC JB print', label)
    t2, _ = ab.simulate_tc(T, ov, 99, state=prev_state_tc)
    if t2['System Prompt'] != t['System Prompt']: bad('TC system changes with stale state', label)
    t3, _ = ab.simulate_tc(T, ov, 1, state=prev_state_tc)
    if t3['Post-History'] != ph: bad('TC post-history changes with stale state (same seed)', label)
    prev_state_tc = st
    # the same configuration in Chibi CC
    c = xed.cc_render(ov)
    sysc = '\n'.join(c[p] for p in order if p in c and (prompts[p].get('injection_position') or 0) == 0)
    if norm(sysc) != norm(t['System Prompt']): bad('TC system != CC system block', label)
    inchat = '\n'.join(c[p] for p in order if p in c and (prompts[p].get('injection_position') or 0) == 1)
    tc_post = GLUE_CLOSE.sub('', ph).replace(' A message written as User skips it.', '').replace(' A message written as User carries none.', '')
    if norm(inchat) != norm(tc_post):
        import difflib
        d = [l for l in difflib.unified_diff(norm(inchat).split('\n'), norm(tc_post).split('\n'), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
        bad('TC post-history != CC in-chat (after TC glue)', label, ' | '.join(d)[:300])
    if lcon and ' A message written as User skips it.' in ph.replace('- Tally', '').split('<final_gate>')[1] and False: pass
    # notes: with LC on only the Tally note may print; with LC off the gate notes print on each present line
    notes = ph.count('A message written as User')
    gate = ph.split('<final_gate>')[1] if '<final_gate>' in ph else ''
    want_gate_notes = 0 if lcon else sum(1 for v in ('ariaEchoGate', 'ariaPovGate', 'ariaLedgerGate', 'ariaHoldGate') if st.get(v))
    got_gate_notes = gate.count('A message written as User')
    if got_gate_notes != want_gate_notes: bad('TC gate notes', label, f'want {want_gate_notes} got {got_gate_notes}')
print('TC renders', n_tc)
print('PROBLEMS:', dict(problems))
for k, v in examples.items(): print(' ', k, '->', v)
