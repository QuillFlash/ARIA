#!/usr/bin/env python3
"""Build the final G2 draft from the *_final.txt files and comments.json, with tokens and notes."""
import json, os, random, re, sys, importlib.util
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
W = S + '/chibi/work_g2'
sys.path.insert(0, S + '/spec/frozen')
import aria_budget as ab
spec = importlib.util.spec_from_file_location('b', W + '/build.py'); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)

com = json.load(open(W + '/comments.json', encoding='utf-8'))
for k, v in com.items():
    assert '{{' not in v and '}}' not in v, k
out = b.build('codex_final.txt', 'gate_final.txt', 'echo_final.txt', 'chop_final.txt', 'comments.json')
CODEX = b.CODEX_ID

# hygiene: no trailing spaces, no double spaces, no CR, no tabs in model-facing text
for pid, p in out['prompts'].items():
    body = p['content']
    for ln in body.split('\n'):
        assert ln == ln.rstrip(), (pid, ln[:50])
    assert '\r' not in body and '\t' not in body

# TC gate = CC gate after the comment line plus TC's four notes only
cc_gate = out['prompts']['jailbreak']['content'].split('\n', 1)[1]
tc_gate = out['tc']['post_history_gate']
removed = tc_gate
for note in (' A message written as {{user}} skips it.', ' A message written as {{user}} carries none.'):
    removed = removed.replace(note, '')
assert removed == cc_gate, 'TC gate differs from CC gate beyond the four notes'
assert tc_gate.count('A message written as {{user}}') == 4

def tok(text, state=None):
    st = dict(state or {})
    r = ab.render(text, st, random.Random(1))
    return len(r) / 4, st
c_tok, st = tok(out['prompts'][CODEX]['content'])
g_tok, _ = tok(out['prompts']['jailbreak']['content'])
tg_tok, _ = tok(tc_gate)
echo_tok = len(st['ariaEchoGate']) / 4
chop_tok = len(st['ariaChopGate']) / 4
r = lambda x: int(round(x))
out['tokens'] = {
    CODEX: r(c_tok),
    'ariaEchoGate': r(echo_tok),
    'ariaChopGate': r(chop_tok),
    'jailbreak': r(g_tok),
    'tc.post_history_gate': r(tg_tok),
}
print('exact:', c_tok, echo_tok, chop_tok, g_tok, tg_tok)
assert c_tok <= 330 and echo_tok <= 30 and chop_tok <= 30 and g_tok <= 290, 'over a ceiling'

out['notes'] = open(W + '/notes.txt', encoding='utf-8').read().strip()
dest = S + '/chibi/drafts/G2.json'
os.makedirs(os.path.dirname(dest), exist_ok=True)
with open(dest, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('wrote', dest)
