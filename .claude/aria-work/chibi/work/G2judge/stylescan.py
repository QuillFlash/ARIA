import json, sys, random, re
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
from paths import *
import aria_budget as ab
d = json.load(open(FINAL, encoding='utf-8'))
full_state = {k: f'- {k}: x.' for k in ('ariaScentGate', 'ariaPovGate', 'ariaLedgerGate', 'ariaPatchGate', 'ariaPatchJoins',
                                        'ariaFlashGate', 'ariaHoldGate')}
full_state.update({'ariaDice': 'Fate dice: A 1 | B 2 | C 3', 'player-posthistory': 'PH', 'ariaPlanCue': 'CUE'})
texts = {}
st = {}
texts['codex'] = ab.render(d['prompts'][CODEX]['content'], st, random.Random(1))
texts['echo'] = st['ariaEchoGate']; texts['chop'] = st['ariaChopGate']
s2 = dict(st); texts['gate_plain'] = ab.render(d['prompts'][GATE]['content'], s2, random.Random(1))
s3 = dict(st); s3.update(full_state); texts['gate_full'] = ab.render(d['prompts'][GATE]['content'], s3, random.Random(1))
s4 = dict(st); s4.update(full_state); texts['tc_gate_full'] = ab.render(d['tc']['post_history_gate'], s4, random.Random(1))
bad = 0
for name, t in texts.items():
    for pat, label in ((r'  ', 'double space'), (r' [.,;:]', 'space before punctuation'), (r'"', 'double quote'),
                       (r"(?<![A-Za-z])'[A-Za-z]", 'opening single quote'), (r'\n\n', 'blank line'), (r'[.;,]{2}', 'doubled punctuation'),
                       (r'\{\{|\}\}', 'unrendered macro')):
        for m in re.finditer(pat, t):
            bad += 1
            print(f'{name}: {label} at {m.start()}: {t[max(0,m.start()-30):m.start()+30]!r}')
print('issues:', bad)
print('--- gate with every print set (CC):')
print(texts['gate_full'])
