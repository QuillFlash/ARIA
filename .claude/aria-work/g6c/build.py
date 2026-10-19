import json, re, sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/g6c')
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import importlib
import aria_budget as ab
import cand, comments
importlib.reload(cand); importlib.reload(comments)

S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
CC = S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
cc = json.load(open(CC, encoding='utf-8'))
by = {p['identifier'][:8]: p for p in cc['prompts']}

def render(text, state=None):
    st = dict(state or {})
    out = ab.render(text, st, random.Random(1))
    return out, st

def tk(s):
    return len(s) / 4

B = cand.B
# ---- measurements used in comments
m = {}
m['claude'] = tk(render(B['b59a2ad1'])[0])
m['g38'] = tk(render(B['333dbbed'])[1]['gemini38Patch'])
o, s = render(B['ac96376e'], {'gemini38Patch': ''})
m['aio_own'] = tk(o); m['aio_gate'] = tk(s['ariaPatchGate'])
o, s = render(B['1f2e1f97']); m['glm_lines'] = tk(s['ariaPatchGate'])
o, s = render(B['9bb6c2b0']); m['kq_own'] = tk(o); m['kq_gate'] = tk(s['ariaPatchGate'])
o, s = render(B['33f92483']); m['mp_own'] = tk(o); m['mp_gate'] = tk(s['ariaPatchGate'])
o, s = render(B['3a027832']); m['mf_own'] = tk(o); m['mf_gate'] = tk(s['ariaPatchGate'])
o, s = render(B['e04b9c2b'], {'ariaBondsLine': 'x', 'ariaFateLine': 'x'})
m['ds_gate'] = tk(s['ariaPatchGate']); m['ds_joins'] = tk(s['ariaPatchJoins']); m['ds_tally'] = tk(s['ariaPatchTally'])
o, s = render(B['2e3e7f63']); m['fg'] = tk(s['ariaFlashGate'])
o, s = render(B['2e3e7f63'], {'ariaPatchJoins': 'x'}); m['fg_nr'] = tk(s['ariaFlashGate'])
o, s = render(B['dc8b1acb']); m['hold'] = tk(s['ariaHoldLine']) + tk(s['ariaHoldGate'])
fmt = {k: f'{round(v)}' for k, v in m.items()}

def comment(pid):
    return comments.C[pid].format(**fmt)

order = ['b59a2ad1', '333dbbed', 'ac96376e', '1f2e1f97', '9bb6c2b0', '33f92483', '3a027832', 'e04b9c2b', '2e3e7f63', 'dc8b1acb']
prompts = {}
for k in order:
    src = by[k]
    content = '{{// ' + comment(k) + '}}{{trim}}\n' + B[k]
    prompts[src['identifier']] = {'name': src['name'], 'content': content}

# ---- TC blocks
wrap = {
 '1f2e1f97': ('aria-patch-glm', '{{#if .aria-patch-glm}}', '\n{{/if}}'),
 '9bb6c2b0': ('aria-patch-kimi-qwen', '{{#if .aria-patch-kimi-qwen}}', '\n{{/if}}'),
 '33f92483': ('aria-patch-mimo-pro', '{{#if .aria-patch-mimo-pro}}', '\n{{/if}}'),
 '3a027832': ('aria-patch-mimo-flash', '{{#if .aria-patch-mimo-flash}}', '\n{{/if}}'),
 'e04b9c2b': ('aria-patch-deepseek', '{{#if .aria-patch-deepseek}}', '\n{{/if}}'),
 '2e3e7f63': ('aria-flash-gate', '{{if .aria-flash-gate}}', '{{/if}}'),
 'dc8b1acb': ('aria-character-hold', '{{#if .aria-character-hold}}', '{{/if}}'),
}
tc = {}
for k, (sw, o, c) in wrap.items():
    tc['module_' + sw] = o + B[k] + c
for sw, text in comments.T.items():
    tc['switch_comment_' + sw] = '{{// ' + text + '}}'

# ---- tokens
tokens = {}
def put(key, val):
    tokens[key] = round(val, 2)
for k in order:
    pid = by[k]['identifier']
    st = {'gemini38Patch': ''} if k == 'ac96376e' else {}
    out, sets = render(B[k], st)
    put(pid, tk(out))
put('gemini38Patch (3.8 Flash Method)', m['g38'])
put('ariaChopGate (Gemini)', tk(render(B['ac96376e'])[1]['ariaChopGate']))
put('ariaPatchGate (Gemini All-In-One)', m['aio_gate'])
put('ariaPatchGate (GLM, 5 lines)', m['glm_lines'])
put('ariaPatchGate (Kimi / Qwen)', m['kq_gate'])
put('ariaPatchGate (MiMo V2.6 Pro)', m['mp_gate'])
put('ariaPatchGate (MiMo V2.6 Flash)', m['mf_gate'])
put('ariaPatchGate (DeepSeek, 3 lines)', m['ds_gate'])
put('ariaPatchJoins (DeepSeek)', m['ds_joins'])
for lab, st in (('both', {'ariaBondsLine': 'x', 'ariaFateLine': 'x'}), ('Bonds only', {'ariaBondsLine': 'x'}), ('Fate only', {'ariaFateLine': 'x'})):
    out, sets = render(B['e04b9c2b'], st)
    put(f'ariaPatchTally ({lab})', tk(sets['ariaPatchTally']))
out, sets = render(B['e04b9c2b'], {'ariaBondsLine': 'x', 'ariaFateLine': 'x'})
put('DeepSeek own text (Tally on)', tk(out))
out, sets = render(B['e04b9c2b']); put('DeepSeek own text (no Tally)', tk(out))
put('ariaFlashGate (with Runs)', m['fg']); put('ariaFlashGate (without Runs)', m['fg_nr'])
put('ariaVoiceExtra', tk(render(B['2e3e7f63'])[1]['ariaVoiceExtra']))
o, s = render(B['dc8b1acb'])
put('ariaHoldLine', tk(s['ariaHoldLine'])); put('ariaHoldGate', tk(s['ariaHoldGate']))
for key, text in tc.items():
    if key.startswith('module_'):
        sw = key[len('module_'):]
        st = {sw: 'on', 'ariaBondsLine': 'x', 'ariaFateLine': 'x'}
        out, sets = render(text, st)
        put('tc.' + key + ' (own text)', tk(out))

notes = open(S + '/g6c/notes.txt', encoding='utf-8').read().strip() if __import__('os').path.exists(S + '/g6c/notes.txt') else ''
draft = {'prompts': prompts, 'tc': tc, 'tokens': tokens, 'notes': notes}
out_path = sys.argv[1] if len(sys.argv) > 1 else S + '/g6c/G6.check.json'
open(out_path, 'w', encoding='utf-8').write(json.dumps(draft, ensure_ascii=False, indent=1))
print('wrote', out_path)
