#!/usr/bin/env python3
"""Render matrix and CC comparison for Chibi TC, with the checker's own simulate_tc / simulate_cc.

usage: python3 verify_chibi_tc.py CHIBI_TC.json [--cc CHIBI_CC.json] [--glue capped|finals] [--jobs N] [--modules-only] [--quick]

Part A, the matrix (every combination of): Logic Core on/off, tags on/off, adult mode (none, Adult, Freaky, both), JB, Fate, Bonds,
Time & Place, Flash Gate, Character Hold, model patch (none and each of the five TC has), and three extras patterns (Hybrid POV,
NPC Voice, Anthro, Scent all off / shipped / all on). Per render: no '{{' or '}}' left, no backslash, the plan head's N equals the
dashed lines before '- go', the Tags cue in the gate repeats N and is absent with Tags off or the Logic Core off, no blank line /
double space / edge whitespace / separator-ended line / space before punctuation in the plan and the gate, no double space in the
System Prompt, Role and Frank print adjacent right before Fresh exactly when JB, an adult mode and the Logic Core are on, the Mode
line matches the adult mode, and the TC glue is where the build puts it (see GLUE below).
Part B, against Chibi CC (normal turns): for each shared module, TC's rendered module text equals CC's rendered entry text and the
variables the module sets are equal; for every matrix render the TC System Prompt equals the CC system block, the TC Logic Core
equals the CC Logic Core and the TC gate equals the CC gate, after removing TC's own glue (and nothing else) and collapsing newline
runs in the System Prompt.

GLUE (TC's own additions, the only text TC may have that CC does not):
  capped (default): the plan's closing sentence 'For a message written as User, plan only User's move, with no Fate, Bonds, Ledger,
    Layers, Role, Frank, Own words or POV line.' with the Logic Core on; the Tally note ' A message written as User skips it.' after
    the Tally line; the four gate notes (Own words, POV, Ledger, Layers) only while the Logic Core is off.
  finals: the same closing sentence as the finals have it ('... Role or Frank line.') and the four gate notes always.
"""
import difflib, itertools, json, random, re, sys
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab  # noqa: E402

R = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA'
CCPATH = R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"
PATH = None
GLUE = 'capped'

CC = {'main': 'main', 'custom': '0dc06d25-6eaa-4f98-8711-c4456f19e80e', 'tags': '303f26f5-bc2f-5dde-a9e9-aaaacd3eff4b',
      'adult': 'nsfw', 'freaky': '4537b57d-e002-586d-a4c9-233740c51605', 'jb': '05f6e90d-b30b-48d5-b2bf-26a6e45faffa',
      'pov': 'b7b6ab7f-032b-5c37-aa89-1a0494782d21', 'scene': '15a8065d-1d77-5db5-9d95-675f4424d44e',
      'npc': 'cca418a6-ceeb-5a89-a2d4-0c76b9d8b261', 'anthro': '2a2e12d0-1344-442c-8200-9eef9fd43a52',
      'codex': '9869a1e5-ec75-518a-a9fa-0a8db9600ee0', 'scent': 'dd3642f5-f418-5d74-88cf-88275a1c2001',
      'time': '5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa', 'fate': 'acc2177a-34e4-4941-93a2-b80bc18b8c91',
      'bonds': '5506d699-fb00-49ce-a631-73b3f0036eae', 'glm': '1f2e1f97-1cde-5d46-8eb0-87e2fe55f916',
      'kimi': '9bb6c2b0-7906-564f-852e-3d8c327b4879', 'mimopro': '33f92483-e84c-54a6-9188-1189aff1098a',
      'mimoflash': '3a027832-2e4b-4706-aaed-5fc6ec5e59ad', 'deepseek': 'e04b9c2b-d8a0-5346-ab66-1cf25e5d7c1b',
      'flash': '2e3e7f63-8463-51ff-ba8f-e5b05162c193', 'hold': 'dc8b1acb-9a7e-5a43-b9aa-38e7b70662a3',
      'story': 'f23feaf4-fa91-5bae-8ff7-02cf49c447e0', 'lc': '15b770cf-6049-5f3b-b25d-be09728a65d5',
      'twin': '591b8c15-985e-59f1-8c90-59e7cae236ae', 'gate': 'jailbreak'}
