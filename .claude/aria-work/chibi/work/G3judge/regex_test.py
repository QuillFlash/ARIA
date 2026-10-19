"""Run the snapshot's Logic Core regex scripts (JS patterns through Python re) on echoed or leaked plans,
for the source texts and a G3 file, and report whether each script leaves the same remainder.

usage: python3 regex_test.py G3.json
"""
import json, random, re, sys
S = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work"
sys.path.insert(0, S + "/spec/frozen")
import aria_budget as ab

cc = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
tcrx = json.load(open(S + "/chibi/src/ARIA 1.0 Regex Scripts (Text Completions).json", encoding='utf-8'))
tcsrc = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", encoding='utf-8'))
g3 = json.load(open(sys.argv[1], encoding='utf-8'))
P = '15b770cf-6049-5f3b-b25d-be09728a65d5'
src_cc = {p['identifier']: p for p in cc['prompts']}[P]['content']
ph = tcsrc['sysprompt']['post_history']
src_tc = ph[:ph.index('<final_gate>')]
assert [s['findRegex'] for s in cc['extensions']['regex_scripts']] == [s['findRegex'] for s in tcrx], 'CC and TC regex differ'
scripts = [s for s in cc['extensions']['regex_scripts'] if 'Logic Core' in s['scriptName'] or 'untagged plan' in s['scriptName']
           or 'thinking' in s['scriptName'].lower() or 'reasoning' in s['scriptName'].lower()]


def conv(find):
    m = re.match(r'^/(.*)/([a-z]*)$', find, re.S)
    flags = re.I if 'i' in m.group(2) else 0
    if 'm' in m.group(2):
        flags |= re.M
    return re.compile(m.group(1), flags), 'g' in m.group(2)


def run(script, text):
    rx, g = conv(script['findRegex'])
    repl = script.get('replaceString') or ''

    def f(m):
        out = repl
        for i in range(9, 0, -1):
            out = out.replace('$%d' % i, (m.group(i) or '') if i <= rx.groups else '')
        return out
    return rx.sub(f, text, count=0 if g else 1)


def rend(text, state):
    st = dict(state)
    return ab.render(text, st, random.Random(1))


TAGS = {'ariaThinkOpen': '<thinking>', 'ariaThinkClose': '</thinking>'}
MODS = {'ariaFateLine': '- Fate: x.', 'ariaLedgerLine': '- Ledger: y.', 'ariaJb': '- Role: r.\n- Frank: f.', 'ariaJbLines': '2'}
PROSE = '\n\nShe turned away from the window.'
cases = []
for kind, src, mine, extra in (('CC', src_cc, g3['prompts'][P]['content'], {}),
                               ('TC', src_tc, g3['tc']['post_history_logic_core'], {'aria-logic-core': 'on'})):
    for mods in (False, True):
        st = dict(TAGS, **extra, **(MODS if mods else {}))
        cases.append((f'{kind} Tags-on template echoed{" (modules)" if mods else ""}', rend(src, st) + PROSE, rend(mine, st) + PROSE))
    # A leaked untagged plan (Tags off): the lines from OOC to go, without the head/tail sentences, then prose
    st = dict(extra, **MODS)
    def plan_only(t):
        lines = t.split('\n')
        a = next(i for i, l in enumerate(lines) if l.startswith('- OOC:'))
        b = next(i for i, l in enumerate(lines) if l == '- go')
        return '\n'.join(lines[a:b + 1])
    cases.append((f'{kind} untagged plan leaked', plan_only(rend(src, st)) + PROSE, plan_only(rend(mine, st)) + PROSE))
    cases.append((f'{kind} Tags-off <logic_core> block echoed', rend(src, st) + PROSE, rend(mine, st) + PROSE))

bad = 0
for label, s_text, m_text in cases:
    print(f'##### {label}')
    for sc in scripts:
        a, b = run(sc, s_text), run(sc, m_text)
        sa, sb = a.strip() == PROSE.strip(), b.strip() == PROSE.strip()
        touched_a, touched_b = a != s_text, b != m_text
        if touched_a or touched_b:
            same = (sa == sb) and (touched_a == touched_b)
            if not same:
                bad += 1
            print(f"  {'OK  ' if same else 'DIFF'} {sc['scriptName'][:78]:78} | source -> {'prose only' if sa else repr(a[-90:])} | G3 -> {'prose only' if sb else repr(b[-90:])}")
print('\nscripts behaving differently for source and G3:', bad)
