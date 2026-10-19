import json
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/"
A = json.load(open(R + "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"))
C = json.load(open(R + "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"))
print('regex identical:', A['extensions']['regex_scripts'] == C['extensions']['regex_scripts'])
na = {p['identifier']: p.get('name') for p in A['prompts']}
oa = [(r['identifier'], r['enabled']) for r in A['prompt_order'][1]['order']]
oc = [(r['identifier'], r['enabled']) for r in C['prompt_order'][1]['order']]
print('same order ids:', [i for i, _ in oa] == [i for i, _ in oc])
for (i, e), (j, f) in zip(oa, oc):
    print(('  ' if e == f else '* ') + str(na.get(i, i)), e, f)
print('names same:', {p['identifier']: p.get('name') for p in A['prompts']} == {p['identifier']: p.get('name') for p in C['prompts']})
for k in ['name', 'role', 'injection_position', 'injection_depth', 'injection_order', 'injection_trigger']:
    diffs = [p['identifier'] for p in C['prompts'] if {q['identifier']: q for q in A['prompts']}[p['identifier']].get(k) != p.get(k)]
    print(k, 'diffs', diffs)
print('other top-level keys differing:', [k for k in A if k not in ('prompts', 'prompt_order', 'extensions') and A[k] != C.get(k)])
