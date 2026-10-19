import copy, io, json, re, subprocess, sys, contextlib
W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G4judge'
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
sys.path.insert(0, W); sys.path.insert(0, S + '/spec/frozen')
import aria_budget as ab
import bodies, comments
SRC_CC = S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
SRC_TC = S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
cc = json.load(open(SRC_CC, encoding='utf-8'))
tc = json.load(open(SRC_TC, encoding='utf-8'))
by_id = {p['identifier']: p for p in cc['prompts']}
TCMAP = {'nsfw': 'aria-adult', '4537b57d-e002-586d-a4c9-233740c51605': 'aria-freaky',
         'b7b6ab7f-032b-5c37-aa89-1a0494782d21': 'aria-hybrid-pov', 'cca418a6-ceeb-5a89-a2d4-0c76b9d8b261': 'aria-npc-voice',
         '2a2e12d0-1344-442c-8200-9eef9fd43a52': 'aria-anthro', 'dd3642f5-f418-5d74-88cf-88275a1c2001': 'aria-scent',
         '15a8065d-1d77-5db5-9d95-675f4424d44e': None}

def cc_body(content):
    m = re.match(r'\{\{//.*?\}\}\{\{trim\}\}\n', content, re.S)
    assert m, content[:80]
    return content[m.end():]

def tc_span(text, switch):
    """(start, end) of the inner text of {{#if .switch}}...{{/if}}, or of <scene_engine>...</scene_engine>."""
    if switch is None:
        a = text.index('<scene_engine>'); b = text.index('</scene_engine>') + len('</scene_engine>')
        assert text.count('<scene_engine>') == 1
        return a, b
    tag = '{{#if .%s}}' % switch
    assert text.count(tag) == 1, switch
    a = text.index(tag) + len(tag)
    then, els, end = ab.split_if(text, a)
    assert els is None
    return a, a + len(then)

sys_src = tc['sysprompt']['content']
new_cc = copy.deepcopy(cc)
new_by_id = {p['identifier']: p for p in new_cc['prompts']}
final_prompts, tc_out, spans = {}, {}, []
for pid, body in bodies.B.items():
    src_body = cc_body(by_id[pid]['content'])
    a, b = tc_span(sys_src, TCMAP[pid])
    src_seg = sys_src[a:b]
    expect = src_body if TCMAP[pid] is None else src_body + '\n'
    assert src_seg == expect, f'TC/CC mapping differs for {pid}'
    content = '{{// ' + comments.C[pid] + '}}{{trim}}\n' + body
    final_prompts[pid] = {'name': by_id[pid]['name'], 'content': content}
    new_by_id[pid]['content'] = content
    new_seg = body if TCMAP[pid] is None else body + '\n'
    key = 'scene_engine' if TCMAP[pid] is None else 'if_' + TCMAP[pid]
    tc_out[key] = new_seg
    spans.append((a, b, new_seg))
    open(f'{W}/tc_src_{key}.txt', 'w', encoding='utf-8').write(src_seg)
    open(f'{W}/tc_new_{key}.txt', 'w', encoding='utf-8').write(new_seg)
# rebuild TC system prompt with the new segments (right to left keeps offsets valid)
sys_new = sys_src
for a, b, seg in sorted(spans, reverse=True):
    sys_new = sys_new[:a] + seg + sys_new[b:]
new_tc = copy.deepcopy(tc); new_tc['sysprompt']['content'] = sys_new
json.dump({'prompts': final_prompts, 'tc': tc_out}, open(f'{W}/G4_candidate.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(new_cc, open(f'{W}/cc_inmem.json', 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(new_tc, open(f'{W}/tc_inmem.json', 'w', encoding='utf-8'), ensure_ascii=False)

def quiet(f, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = f(*a)
    return r, buf.getvalue()
(t0, e0), _ = quiet(ab.analyse_cc, cc)
(t1, e1), out_cc = quiet(ab.analyse_cc, new_cc)
(u0, f0), _ = quiet(ab.analyse_tc, tc)
(u1, f1), out_tc = quiet(ab.analyse_tc, new_tc)
print('CC totals before', t0); print('CC totals after ', t1)
print('CC errors before', len(e0), e0[:5]); print('CC errors after ', len(e1), e1[:5])
print('CC new errors:', sorted(set(e1) - set(e0)))
print('TC totals before', u0); print('TC totals after ', u1)
print('TC errors before', len(f0), f0[:5]); print('TC errors after ', len(f1), f1[:5])
print('TC new errors:', sorted(set(f1) - set(f0)))
