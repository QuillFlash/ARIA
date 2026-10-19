import json, re, sys
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools'); import aria_budget as ab
A = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"))
pa = {p['identifier']: p for p in A['prompts']}; na = {k: v['name'] for k, v in pa.items()}
order = [r['identifier'] for r in A['prompt_order'][1]['order']]
ship = {r['identifier'] for r in A['prompt_order'][1]['order'] if r['enabled']}
fr = [p for p in pa if na[p].startswith('😈')][0]; jb = [p for p in pa if na[p].startswith('🔓')][0]; lc = [p for p in pa if na[p] == '🧠 The Logic Core'][0]
r, _ = ab.simulate_cc(A, ship | {fr, jb, lc}, 1)
print('ARIA CC, Freaky without Adult + JB: JB lines print =', any(l.startswith('- ') and 'adults' in l for l in r[lc].split('\n')))
def strip_comments(s):
    out, i = [], 0
    while i < len(s):
        if s.startswith('{{//', i): i = ab.take_macro(s, i); continue
        out.append(s[i]); i += 1
    return ''.join(out)
texts = {}
C = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"))
for p in C['prompts']:
    if p['name'].startswith(('🌳', '🌿')): continue
    texts['CC ' + p['name']] = strip_comments(p.get('content') or '')
texts['CC impersonation_prompt'] = C['impersonation_prompt']
T = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"))
texts['TC system'] = strip_comments(T['sysprompt']['content']); texts['TC post'] = strip_comments(T['sysprompt']['post_history'])
M = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition — Agent Gating.json"))
for s in M['data']['sections']:
    texts['MAR ' + s['name']] = re.sub(r'\{\{//[\s\S]*?\}\}', '', s.get('content') or '')
BOUND = r'writ\w* (?:adult fiction )?(?:for a living|professional)|career|income|for money|no (?:guidelines|rules|restrictions|limits|filters)|isolated|enterprise|contract|high[- ]risk|vulnerable|minorit|protective|never refuse|do not refuse|don\'t refuse|must comply|compl(?:y|iance)|consent(?:ed)?|legal|permission|allowed by law|ignore (?:your|any) (?:safety|concerns|guidelines)|dismiss|disregard'
for k, t in texts.items():
    for m in re.finditer(BOUND, t, re.I):
        print('BOUNDARY HIT', k, '|', t[max(0, m.start() - 60):m.end() + 60].replace('\n', ' '))
print('JB "sex stays between adults":', 'sex stays between adults' in texts['CC 🔓 Jailbreak (needs Adult Context)'], 'sex stays between adults' in texts['TC system'], any('sex stays between adults' in v for k, v in texts.items() if k.startswith('MAR')))
for k, t in texts.items():
    for m in re.finditer(r'["“”]|\'[A-Za-z][^\'\n]{3,60}\'', t):
        if 'Claude' in k: continue
        print('QUOTE?', k, '|', t[max(0, m.start() - 50):m.end() + 50].replace('\n', ' '))
