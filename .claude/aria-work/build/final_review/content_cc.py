import json
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"; W = R + "/.claude/aria-work"
A = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"))
C = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"))
pa = {p['identifier']: p for p in A['prompts']}; pc = {p['identifier']: p for p in C['prompts']}
final = {}
for g in ['G1', 'G2', 'G3', 'G4', 'G5', 'G6']:
    d = json.load(open(f'{W}/chibi/final/{g}.json'))
    for pid, p in d['prompts'].items():
        assert pid not in final, pid
        final[pid] = (g, p['content'])
jb = json.load(open(f'{W}/chibi/final/JB.json'))
jbid = [p for p in pc if pc[p]['name'].startswith('🔓')][0]
final[jbid] = ('JB', jb['cc_comment'] + '{{trim}}\n{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::' + '\n'.join(jb['lines']) + '}}{{/if}}')
cc_rev = json.load(open(W + '/build/review_cc_changes.json'))
same_as_aria, ok, bad = [], 0, []
for pid, p in pc.items():
    if pid in final:
        g, want = final[pid]
        if pid == 'main':
            want = want.replace('{{setvar::ariaJbLines::}}', '{{setvar::ariaJbLines::}}{{setvar::gemini38Patch::}}', 1)
        for ch in cc_rev['changes']:
            if ch['identifier'] == pid:
                want = want.replace(ch['old'], ch['new'])
        if p.get('content') == want: ok += 1
        else: bad.append((g, p['name']))
    else:
        same_as_aria.append((p['name'], p.get('content') == pa[pid].get('content')))
print('equal to final:', ok, '| differing:', bad)
print('not in finals (must equal ARIA):', same_as_aria)
