#!/usr/bin/env python3
import json, sys
sys.path.insert(0, '.')
import build_g4 as b
from notes_g4 import NOTES
from t import T

d = b.build()
tokens = {}
for pid, p in d['prompts'].items():
    n, tk, out = T(p['content'])
    tokens[pid] = tk
# gate and Mode lines (rendered, {{user}} counted as User)
def line_tokens(s):
    return T(s)[1]
tokens['ariaScentGate'] = line_tokens(b.SCENT_GATE)
tokens['ariaPovGate'] = line_tokens(b.POV_GATE)
tokens['ariaModeLine (Adult Context)'] = line_tokens(b.ADULT_MODE)
tokens['ariaModeLine (Freaky Override)'] = line_tokens(b.FREAKY_MODE)
# keep the order: each module followed by its own line
order = []
ids = list(d['prompts'])
by_prefix = {i[:8]: i for i in ids}
seq = [('15a8065d', None), ('cca418a6', None), ('2a2e12d0', None), ('dd3642f5', 'ariaScentGate'),
       ('b7b6ab7f', 'ariaPovGate'), ('nsfw', 'ariaModeLine (Adult Context)'),
       ('4537b57d', 'ariaModeLine (Freaky Override)')]
ordered = {}
for pre, line in seq:
    pid = next(i for i in ids if i.startswith(pre))
    ordered[pid] = tokens[pid]
    if line:
        ordered[line] = tokens[line]
d['tokens'] = ordered
d['notes'] = NOTES
out = sys.argv[1]
open(out, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print('wrote', out)
print(json.dumps(ordered, ensure_ascii=False, indent=1))
