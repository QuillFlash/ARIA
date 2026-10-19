import json, sys, copy, io, contextlib, re
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools')
import aria_budget as ab
for label, f in (('ARIA CC', "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"), ('Chibi CC', "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json")):
    P = json.load(open(R + '/' + f))
    prompts = {p['identifier']: p for p in P['prompts']}
    main = prompts['main']['content']
    first = [l for l in main.split('\n') if l.startswith('{{setvar::')][0]
    # the blanking run: the setvar::x:: run at the end of the first line (after comments)
    run = re.findall(r'\{\{setvar::([\w-]+)::\}\}', first)
    print(label, 'blanks in first line:', len(run), '| last three:', run[-3:], '| gemini38Patch count in main:', main.count('{{setvar::gemini38Patch::}}'))
    assert run[-1] == 'gemini38Patch' and run[-2] == 'ariaJbLines', run[-3:]
    # every variable any entry sets that some patch-only entry reads?
    with contextlib.redirect_stdout(io.StringIO()):
        t, e = ab.analyse_cc(P, f)
    print('  live checker errors:', e)
    M = copy.deepcopy(P)
    for p in M['prompts']:
        if p['identifier'] == 'main':
            assert p['content'].count('{{setvar::gemini38Patch::}}') == 1
            p['content'] = p['content'].replace('{{setvar::gemini38Patch::}}', '')
    with contextlib.redirect_stdout(io.StringIO()):
        t2, e2 = ab.analyse_cc(M, f)
    print('  mutant (blank removed) errors:', e2)
    # the old checker (pre-fix snapshot) on the mutant
    sys.path.insert(0, R + '/.claude/aria-work/build/orig')
    import importlib.util
    spec = importlib.util.spec_from_file_location('ab_old', R + '/.claude/aria-work/build/orig/aria_budget.py'); old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
    with contextlib.redirect_stdout(io.StringIO()):
        t3, e3 = old.analyse_cc(M, f) if 'filename' in old.analyse_cc.__code__.co_varnames else old.analyse_cc(M)
    print('  old checker on mutant:', e3)
    # two turns: 3.8 + All-In-One, then All-In-One alone
    nm = {pid: prompts[pid]['name'] for pid in prompts}
    g38 = [p for p in prompts if '3.8' in nm[p]][0]; aio = [p for p in prompts if 'All-In-One' in nm[p]][0]
    order = P['prompt_order'][1]['order']
    shipped = {r['identifier'] for r in order if r['enabled']}
    for preset, tag in ((P, 'live'), (M, 'mutant')):
        r1, st = ab.simulate_cc(preset, shipped | {g38, aio}, 1)
        r2, _ = ab.simulate_cc(preset, shipped | {aio}, 2, state=st)
        fresh, _ = ab.simulate_cc(preset, shipped | {aio}, 2)
        sysdiff = sum(len(r2[p]) - len(fresh[p]) for p in fresh if (prompts[p].get('injection_position') or 0) == 0)
        print(f'  two-turn {tag}: system block chars leaked on turn 2 = {sysdiff}')
