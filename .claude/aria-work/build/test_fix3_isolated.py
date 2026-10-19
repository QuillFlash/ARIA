"""Each of the four changed scripts on its own (no other script helping): on echoed ARIA TC / Chibi TC Logic Cores, tags on, {{user}} as a
name, followed by a reply, the script must leave neither the "For a message written as ... line." sentence nor the "Every response starts
with" line behind. OLD (snapshot) scripts are run alongside to show they did leave them."""
import json
import re
import sys
from rxlib import *

OLD_CC = json.load(open(SNAP_CC, encoding='utf-8'))['extensions']['regex_scripts']
NEW_CC = json.load(open(CCFILE, encoding='utf-8'))['extensions']['regex_scripts']
NEW_TC = json.load(open(RXFILE, encoding='utf-8'))
REPLY = ("The kettle clicked off, and Aria set two cups on the counter before she looked up.\n\n"
         "\"Sit down, Manager. You look like you've been arguing with a spreadsheet again.\"")
NAMES = ["Lewis", "User", "Lewis the Manager", "D'Artagnan", "Dr. Elena Marchetti-Vasquez of the Westerbrook Line"]
LEFT = ['For a message written as', 'Every response starts with', 'closes on the line after go', 'Nothing above go enters the reply',
        'The reply starts on the line after that']
IDX = {0: 'Fold (display)', 1: 'Hide closing line (display)', 2: 'Keep out of prompt', 24: 'Impersonate strip'}
# which echo shapes each script is built for (a script needs its own anchor: <thinking> at the start, or a closing tag before the line)
SHAPES = {0: ('full', 'full, one newline', 'full + real plan'),
          1: ('full', 'full, one newline', 'plan + closing', 'closing only', 'full + real plan'),
          2: ('full', 'full, one newline', 'plan + closing', 'closing only', 'full + real plan'),
          24: ('full', 'full, one newline', 'plan + closing', 'full + real plan')}

tc = tc_preset()
g3 = g3_text()
failures, old_dirty, runs = [], 0, 0
for name in NAMES:
    for config in ('lean', 'full'):
        o = overrides_for(tc, config, True)
        lc, state = render_tc_logic_core(tc, o, name)
        chibi = render_chibi_logic_core(g3, state, name)
        for src, text in (('ARIA TC', lc), ('Chibi TC', chibi)):
            closing = text[text.index('closes on the line after go.'):]
            shapes = {'full': text + '\n\n', 'full, one newline': text + '\n',
                      'plan + closing': '<thinking>\n' + plan_lines(text) + '\n</thinking> ' + closing + '\n\n',
                      'closing only': closing + '\n\n',
                      'full + real plan': text + '\n' + plan_lines(text) + '\n</thinking>\n\n'}
            for i, title in IDX.items():
                for shape in SHAPES[i]:
                    body = shapes[shape] + REPLY
                    for side, scripts in (('CC', NEW_CC), ('TC', NEW_TC)):
                        out = sub_js(scripts[i], body)
                        runs += 1
                        left = [p for p in LEFT if p in out.replace(REPLY, '')]
                        if left or out.count(REPLY) != 1 or not out.rstrip().endswith(REPLY):
                            failures.append(f'{title} [{side} copy] on {src}, {name[:12]}, {config}, {shape}: left {left}')
                    old_out = sub_js(OLD_CC[i], body)
                    old_dirty += any(p in old_out.replace(REPLY, '') for p in ('For a message written as',))
print(f'{runs} isolated runs (4 scripts x CC and TC copies x shapes x 5 names x lean/full x ARIA/Chibi)')
print(f'the OLD scripts left the "For a message written as" sentence behind in {old_dirty} of {runs // 2} comparable runs')
if failures:
    print(len(failures), 'FAILURES')
    for f in failures[:20]:
        print(' -', f)
    sys.exit(1)
print('ALL PASS: every changed script, on its own, removes the sentence and the "Every response starts with" line')