SW = {'aria-logic-core': 'lc', 'aria-thinking-tags': 'tags', 'aria-adult': 'adult', 'aria-freaky': 'freaky', 'aria-jailbreak': 'jb',
      'aria-hybrid-pov': 'pov', 'aria-npc-voice': 'npc', 'aria-anthro': 'anthro', 'aria-scent': 'scent', 'aria-time-place': 'time',
      'aria-fate': 'fate', 'aria-bonds': 'bonds', 'aria-patch-glm': 'glm', 'aria-patch-kimi-qwen': 'kimi',
      'aria-patch-mimo-pro': 'mimopro', 'aria-patch-mimo-flash': 'mimoflash', 'aria-patch-deepseek': 'deepseek',
      'aria-flash-gate': 'flash', 'aria-character-hold': 'hold'}
ALWAYS_CC = ['main', 'custom', 'scene', 'codex', 'gate', 'story']
PATCHES = ['aria-patch-glm', 'aria-patch-kimi-qwen', 'aria-patch-mimo-pro', 'aria-patch-mimo-flash', 'aria-patch-deepseek']

CLOSE_CAPPED = " For a message written as User, plan only User's move, with no Fate, Bonds, Ledger, Layers, Role, Frank, Own words or POV line."
CLOSE_FINALS = " For a message written as User, plan only User's move, with no Fate, Bonds, Ledger, Layers, Role or Frank line."
NOTE_SKIP = ' A message written as User skips it.'
NOTE_NONE = ' A message written as User carries none.'
VARS = re.compile(r'aria[A-Z]\w*|gemini38Patch')

_cache = {}
_n = [0]


def load():
    if 'tc' not in _cache:
        _cache['tc'] = json.load(open(PATH, encoding='utf-8'))
        _cache['cc'] = json.load(open(CCPATH, encoding='utf-8'))
        _cache['prompts'] = {p['identifier']: p for p in _cache['cc']['prompts']}
    return _cache


def collapse(s):
    return re.sub(r'\n+', '\n', s).strip()


def tc_system(tc, ov, seed=1):
    system = ab.SWITCH.sub(lambda m: '{{.%s = %s}}' % (m.group(1), ov.get(m.group(1), m.group(2))), tc['sysprompt']['content'])
    state = {}
    return ab.render(system, state, random.Random(seed)), state


def var_subset(state):
    return {k: v for k, v in state.items() if VARS.fullmatch(k) and v != ''}


def cc_enabled(cfg):
    return {CC[k] for k in ALWAYS_CC} | {CC[SW[s]] for s, v in cfg.items() if v}


def first_diff(a, b):
    la, lb = a.split('\n'), b.split('\n')
    for i, (x, y) in enumerate(itertools.zip_longest(la, lb)):
        if x != y:
            return f'line {i}: TC {x!r:.160} | CC {y!r:.160}'
    return 'equal'


# --------------------------------------------------------------------------------------------- Part B: shared modules

MODULE_CASES = [  # (TC switch, extra TC switches that must be on, extra CC keys)
    ('aria-adult', [], []), ('aria-freaky', [], []), ('aria-jailbreak', ['aria-adult'], ['adult']), ('aria-hybrid-pov', [], []),
    ('aria-npc-voice', [], []), ('aria-anthro', [], []), ('aria-scent', [], []), ('aria-time-place', [], []),
    ('aria-fate', [], []), ('aria-bonds', [], []), ('aria-patch-glm', [], []), ('aria-patch-kimi-qwen', [], []),
    ('aria-patch-mimo-pro', [], []), ('aria-patch-mimo-flash', [], []), ('aria-patch-deepseek', [], []),
    ('aria-patch-deepseek', ['aria-bonds'], ['bonds']), ('aria-patch-deepseek', ['aria-fate'], ['fate']),
    ('aria-patch-deepseek', ['aria-fate', 'aria-bonds'], ['fate', 'bonds']),
    ('aria-flash-gate', [], []), ('aria-flash-gate', ['aria-patch-deepseek'], ['deepseek']), ('aria-character-hold', [], []),
    ('aria-bonds', ['aria-fate'], ['fate']),
]


