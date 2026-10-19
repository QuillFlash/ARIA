import json, sys
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/.claude/aria-work/spec')
from skeleton import skeleton
A = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"))
C = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"))
print('top-level keys equal (order):', list(A) == list(C))
print('top-level non-prompt fields that differ:', [k for k in A if k not in ('prompts', 'prompt_order') and A[k] != C[k]])
print('prompt_order[0] equal:', A['prompt_order'][0] == C['prompt_order'][0])
oa, oc = A['prompt_order'][1], C['prompt_order'][1]
print('prompt_order[1] keys/char equal:', {k: oa[k] == oc[k] for k in oa if k != 'order'})
pa = {p['identifier']: p for p in A['prompts']}; pc = {p['identifier']: p for p in C['prompts']}
print('order ids equal:', [r['identifier'] for r in oa['order']] == [r['identifier'] for r in oc['order']])
print('order enabled diffs:', [(pc[r['identifier']]['name'], ra['enabled'], r['enabled']) for ra, r in zip(oa['order'], oc['order']) if ra['enabled'] != r['enabled']])
print('prompts id order equal:', [p['identifier'] for p in A['prompts']] == [p['identifier'] for p in C['prompts']])
bad = 0
for a, c in zip(A['prompts'], C['prompts']):
    if list(a) != list(c): print('key order differs', a['identifier']); bad += 1
    for k in a:
        if k != 'content' and a[k] != c.get(k): print('field differs', a['name'], k, a[k], c.get(k)); bad += 1
    sa, sc = skeleton(a.get('content') or ''), skeleton(c.get('content') or '')
    if sa != sc:
        bad += 1; print('SKELETON DIFF', a['name'])
print('prompt field/skeleton problems:', bad)
lcs = [p for p in C['prompts'] if p['name'].startswith('🧠 The Logic Core')]
def body(t):  # content after the leading comment+trim
    import re
    return re.sub(r'^\{\{//(?:(?!\}\}).)*\}\}(\{\{trim\}\})?', '', t, flags=re.S)
print('Chibi Logic Cores identical after comments:', body(lcs[0]['content']) == body(lcs[1]['content']), [p['name'] for p in lcs])
jb = [p for p in C['prompts'] if p['name'].startswith('🔓')][0]['content']
print('JB backslash:', '\\' in jb, '| real newline inside setvar:', '\n' in jb.split('{{setvar::ariaJb::')[1])
print('JB tail:', repr(jb[jb.find('{{#if'):]))
print('impersonation_prompt A:', repr(A.get('impersonation_prompt'))); print('impersonation_prompt C:', repr(C.get('impersonation_prompt')))
