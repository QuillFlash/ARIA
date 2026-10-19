#!/usr/bin/env python3
"""Review check 4: render matrix for Chibi CC, side by side with ARIA CC, using the checker's simulate_cc.

usage: python3 matrix.py [CHIBI_CC] [--jobs N]

Axes (full product): Logic Core (plain, twin, none), Tags, adult mode (none, Adult, Freaky, both), JB, Fate, Bonds,
Time, Flash Gate, Hold, model patch (none, each patch, All-In-One + 3.8 Flash, 3.8 Flash alone), normal and Impersonate.
Per configuration a seeded pick of POV, Scent, Anthro, Codex, Engine and NPC Voice on/off (the same pick for both presets).

Per render, Chibi on its own:
  the plan head's N equals the dashed lines before '- go'; the Tags cue in the gate repeats N; no '{{' or '}}';
  no backslash (literal \\n); no doubled space anywhere; no blank line, edge whitespace, separator-ended line or
  space before punctuation inside the plan and the gate; JB lines print exactly when JB, an adult mode and a Logic Core
  are on on a normal turn, right before '- Fresh:'; dangling tags.
Chibi against ARIA (same configuration, same seed):
  the same entries render (non-empty), the same plan label sequence and N, the same gate label sequence, the same Tags
  cue presence, the same dangling-tag set.
Stale state: the configuration rendered after a different configuration's turn (its leftover variables, seeded pick)
  renders every entry exactly as a fresh render (system block for caching, In-Chat for correctness).
"""
import itertools, json, random, re, sys
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/build/review_cc')
import ab_snap as ab  # noqa: E402

REPO = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/'
ARIA = REPO + "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
CHIBI = REPO + "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"
LC = '15b770cf-6049-5f3b-b25d-be09728a65d5'
TW = '591b8c15-985e-59f1-8c90-59e7cae236ae'
TAGS = '303f26f5-bc2f-5dde-a9e9-aaaacd3eff4b'
ADULT = 'nsfw'
FREAKY = '4537b57d-e002-586d-a4c9-233740c51605'
JBID = '05f6e90d-b30b-48d5-b2bf-26a6e45faffa'
FATE = 'acc2177a-34e4-4941-93a2-b80bc18b8c91'
BONDS = '5506d699-fb00-49ce-a631-73b3f0036eae'
TIME = '5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa'
FLASH = '2e3e7f63-8463-51ff-ba8f-e5b05162c193'
HOLD = 'dc8b1acb-9a7e-5a43-b9aa-38e7b70662a3'
GEM38 = '333dbbed-344d-4a6c-90c5-b0625291115a'
AIO = 'ac96376e-5777-595b-8f48-359f864b0685'
GATE = 'jailbreak'
IMP = '379e3c22-9a25-5e6d-bf4a-037d49aa60d9'
POV = 'b7b6ab7f-032b-5c37-aa89-1a0494782d21'
SCENT = 'dd3642f5-f418-5d74-88cf-88275a1c2001'
ANTHRO = '2a2e12d0-1344-442c-8200-9eef9fd43a52'
CODEX = '9869a1e5-ec75-518a-a9fa-0a8db9600ee0'
ENGINE = '15a8065d-1d77-5db5-9d95-675f4424d44e'
NPC = 'cca418a6-ceeb-5a89-a2d4-0c76b9d8b261'
RR = '939286fd-2ccb-4971-ab70-b39779830294'
BASE = {'main', '0dc06d25-6eaa-4f98-8711-c4456f19e80e', 'f23feaf4-fa91-5bae-8ff7-02cf49c447e0', GATE, IMP}
OPTIONAL = [POV, SCENT, ANTHRO, CODEX, ENGINE, NPC, RR]

_c = {}


def load(path):
    if path not in _c:
        d = json.load(open(path, encoding='utf-8'))
        _c[path] = d
    return _c[path]


def patch_ids(d):
    name = {p['identifier']: p['name'] for p in d['prompts']}
    return [r['identifier'] for r in d['prompt_order'][1]['order'] if name[r['identifier']].startswith('🩹')]


def combos(d):
    pats = patch_ids(d)
    patch_opts = [('none', ())] + [(pid[:8], (pid,)) for pid in pats if pid != GEM38] + [('AIO+3.8', (AIO, GEM38)), ('3.8 alone', (GEM38,))]
    modes = [('noadult', ()), ('adult', (ADULT,)), ('freaky', (FREAKY,)), ('adult+freaky', (ADULT, FREAKY))]
    i = 0
    for lc, tags, mode, jb, fate, bonds, time_, flash, hold, patch, imp in itertools.product(
            (LC, TW, None), (False, True), modes, (False, True), (False, True), (False, True), (False, True), (False, True),
            (False, True), patch_opts, (False, True)):
        rnd = random.Random(i)
        i += 1
        opt = tuple(x for x in OPTIONAL if rnd.random() < 0.75)
        yield dict(i=i, lc=lc, tags=tags, mode=mode[0], mset=mode[1], jb=jb, fate=fate, bonds=bonds, time=time_, flash=flash,
                   hold=hold, patch=patch[0], pset=patch[1], imp=imp, opt=opt)


