"""Render the G3 Logic Core (CC plain, twin, TC) under every on/off combination of the variables it splices,
with Tags on and off, and flag spacing or punctuation faults and count mismatches.

usage: python3 render_scan.py G3.json
"""
import itertools, json, random, re, sys
S = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work"
sys.path.insert(0, S + "/spec/frozen")
import aria_budget as ab

d = json.load(open(sys.argv[1], encoding='utf-8'))
P, T = '15b770cf-6049-5f3b-b25d-be09728a65d5', '591b8c15-985e-59f1-8c90-59e7cae236ae'
jb = json.load(open(S + "/jb/final.json", encoding='utf-8'))
VALS = {
    'ariaModeLine': [('ariaModeLine', '- Mode: realism; persona-true; each plea new.')],
    'ariaFateLine': [('ariaFateLine', "- Fate: A tier on q's band; B source; C form vs THREAD; cell; C 20 limit; results only.")],
    'ariaBondsLine': [('ariaBondsLine', '- Bonds: listed acts add Sparks (max 2 per pair), slights Grudge; Sparks 7: BOND +1, Sparks 0.')],
    'ariaLedgerLine': [('ariaLedgerLine', "- Ledger: last 🎲 block plus this turn's changes, ages +1; the closing 🎲 block copies it.")],
    'ariaHoldLine': [('ariaHoldLine', '- Layers: per card character, one card trait this mood fits and one it would bury.')],
    'ariaPatchGate': [('ariaPatchGate', '- Echo: e.\n- Repeats: r.\n- Bodies: b.'), ('ariaPatchLines', '3')],
    'ariaPatchJoins': [('ariaPatchJoins', '- Joins: j.')],
    'ariaPatchTally': [('ariaPatchTally', '- Tally: t.')],
    'ariaVoiceExtra': [('ariaVoiceExtra', '; one raw thought each, in their own voice, steering their next move')],
    'ariaJb': [('ariaJb', '\n'.join(jb['lines']).replace('{{user}}', 'User')), ('ariaJbLines', str(len(jb['lines'])))],
}
TAGS = {'ariaThinkOpen': '<thinking>', 'ariaThinkClose': '</thinking>'}
FAULTS = [(r'  ', 'double space'), (r' [.,;:]', 'space before punctuation'), (r'[;,]{2}|\.\.', 'doubled punctuation'),
          (r'\n\n', 'blank line'), (r'\n ', 'line starts with a space'), (r'[;,] *\n', 'line ends on a separator'),
          (r'\{\{|\}\}', 'unrendered macro'), (r'(?<![<\w/])\.[A-Za-z]', 'missing space after period')]
texts = {'CC plain': d['prompts'][P]['content'], 'CC twin': d['prompts'][T]['content'],
         'TC': d['tc']['post_history_logic_core']}
keys = list(VALS)
problems, shapes = {}, 0
for name, text in texts.items():
    for tags in (False, True):
        for combo in itertools.product((False, True), repeat=len(keys)):
            st = dict(TAGS) if tags else {}
            if name == 'TC':
                st['aria-logic-core'] = 'on'
            for k, on in zip(keys, combo):
                if on:
                    st.update(VALS[k])
            s2 = dict(st)
            out = ab.render(text, s2, random.Random(1))
            shapes += 1
            for pat, label in FAULTS:
                for m in re.finditer(pat, out):
                    ctx = out[max(0, m.start() - 30):m.end() + 30]
                    problems.setdefault((name, label, ctx), 0)
                    problems[(name, label, ctx)] += 1
            body = out.split('\n')
            gi = body.index('- go')
            dashed = [l for l in body[:gi] if l.startswith('- ')]
            if str(len(dashed)) != s2.get('logicCoreLines'):
                problems.setdefault((name, 'count mismatch', f'{len(dashed)} vs {s2.get("logicCoreLines")}'), 0)
                problems[(name, 'count mismatch', f'{len(dashed)} vs {s2.get("logicCoreLines")}')] += 1
            head = f'{len(dashed)} dashed lines' if tags else f'Reasoning: {len(dashed)} lines;'
            if head not in out:
                problems.setdefault((name, 'head count differs from printed lines', head), 0)
print('shapes rendered:', shapes)
if not problems:
    print('no spacing, punctuation, macro or count faults')
for (name, label, ctx), n in sorted(problems.items()):
    print(f'{name} | {label} | x{n} | {ctx!r}')