def module_compare():
    c = load()
    tc, cc, prompts = c['tc'], c['cc'], c['prompts']
    allsw = list(SW)
    errs = []
    for sw, extra_sw, extra_cc in MODULE_CASES:
        base_ov = {s: 'off' for s in allsw} | {e: 'on' for e in extra_sw}
        on_ov = dict(base_ov) | {sw: 'on'}
        t_base, s_base = tc_system(tc, base_ov)
        t_on, s_on = tc_system(tc, on_ov)
        en_base = {CC[k] for k in ALWAYS_CC if k != 'gate'} | {CC[k] for k in extra_cc} | {CC[SW[e]] for e in extra_sw}
        en_on = en_base | {CC[SW[sw]]}
        r_base, cs_base = ab.simulate_cc(cc, en_base, seed=1)
        r_on, cs_on = ab.simulate_cc(cc, en_on, seed=1)
        module_text = r_on.get(CC[SW[sw]], '').strip('\n')
        label = f"{sw}{' + ' + ' + '.join(extra_sw) if extra_sw else ''}"
        # 1. the module's rendered text: TC with the switch on == TC with it off plus CC's entry text, nothing else
        if module_text == '':
            if collapse(t_on) != collapse(t_base):
                errs.append(f'{label}: CC prints nothing but TC prints something: {first_diff(collapse(t_on), collapse(t_base))}')
        else:
            if module_text not in t_on:
                errs.append(f'{label}: CC text not found in the TC render: {module_text[:90]!r}')
            else:
                # remove the one occurrence that is not already in the base render
                rest = t_on
                if t_base.count(module_text) < t_on.count(module_text):
                    rest = t_on.replace(module_text, '', 1)
                    # the occurrence must be a contiguous insertion: compare against the base
                if collapse(rest) != collapse(t_base):
                    errs.append(f'{label}: TC render differs from base + CC text: {first_diff(collapse(rest), collapse(t_base))}')
        # 2. the variables the module sets (rendered values) are equal
        vt, vc = var_subset(s_on), var_subset(cs_on)
        if vt != vc:
            diff = {k: (vt.get(k), vc.get(k)) for k in set(vt) | set(vc) if vt.get(k) != vc.get(k)}
            errs.append(f'{label}: variables differ: ' + '; '.join(f'{k}: TC {v[0]!r:.80} | CC {v[1]!r:.80}' for k, v in sorted(diff.items())))
    return errs


# --------------------------------------------------------------------------------------------- Part A and B per render

def combos(quick=False, stride=1):
    modes = [('noadult', {}), ('adult', {'aria-adult': 'on'}), ('freaky', {'aria-freaky': 'on'}),
             ('adult+freaky', {'aria-adult': 'on', 'aria-freaky': 'on'})]
    extras = [('extras-off', {'aria-hybrid-pov': 'off', 'aria-npc-voice': 'off', 'aria-anthro': 'off', 'aria-scent': 'off'}),
              ('extras-shipped', {'aria-hybrid-pov': 'off', 'aria-npc-voice': 'on', 'aria-anthro': 'off', 'aria-scent': 'on'}),
              ('extras-on', {'aria-hybrid-pov': 'on', 'aria-npc-voice': 'on', 'aria-anthro': 'on', 'aria-scent': 'on'})]
    patches = [('none', None)] + [(p, p) for p in PATCHES]
    if quick:
        extras = extras[1:2]
    for lc, tags, (mname, mov), jb, fate, bonds, time_, flash, hold, (pname, p), (ename, eov) in itertools.product(
            ('on', 'off'), ('on', 'off'), modes, ('on', 'off'), ('on', 'off'), ('on', 'off'), ('on', 'off'), ('on', 'off'),
            ('on', 'off'), patches, extras):
        ov = {s: 'off' for s in SW}
        ov.update(eov)
        ov.update(mov)
        ov.update({'aria-logic-core': lc, 'aria-thinking-tags': tags, 'aria-jailbreak': jb, 'aria-fate': fate, 'aria-bonds': bonds,
                   'aria-time-place': time_, 'aria-flash-gate': flash, 'aria-character-hold': hold})
        if p:
            ov[p] = 'on'
        _n[0] += 1
        if _n[0] % stride == 0:
            yield dict(ov=ov, mode=mname, patch=pname, extras=ename)


