import json, difflib, re
R="/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/"
O=R+".claude/aria-work/build/orig/"
pairs=[(O+"CC.json",R+"Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"),(O+"TC.json",R+"Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"),(O+"TCregex.json",R+"regex/ARIA 1.0 Regex Scripts (Text Completions).json")]
for a,b in pairs:
    A=open(a,encoding='utf-8').read().split('\n'); B=open(b,encoding='utf-8').read().split('\n')
    print(b[len(R):], 'lines', len(A), len(B))
    for t,i1,i2,j1,j2 in difflib.SequenceMatcher(None,A,B,autojunk=False).get_opcodes():
        if t=='equal': continue
        for x,y in zip(A[i1:i2],B[j1:j2]):
            sm=difflib.SequenceMatcher(None,x,y,autojunk=False)
            for tt,a1,a2,b1,b2 in sm.get_opcodes():
                if tt!='equal': print('   line',j1+1,tt, repr(x[max(0,a1-40):a2+10]), '->', repr(y[max(0,b1-40):b2+10]))
        if (i2-i1)!=(j2-j1): print('   LINE COUNT CHANGE', t, i1,i2,j1,j2)
files={"ARIA CC":R+"Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json","ARIA TC":R+"Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json","Chibi CC":R+"Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json","Chibi TC":R+"Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json","regex":R+"regex/ARIA 1.0 Regex Scripts (Text Completions).json"}
for k,f in files.items():
    raw=open(f,encoding='utf-8').read(); d=json.loads(raw)
    print(k,'indent4 roundtrip', json.dumps(d,ensure_ascii=False,indent=4)==raw, '| trailing NL', raw.endswith('\n'), '| CR', '\r' in raw, '| \\u escapes', bool(re.search(r'\\u[0-9a-fA-F]{4}', raw)))
for k,f in {"ARIA Mar":R+"Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json","Chibi Mar":R+"Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition — Agent Gating.json"}.items():
    raw=open(f,encoding='utf-8').read(); d=json.loads(raw)
    print(k,'tab roundtrip', json.dumps(d,ensure_ascii=False,indent='\t')==raw, '| trailing NL', raw.endswith('\n'))
