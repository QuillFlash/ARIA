#!/usr/bin/env python3
"""Echo scenarios for the regex pipeline test, rendered from ARIA CC and Chibi CC (names as Lewis)."""
import json, sys
sys.path.insert(0, '.')
import ab_snap as ab
import matrix as m
REPLY = 'Mira sets the cup down and looks at Lewis.\n\n"You came back," she says.'
PLAN_LINES = {
    'aria': None, 'chibi': None}
out = {}
for tag, path in (('aria', m.ARIA), ('chibi', m.CHIBI)):
    d = json.load(open(path, encoding='utf-8'))
    cases = {}
    for cfg, extra in (('plain', set()), ('full', {m.ADULT, m.JBID, m.FATE, m.BONDS, m.HOLD, m.TIME, '1f2e1f97-1cde-5d46-8eb0-87e2fe55f916'})):
        for tags in (0, 1):
            en = {'main', m.GATE, m.LC, m.CODEX} | extra | ({m.TAGS} if tags else set())
            r, _ = ab.simulate_cc(d, en, seed=1)
            plan = r[m.LC].replace('User', 'Lewis')
            # a filled plan with this config's labels
            lines = plan.split('\n')
            go = lines.index('- go')
            labels = [l.split(':')[0] for l in lines[:go] if l.startswith('- ')]
            filled = '\n'.join(f'{lb}: something about the scene.' for lb in labels) + '\n- go'
            k = f'{cfg}_tags{tags}'
            cases[k + '_echo_template'] = plan + '\n' + REPLY
            if tags:
                cases[k + '_echo_template_then_plan'] = plan + '\n' + filled + '\n</thinking>\n' + REPLY
                cases[k + '_tagged_plan'] = '<thinking>\n' + filled + '\n</thinking>\n' + REPLY
                closing = plan[plan.index('</thinking> closes'):]
                cases[k + '_closing_echo'] = '<thinking>\n' + filled + '\n' + closing + '\n' + REPLY
            cases[k + '_untagged_plan'] = filled + '\n' + REPLY
    out[tag] = cases
json.dump({'reply': REPLY, 'cases': out}, open('rx_cases.json', 'w'), ensure_ascii=False, indent=1)
print({t: len(c) for t, c in out.items()})
