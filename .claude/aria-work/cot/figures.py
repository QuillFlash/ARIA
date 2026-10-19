#!/usr/bin/env python3
"""Every token figure the guide quotes, for one directory of presets (characters / 4, comments stripped)."""
import json, re, sys, io, contextlib
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab
D = sys.argv[1]
N = {'cc': "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json",
     'tc': "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",
     'ccc': "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json",
     'ctc': "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"}
L = lambda k: json.load(open(f'{D}/{N[k]}', encoding='utf-8'))
out = {}
for k in ('cc', 'ccc'):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        totals, errors = ab.analyse_cc(L(k), N[k])
    out[k] = {lab: v for lab, v in totals.items()}
    out[k]['per_entry'] = {m.group(2): int(m.group(1)) for m in re.finditer(r'^\s+(\d+)\s+(.+)$', buf.getvalue(), re.M)}
for k in ('tc', 'ctc'):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        totals, errors = ab.analyse_tc(L(k), N[k]) if 'filename' in ab.analyse_tc.__code__.co_varnames else ab.analyse_tc(L(k))
    out[k] = dict(totals)
    p = L(k); sw = dict(ab.SWITCH.findall(p['sysprompt']['content']))
    tot = lambda o: sum(ab.tokens(t) for t in ab.simulate_tc(p, o, 1)[0].values())
    def cost(base, s):
        o = dict(base)
        if base.get(s) == 'on':
            o[s] = 'off'; return tot(base) - tot(o)
        o[s] = 'on'
        if s == 'aria-freaky': o['aria-adult'] = 'on'; return tot(o) - tot(dict(base, **{'aria-adult': 'on'}))
        return tot(o) - tot(base)
    shipped = dict(sw)
    lc_on = dict(sw, **{'aria-logic-core': 'on'})
    out[k]['switch_from_shipped'] = {s: cost(shipped, s) for s in sw}
    out[k]['switch_lc_on'] = {s: cost(lc_on, s) for s in sw}
    out[k]['tags_with_lc'] = tot(dict(lc_on, **{'aria-thinking-tags': 'on'})) - tot(dict(lc_on, **{'aria-thinking-tags': 'off'}))
    out[k]['lean_without_lc'] = tot(dict(sw, **{'aria-logic-core': 'off'}))
print(json.dumps(out, ensure_ascii=False, indent=1))
