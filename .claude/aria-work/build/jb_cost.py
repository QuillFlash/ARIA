#!/usr/bin/env python3
"""Measure the Chibi JB's cost inside the approved Chibi Logic Core (G3 final), CC and TC, with the frozen checker's renderer."""
import json, random, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab  # noqa: E402

W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
g3 = json.load(open(f'{W}/chibi/final/G3.json', encoding='utf-8'))
cc_lc = g3['prompts']['15b770cf-6049-5f3b-b25d-be09728a65d5']['content']
tc_lc = g3['tc']['post_history_logic_core']

lines = json.load(open(sys.argv[1], encoding='utf-8'))['lines'] if len(sys.argv) > 1 else None
if lines is None:
    raise SystemExit('usage: jb_cost.py candidate.json')
jb = '\n'.join(lines)


def render(text, state):
    st = dict(state)
    out = ab.render(text, st, random.Random(1))
    return out


def cost(label, text, base_state):
    off = render(text, base_state)
    on_state = dict(base_state, ariaJb=render(jb, {}), ariaJbLines='2')
    on = render(text, on_state)
    print(f'{label}: off {len(off)} chars, on {len(on)} chars, +{len(on) - len(off)} chars = +{(len(on) - len(off)) / 4:.2f} tok')
    return on


mode = {'ariaModeLine': '- Mode: realism, persona-true.'}
# CC plain Logic Core (the entry renders to nothing but the plan); the JB counter only shows in the 'N lines' digit
for tags in (False, True):
    st = dict(mode)
    if tags:
        st.update(ariaThinkOpen='<thinking>', ariaThinkClose='</thinking>')
    on = cost(f'CC Logic Core, adult on, tags {"on" if tags else "off"}', cc_lc, st)
st = dict(mode, **{'aria-logic-core': 'on'})
for tags in (False, True):
    st = dict(mode, **{'aria-logic-core': 'on'})
    if tags:
        st.update(ariaThinkOpen='<thinking>', ariaThinkClose='</thinking>')
    cost(f'TC post_history Logic Core, adult on, tags {"on" if tags else "off"}', tc_lc, st)

# show the rendered plan once with the JB on (CC, tags off)
st = dict(mode, ariaJb=render(jb, {}), ariaJbLines='2')
print('---- rendered CC Logic Core, adult+JB, tags off ----')
print(render(cc_lc, st))