def label(k):
    on = [s.replace('aria-', '') for s, v in k['ov'].items() if v == 'on']
    return ' '.join(on) + f" | {k['mode']}"


def check(k):
    c = load()
    tc, cc, prompts = c['tc'], c['cc'], c['prompts']
    ov = k['ov']
    on = {s for s, v in ov.items() if v == 'on'}
    lc, tags = 'aria-logic-core' in on, 'aria-thinking-tags' in on
    r, st = ab.simulate_tc(tc, ov, seed=7)
    sysp, ph = r['System Prompt'], r['Post-History']
    errs = []
    full = sysp + '\n' + ph
    if '{{' in full or '}}' in full:
        errs.append('unrendered macro: ' + re.search(r'.{0,30}(?:\{\{|\}\}).{0,30}', full, re.S).group(0).replace('\n', '⏎'))
    if '\\' in full:
        errs.append('backslash prints: ' + re.search(r'.{0,30}\\.{0,30}', full, re.S).group(0).replace('\n', '⏎'))
    if '<final_gate>' not in ph or '</final_gate>' not in ph:
        errs.append('no final gate in the post-history')
        return errs
    lc_part = ph[:ph.index('<final_gate>')]
    gate = ph[ph.index('<final_gate>'):]
    adult_mode = ('aria-adult' in on) or ('aria-freaky' in on)
    # ---- the Logic Core part
    if not lc:
        if lc_part.strip():
            errs.append('Logic Core off but the post-history holds a plan: ' + lc_part[:60])
    else:
        lines = lc_part.strip('\n').split('\n')
        try:
            go = lines.index('- go')
        except ValueError:
            errs.append('no "- go" line in the plan')
            return errs
        dashed = [l for l in lines[:go] if l.startswith('- ')]
        n = len(dashed)
        m = re.search(r'(\d+) (?:dashed )?lines', '\n'.join(lines[:2]))
        if not m:
            errs.append('plan head has no count')
        elif int(m.group(1)) != n:
            errs.append(f'plan head says {m.group(1)}, dashed lines before go: {n}')
        if tags:
            cue = re.search(r'then (\d+) dashed lines, go', gate)
            if not cue:
                errs.append('Tags on but the gate has no cue')
            elif int(cue.group(1)) != n:
                errs.append(f'gate cue says {cue.group(1)}, dashed lines before go: {n}')
        elif 'Begin with' in gate:
            errs.append('Tags off but the gate has a Tags cue')
        # JB lines
        has_jb = '- Role: ' in lc_part and '- Frank: ' in lc_part
        want_jb = 'aria-jailbreak' in on and adult_mode
        if has_jb != want_jb:
            errs.append(f'JB lines print={has_jb}, expected {want_jb}')
        if want_jb and has_jb:
            i_role = next((i for i, l in enumerate(lines) if l.startswith('- Role: ')), None)
            i_frank = next((i for i, l in enumerate(lines) if l.startswith('- Frank: ')), None)
            i_fresh = next((i for i, l in enumerate(lines) if l.startswith('- Fresh: ')), None)
            if None in (i_role, i_frank, i_fresh):
                errs.append('Role, Frank or Fresh does not start its own plan line')
            elif not (i_role + 1 == i_frank and i_frank + 1 == i_fresh):
                errs.append('Role/Frank are not adjacent right before Fresh')
        # Mode line
        mode = [l for l in lines[:go] if l.startswith('- Mode: ')]
        if not adult_mode and mode:
            errs.append('Mode line without an adult mode')
        if adult_mode and not mode:
            errs.append('adult mode on but no Mode line')
        if mode:
            want = '- Mode: freaky; escalate.' if 'aria-freaky' in on else '- Mode: realism, persona-true.'
            if mode[0] != want:
                errs.append(f'Mode line wrong: {mode[0]!r}')
        # closing sentence (TC's own glue)
        close = CLOSE_CAPPED if GLUE == 'capped' else CLOSE_FINALS
        if lc_part.count(close) != 1:
            errs.append(f'closing sentence found {lc_part.count(close)} times')
        # Tally
        tally = 'aria-patch-deepseek' in on and ('aria-bonds' in on or 'aria-fate' in on)
        if tally != any(l.startswith('- Tally: ') for l in lines):
            errs.append(f'Tally line print={not tally}, expected {tally}')
        notes_in_lc = lc_part.count(NOTE_SKIP)
        if notes_in_lc != (1 if tally else 0):
            errs.append(f'Tally note count {notes_in_lc}, expected {1 if tally else 0}')
        if tally:
            tl = next((l for l in lines if l.startswith('- Tally: ')), '')
            if not tl.endswith(NOTE_SKIP):
                errs.append('the Tally line does not end with the skip note')
        for l in lines[:go]:
            if l and not (l.startswith('- ') or l.startswith('<') or l.startswith('Reasoning') or l.startswith('Fragments')):
                errs.append(f'unexpected line in the plan body: {l[:60]!r}')
    # ---- the gate: the skip notes
    gl = gate.split('\n')
    want_notes = {'Own words': NOTE_SKIP}
    if 'aria-hybrid-pov' in on:
        want_notes['POV'] = NOTE_SKIP
    if 'aria-fate' in on or 'aria-bonds' in on:
        want_notes['Ledger'] = NOTE_NONE
    if 'aria-character-hold' in on:
        want_notes['Layers'] = NOTE_SKIP
    got = {}
    for l in gl:
        for note in (NOTE_SKIP, NOTE_NONE):
            if l.endswith(note):
                mm = re.match(r'- ([\w ]+): ', l)
                got[mm.group(1) if mm else l[:20]] = note
    if GLUE == 'capped' and lc:
        if got:
            errs.append(f'Logic Core on but the gate still carries skip notes: {sorted(got)}')
    else:
        if set(got) != set(want_notes) or any(got[k] != want_notes[k] for k in want_notes if k in got):
            errs.append(f'gate skip notes {sorted(got)}, expected {sorted(want_notes)}')
    # ---- whitespace and punctuation in the plan and the gate
    for nm, t in (('plan', lc_part.strip('\n')), ('gate', gate)):
        if not t:
            continue
        if '\n\n' in t:
            errs.append(f'blank line inside the {nm}')
        if '  ' in t:
            errs.append(f'double space inside the {nm}: ' + re.search(r'.{0,25}  .{0,25}', t).group(0))
        for l in t.split('\n'):
            if l != l.strip():
                errs.append(f'edge whitespace in the {nm}: {l!r}'[:120])
            if l.rstrip().endswith((';', ',', ':')) and not l.startswith('As game master'):
                errs.append(f'{nm} line ends on a separator: {l[-40:]!r}')
            if re.search(r' [.,;:]', l):
                errs.append(f'space before punctuation in the {nm}: ' + re.search(r'.{0,20} [.,;:].{0,10}', l).group(0))
    if '  ' in sysp:
        errs.append('double space in the System Prompt: ' + re.search(r'.{0,25}  .{0,25}', sysp).group(0))
    if sysp != sysp.strip() and sysp.strip() != '':
        errs.append('edge whitespace in the System Prompt')
    # ---- Part B: against CC
    enabled = cc_enabled({s: (v == 'on') for s, v in ov.items()})
    # CC has the Tags entry as a switch of its own: tags matter only with the Logic Core on, TC sets the variables either way
    rc, cs = ab.simulate_cc(cc, enabled, seed=7)
    sys_cc = '\n'.join(t for pid, t in rc.items() if (prompts[pid].get('injection_position') or 0) == 0)
    if collapse(sysp) != collapse(sys_cc):
        errs.append('System Prompt differs from the CC system block: ' + first_diff(collapse(sysp), collapse(sys_cc)))
    close = CLOSE_CAPPED if GLUE == 'capped' else CLOSE_FINALS
    lc_norm = lc_part.replace(close, '').replace(NOTE_SKIP, '').strip('\n')
    cc_lc = rc.get(CC['lc'], '').strip('\n')
    if lc_norm != cc_lc:
        errs.append('Logic Core differs from CC after removing the glue: ' + first_diff(lc_norm, cc_lc))
    gate_norm = gate.replace(NOTE_SKIP, '').replace(NOTE_NONE, '').strip('\n')
    cc_gate = rc.get(CC['gate'], '').strip('\n')
    if gate_norm != cc_gate:
        errs.append('Last-Mile Gate differs from CC after removing the glue: ' + first_diff(gate_norm, cc_gate))
    return errs


