#!/usr/bin/env python3
"""Render matrix for Chibi CC with the checker's simulate_cc.

usage: python3 verify_chibi_cc.py CHIBI_CC.json [--jobs N]

Axes: Logic Core (plain / system-role twin), Tags on/off, adult mode (none, Adult, Freaky, both), JB on/off,
Fate on/off, Bonds on/off, Time on/off, Flash Gate on/off, Hold on/off, model patch (none, each of the seven,
Gemini All-In-One with 3.8 Flash), normal and Impersonate.
Checks per render: the plan head's N equals the dashed lines before '- go', the Tags cue in the gate repeats N,
no '{{' or '}}' remains, no backslash prints, no doubled space, no blank line or separator-ended line inside the
plan and gate, JB lines print exactly when JB and an adult mode are on and it is not an Impersonate turn,
the Mode line matches the adult mode.
"""
import itertools, json, re, sys
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab  # noqa: E402

PATH = None
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

_cache = {}


def load():
    if 'd' not in _cache:
        d = json.load(open(PATH, encoding='utf-8'))
        prompts = {p['identifier']: p for p in d['prompts']}
        name = {k: v['name'] for k, v in prompts.items()}
        order = [r['identifier'] for r in d['prompt_order'][1]['order']]
        patches = [k for k in order if name[k].startswith('🩹')]
        _cache.update(d=d, prompts=prompts, name=name, order=order, patches=patches)
    return _cache


def combos():
    c = load()
    patch_opts = [('none', set())] + [(c['name'][p], {p}) for p in c['patches'] if p != GEM38] + [('AIO+3.8', {AIO, GEM38}), ('3.8 alone', {GEM38})]
    modes = [('noadult', set()), ('adult', {ADULT}), ('freaky', {FREAKY}), ('adult+freaky', {ADULT, FREAKY})]
    for lc, tags, (mname, mset), jb, fate, bonds, time_, flash, hold, (pname, pset), imp in itertools.product(
            (LC, TW), (False, True), modes, (False, True), (False, True), (False, True), (False, True), (False, True),
            (False, True), patch_opts, (False, True)):
        yield dict(lc=lc, tags=tags, mode=mname, mset=sorted(mset), jb=jb, fate=fate, bonds=bonds, time=time_, flash=flash,
                   hold=hold, patch=pname, pset=sorted(pset), imp=imp)


def label(k):
    return (f"{'twin' if k['lc'] == TW else 'plain'} tags={'on' if k['tags'] else 'off'} {k['mode']} jb={int(k['jb'])} "
            f"fate={int(k['fate'])} bonds={int(k['bonds'])} time={int(k['time'])} flash={int(k['flash'])} hold={int(k['hold'])} "
            f"patch={k['patch']} {'IMPERSONATE' if k['imp'] else 'normal'}")