def enabled_of(k):
    en = set(BASE) | set(k['mset']) | set(k['pset']) | set(k['opt'])
    if k['lc']:
        en.add(k['lc'])
    for flag, pid in ((k['tags'], TAGS), (k['jb'], JBID), (k['fate'], FATE), (k['bonds'], BONDS), (k['time'], TIME),
                      (k['flash'], FLASH), (k['hold'], HOLD)):
        if flag:
            en.add(pid)
    return en


def label(k):
    return (f"#{k['i']} lc={'twin' if k['lc'] == TW else 'plain' if k['lc'] else 'none'} tags={int(k['tags'])} {k['mode']} "
            f"jb={int(k['jb'])} fate={int(k['fate'])} bonds={int(k['bonds'])} time={int(k['time'])} flash={int(k['flash'])} "
            f"hold={int(k['hold'])} patch={k['patch']} {'IMP' if k['imp'] else 'normal'} opt={[o[:6] for o in k['opt']]}")


def plan_info(plan):
    lines = plan.split('\n')
    if '- go' not in lines:
        return None
    go = lines.index('- go')
    dashed = [l for l in lines[:go] if l.startswith('- ')]
    m = re.search(r'(\d+) (?:dashed )?lines', '\n'.join(lines[:2]))
    n = int(m.group(1)) if m else None
    labels = [re.match(r'- ([^:]+):', l).group(1) if re.match(r'- ([^:]+):', l) else l for l in dashed]
    return dict(n=n, count=len(dashed), labels=labels, lines=lines)


def gate_labels(gate):
    return [re.match(r'- ([^:]+):', l).group(1) for l in gate.split('\n') if re.match(r'- ([^:]+):', l)]


def dangling(r):
    text_all = '\n'.join(r.values())
    defined = {t for t in re.findall(r'<([A-Za-z_]+)>', text_all) if f'</{t}>' in text_all}
    return set(re.findall(r'<([A-Za-z_]+)>', text_all)) - defined - ab.HTML_TAGS


