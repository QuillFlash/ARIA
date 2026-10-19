import json, re, sys, copy, random, io, contextlib
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab

S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
CC = S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
TC = S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
draft = json.load(open(sys.argv[1] if len(sys.argv) > 1 else S + '/g6c/G6.check.json', encoding='utf-8'))
cc = json.load(open(CC, encoding='utf-8'))
tc = json.load(open(TC, encoding='utf-8'))

def quiet(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = fn(*a, **k)
    return r, buf.getvalue()

# --- baseline
(base_cc_tot, base_cc_err), _ = quiet(ab.analyse_cc, cc)
(base_tc_tot, base_tc_err), _ = quiet(ab.analyse_tc, tc)
print('BASE CC', base_cc_tot, base_cc_err)
print('BASE TC', base_tc_tot, base_tc_err)

# --- swap in CC
cc2 = copy.deepcopy(cc)
for p in cc2['prompts']:
    if p['identifier'] in draft['prompts']:
        p['content'] = draft['prompts'][p['identifier']]['content']
(new_cc_tot, new_cc_err), _ = quiet(ab.analyse_cc, cc2)
print('NEW  CC', new_cc_tot, new_cc_err)

# --- swap in TC blocks: find each source block and replace
by = {p['identifier'][:8]: p for p in cc['prompts']}
wrap = {
 '1f2e1f97': ('aria-patch-glm', '{{#if .aria-patch-glm}}', '\n{{/if}}'),
 '9bb6c2b0': ('aria-patch-kimi-qwen', '{{#if .aria-patch-kimi-qwen}}', '\n{{/if}}'),
 '33f92483': ('aria-patch-mimo-pro', '{{#if .aria-patch-mimo-pro}}', '\n{{/if}}'),
 '3a027832': ('aria-patch-mimo-flash', '{{#if .aria-patch-mimo-flash}}', '\n{{/if}}'),
 'e04b9c2b': ('aria-patch-deepseek', '{{#if .aria-patch-deepseek}}', '\n{{/if}}'),
 '2e3e7f63': ('aria-flash-gate', '{{if .aria-flash-gate}}', '{{/if}}'),
 'dc8b1acb': ('aria-character-hold', '{{#if .aria-character-hold}}', '{{/if}}'),
}
tc2 = copy.deepcopy(tc)
content = tc2['sysprompt']['content']
for k, (sw, o, c) in wrap.items():
    src = by[k]['content']
    body = src[src.find('}}{{trim}}') + len('}}{{trim}}'):]
    if body.startswith('\n'):
        body = body[1:]
    old = o + body + c
    assert content.count(old) == 1, (sw, content.count(old))
    content = content.replace(old, draft['tc']['module_' + sw])
tc2['sysprompt']['content'] = content
(new_tc_tot, new_tc_err), _ = quiet(ab.analyse_tc, tc2)
print('NEW  TC', new_tc_tot, new_tc_err)

# --- skeleton of TC blocks vs source blocks
sys.path.insert(0, S + '/spec')
import skeleton
ok = True
for k, (sw, o, c) in wrap.items():
    src = by[k]['content']
    body = src[src.find('}}{{trim}}') + len('}}{{trim}}'):]
    if body.startswith('\n'):
        body = body[1:]
    old = o + body + c
    ok &= skeleton.compare('TC ' + sw, old, draft['tc']['module_' + sw])

# --- line counts and joins
def lines(text): return [l for l in text.split('\n') if l.startswith('- ')]
for k in ('ac96376e', '1f2e1f97', '9bb6c2b0', '33f92483', '3a027832', 'e04b9c2b'):
    pid = by[k]['identifier']
    c = draft['prompts'][pid]['content']
    st = {'gemini38Patch': ''}
    if k == 'e04b9c2b':
        st.update({'ariaBondsLine': 'x', 'ariaFateLine': 'x'})
    out = {}
    o = ab.render(c, st, random.Random(1))
    n = int(st['ariaPatchLines'])
    gl = lines(st['ariaPatchGate'])
    print(f'{by[k]["name"]:38} ariaPatchLines={n} gate lines={len(gl)}', 'OK' if n == len(gl) else 'MISMATCH')