def check(k):
    c = load()
    d = c['d']
    en = {'main', '0dc06d25-6eaa-4f98-8711-c4456f19e80e', 'f23feaf4-fa91-5bae-8ff7-02cf49c447e0', GATE,
          '15a8065d-1d77-5db5-9d95-675f4424d44e', 'cca418a6-ceeb-5a89-a2d4-0c76b9d8b261', '2a2e12d0-1344-442c-8200-9eef9fd43a52',
          '9869a1e5-ec75-518a-a9fa-0a8db9600ee0', 'dd3642f5-f418-5d74-88cf-88275a1c2001', 'b7b6ab7f-032b-5c37-aa89-1a0494782d21',
          '939286fd-2ccb-4971-ab70-b39779830294', IMP}
    en |= {k['lc']} | set(k['mset']) | set(k['pset'])
    for flag, pid in ((k['tags'], TAGS), (k['jb'], JBID), (k['fate'], FATE), (k['bonds'], BONDS), (k['time'], TIME),
                      (k['flash'], FLASH), (k['hold'], HOLD)):
        if flag:
            en.add(pid)
    r, st = ab.simulate_cc(d, en, seed=7, impersonate=k['imp'])
    errs = []
    full = '\n'.join(r.values())
    if '{{' in full or '}}' in full:
        errs.append('unrendered macro: ' + re.search(r'.{0,30}(?:\{\{|\}\}).{0,30}', full, re.S).group(0).replace('\n', '⏎'))
    if '\\' in full:
        errs.append('backslash prints: ' + re.search(r'.{0,30}\\.{0,30}', full, re.S).group(0).replace('\n', '⏎'))
    plan = r.get(k['lc'], '')
    gate = r.get(GATE, '')
    lines = plan.split('\n')
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
    if k['tags']:
        cue = re.search(r'then (\d+) dashed lines, go', gate)
        if not cue:
            errs.append('Tags on but the gate has no cue')
        elif int(cue.group(1)) != n:
            errs.append(f'gate cue says {cue.group(1)}, dashed lines before go: {n}')
    elif re.search(r'Begin with', gate):
        errs.append('Tags off but the gate has a Tags cue')
    # no blank lines, no double spaces, no separator-ended lines in the plan and the gate
    for nm, t in (('plan', plan), ('gate', gate)):
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
    for nm, t in r.items():
        if nm in (LC, TW, GATE):
            continue
        if '  ' in t:
            errs.append(f'double space in {c["name"][nm]}')
        if t != t.lstrip() or re.search(r'[ \t]\n*$', t):
            errs.append(f'edge whitespace in {c["name"][nm]}')
    # JB lines
    has_jb = any(l.startswith('- Role: ') for l in lines) and any(l.startswith('- Frank: ') for l in lines)
    want_jb = k['jb'] and k['mode'] != 'noadult' and not k['imp']
    if has_jb != want_jb:
        errs.append(f'JB lines print={has_jb}, expected {want_jb}')
    if want_jb and has_jb:
        i_role = next(i for i, l in enumerate(lines) if l.startswith('- Role: '))
        i_frank = next(i for i, l in enumerate(lines) if l.startswith('- Frank: '))
        i_fresh = next(i for i, l in enumerate(lines) if l.startswith('- Fresh: '))
        if not (i_role + 1 == i_frank and i_frank + 1 == i_fresh):
            errs.append('Role/Frank are not adjacent right before Fresh')
    # Mode line
    mode = [l for l in lines if l.startswith('- Mode: ')]
    wantmode = {'noadult': None, 'adult': '- Mode: realism, persona-true.', 'freaky': None, 'adult+freaky': None}[k['mode']]
    if k['mode'] == 'noadult' and mode:
        errs.append('Mode line without an adult mode')
    if k['mode'] != 'noadult' and not mode:
        errs.append('adult mode on but no Mode line')
    if k['mode'] == 'adult' and mode and mode[0] != wantmode:
        errs.append(f'Adult Mode line wrong: {mode[0]!r}')
    if k['mode'] in ('freaky', 'adult+freaky') and mode and mode[0] != '- Mode: freaky; escalate.':
        errs.append(f'Freaky Mode line wrong: {mode[0]!r}')
    return errs


def run(chunk):
    out = []
    for k in chunk:
        e = check(k)
        if e:
            out.append((label(k), e))
    return len(chunk), out


def main():
    global PATH
    PATH = sys.argv[1]
    jobs = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else 4
    allk = list(combos())
    chunks = [allk[i::jobs * 8] for i in range(jobs * 8)]
    total, bad = 0, []
    with ProcessPoolExecutor(jobs, initializer=_init, initargs=(PATH,)) as ex:
        for n, out in ex.map(run, chunks):
            total += n
            bad += out
    print(f'{total} renders, {len(bad)} with errors')
    seen = {}
    for lab, errs in bad:
        for e in errs:
            seen.setdefault(re.sub(r'\d+', 'N', e)[:100], (lab, e))
    for kind, (lab, e) in list(seen.items())[:40]:
        print('  -', e, '   [', lab, ']')
    sys.exit(1 if bad else 0)


def _init(p):
    global PATH
    PATH = p


if __name__ == '__main__':
    main()