def check(k):
    A, C = load(ARIA), load(CHIBI)
    en = enabled_of(k)
    errs = []
    rc, stc = ab.simulate_cc(C, en, seed=7, impersonate=k['imp'])
    ra, sta = ab.simulate_cc(A, en, seed=7, impersonate=k['imp'])
    full = '\n'.join(rc.values())
    if '{{' in full or '}}' in full:
        errs.append('unrendered macro: ' + re.search(r'.{0,30}(?:\{\{|\}\}).{0,30}', full, re.S).group(0).replace('\n', '⏎'))
    if '\\' in full:
        errs.append('backslash prints: ' + re.search(r'.{0,30}\\.{0,30}', full, re.S).group(0).replace('\n', '⏎'))
    for pid, t in rc.items():
        if '  ' in t:
            errs.append(f'double space in {pid[:8]}: ' + re.search(r'.{0,25}  .{0,25}', t, re.S).group(0).replace('\n', '⏎'))

    for pid, t in rc.items():
        if t and t != t.strip() and not (ra.get(pid) and ra[pid] != ra[pid].strip()):
            errs.append(f'edge whitespace in {pid[:8]} (ARIA has none): {t[:20]!r}…{t[-20:]!r}')
    # same entries render non-empty
    ne_c = {p for p, t in rc.items() if t.strip()}
    ne_a = {p for p, t in ra.items() if t.strip()}
    if ne_c != ne_a:
        errs.append(f'non-empty entries differ from ARIA: chibi-only {sorted(x[:8] for x in ne_c - ne_a)}, aria-only {sorted(x[:8] for x in ne_a - ne_c)}')
    gate_c, gate_a = rc.get(GATE, ''), ra.get(GATE, '')
    if gate_labels(gate_c) != gate_labels(gate_a):
        errs.append(f'gate labels differ: chibi {gate_labels(gate_c)} vs aria {gate_labels(gate_a)}')
    cue_c = re.search(r'then (\d+) dashed lines, go', gate_c)
    cue_a = re.search(r'then (\d+) dashed lines, go', gate_a)
    if bool(cue_c) != bool(cue_a):
        errs.append(f'Tags cue presence differs: chibi {bool(cue_c)} aria {bool(cue_a)}')
    for nm, t in (('gate', gate_c),):
        if '\n\n' in t:
            errs.append('blank line inside the gate')
    if k['lc']:
        plan_c, plan_a = rc.get(k['lc'], ''), ra.get(k['lc'], '')
        pc, pa = plan_info(plan_c), plan_info(plan_a)
        if pc is None:
            errs.append('no "- go" line in the Chibi plan')
        else:
            if pc['n'] != pc['count']:
                errs.append(f"plan head says {pc['n']}, dashed lines before go: {pc['count']}")
            if cue_c and int(cue_c.group(1)) != pc['count']:
                errs.append(f"gate cue says {cue_c.group(1)}, dashed lines: {pc['count']}")
            if k['tags'] and not cue_c:
                errs.append('Tags on with a Logic Core, but no gate cue')
            if pa and (pc['labels'] != pa['labels'] or pc['n'] != pa['n']):
                errs.append(f"plan differs from ARIA: chibi {pc['n']} {pc['labels']} vs aria {pa['n']} {pa['labels']}")
            if '\n\n' in plan_c:
                errs.append('blank line inside the plan')
            for nm, t in (('plan', plan_c), ('gate', gate_c)):
                for l in t.split('\n'):
                    if l != l.strip():
                        errs.append(f'edge whitespace in the {nm}: {l!r}'[:120])
                    if l.rstrip().endswith((';', ',')) or (l.rstrip().endswith(':') and not l.startswith(('As game master', 'Cells'))
                                                           and 'starts on the line after that:' not in l):
                        errs.append(f'{nm} line ends on a separator: {l[-50:]!r}')
                    if re.search(r' [.,;:]', l):
                        errs.append(f'space before punctuation in the {nm}: ' + re.search(r'.{0,20} [.,;:].{0,10}', l).group(0))
            has_jb = 'Role' in pc['labels'] and 'Frank' in pc['labels']
            want_jb = k['jb'] and k['mode'] != 'noadult' and not k['imp']
            if has_jb != want_jb:
                errs.append(f'JB lines print={has_jb}, expected {want_jb}')
            if has_jb:
                L = pc['labels']
                if not (L.index('Role') + 1 == L.index('Frank') and L.index('Frank') + 1 == L.index('Fresh')):
                    errs.append(f'Role/Frank not right before Fresh: {L}')
    else:
        if cue_c:
            errs.append('gate cue without a Logic Core')
    if dangling(rc) != dangling(ra):
        errs.append(f'dangling tags differ: chibi {sorted(dangling(rc))} vs aria {sorted(dangling(ra))}')
    # stale state from a different configuration's turn
    rnd = random.Random(k['i'] * 31 + 5)
    other = dict(k)
    for key in ('tags', 'jb', 'fate', 'bonds', 'time', 'flash', 'hold', 'imp'):
        other[key] = rnd.random() < 0.6
    other['mset'] = rnd.choice([(), (ADULT,), (FREAKY,), (ADULT, FREAKY)])
    pats = patch_ids(C)
    other['pset'] = rnd.choice([(), (AIO, GEM38), (GEM38,)] + [(p,) for p in pats])
    other['opt'] = tuple(OPTIONAL)
    other['lc'] = rnd.choice([LC, TW, None])
    _, left = ab.simulate_cc(C, enabled_of(other), seed=3, impersonate=other['imp'])
    # an earlier turn on the same config, too
    _, left_same = ab.simulate_cc(C, en, seed=11, impersonate=not k['imp'])
    for nm, st in (('another config', left), ('the same config', left_same)):
        r2, _ = ab.simulate_cc(C, en, seed=7, state=st, impersonate=k['imp'])
        for pid in rc:
            if rc[pid] != r2.get(pid):
                pos = next(p for p in C['prompts'] if p['identifier'] == pid).get('injection_position') or 0
                errs.append(f"stale state after {nm} changes {'SYSTEM BLOCK' if pos == 0 else 'in-chat'} entry {pid[:8]}")
    return errs


def run(chunk):
    out = []
    for k in chunk:
        e = check(k)
        if e:
            out.append((label(k), e))
    return len(chunk), out


def _init(p):
    global CHIBI
    CHIBI = p


def main():
    global CHIBI
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if args and not args[0].isdigit():
        CHIBI = args[0]
    jobs = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else 8
    allk = list(combos(load(CHIBI)))
    chunks = [allk[i::jobs * 8] for i in range(jobs * 8)]
    total, bad = 0, []
    with ProcessPoolExecutor(jobs, initializer=_init, initargs=(CHIBI,)) as ex:
        for n, out in ex.map(run, chunks):
            total += n
            bad += out
    print(f'{total} configurations (each rendered for Chibi, ARIA and twice with stale state), {len(bad)} with errors')
    seen = {}
    for lab, errs in bad:
        for e in errs:
            key = re.sub(r'\d+', 'N', e)[:90]
            seen.setdefault(key, [0, lab, e])[0] += 1
    for kind, (cnt, lab, e) in sorted(seen.items(), key=lambda x: -x[1][0])[:60]:
        print(f'  [{cnt}x] {e}\n        e.g. {lab}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