def run(chunk):
    out = []
    for k in chunk:
        try:
            e = check(k)
        except Exception as ex:  # a render that raises is a finding, not a crash
            e = [f'render raised {type(ex).__name__}: {str(ex)[:100]}']
        if e:
            out.append((label(k), e))
    return len(chunk), out


def _init(p, g):
    global PATH, GLUE
    PATH, GLUE = p, g


def verify(path, glue='capped', jobs=4, quick=False, modules_only=False, cc_path=None, quiet=False, stride=1):
    """Returns (renders, number with errors, list of (kind, example) tuples)."""
    global PATH, GLUE, CCPATH
    PATH, GLUE = path, glue
    if cc_path:
        CCPATH = cc_path
    _cache.clear()
    problems = []
    try:
        for e in module_compare():
            problems.append(('module', e))
    except Exception as ex:
        problems.append(('module', f'module comparison raised {type(ex).__name__}: {str(ex)[:100]}'))
    total, bad = 0, []
    if not modules_only:
        _n[0] = 0
        allk = list(combos(quick, stride))
        chunks = [allk[i::jobs * 8] for i in range(jobs * 8)]
        with ProcessPoolExecutor(jobs, initializer=_init, initargs=(path, glue)) as ex:
            for n, out in ex.map(run, chunks):
                total += n
                bad += out
        seen = {}
        for lab, errs in bad:
            for e in errs:
                seen.setdefault(re.sub(r'\d+', 'N', e)[:110], (lab, e))
        for kind, (lab, e) in list(seen.items())[:40]:
            problems.append(('matrix', f'{e}   [ {lab} ]'))
    if not quiet:
        print(f'{len(MODULE_CASES)} module comparisons against Chibi CC, {total} matrix renders; {len(bad)} renders with errors; '
              f'{len([p for p in problems if p[0] == "module"])} module differences')
        for kind, e in problems[:50]:
            print(f'  - [{kind}] {e}')
    return total, len(bad), problems


def main():
    args = sys.argv[1:]
    path = args[0]
    glue = args[args.index('--glue') + 1] if '--glue' in args else 'capped'
    jobs = int(args[args.index('--jobs') + 1]) if '--jobs' in args else 4
    cc_path = args[args.index('--cc') + 1] if '--cc' in args else None
    total, nbad, problems = verify(path, glue, jobs, '--quick' in args, '--modules-only' in args, cc_path)
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
