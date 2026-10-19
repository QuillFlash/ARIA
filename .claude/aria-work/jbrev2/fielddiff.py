import json, subprocess, sys, difflib
ROOT = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
FILES = {
 'CC': "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json",
 'TC': "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",
 'MAR': "Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json",
 'RX': "regex/ARIA 1.0 Regex Scripts (Text Completions).json",
}
def head(path):
    return subprocess.run(['git','-C',ROOT,'show','HEAD:'+path],capture_output=True).stdout.decode('utf-8')
def walk(a,b,path,out):
    if type(a)!=type(b):
        out.append((path,a,b)); return
    if isinstance(a,dict):
        for k in list(dict.fromkeys(list(a)+list(b))):
            if k not in a: out.append((path+'/'+k,'<MISSING>',b[k]))
            elif k not in b: out.append((path+'/'+k,a[k],'<MISSING>'))
            else: walk(a[k],b[k],path+'/'+k,out)
        if [k for k in a if k in b]!=[k for k in b if k in a]: out.append((path+' KEYORDER',list(a),list(b)))
    elif isinstance(a,list):
        if len(a)!=len(b):
            out.append((path+' LEN',len(a),len(b)))
            # try align by identifier
            ida=[x.get('identifier') or x.get('id') if isinstance(x,dict) else None for x in a]
            idb=[x.get('identifier') or x.get('id') if isinstance(x,dict) else None for x in b]
            if all(ida) and all(idb):
                for i,x in enumerate(b):
                    k=idb[i]
                    if k in ida: walk(a[ida.index(k)],x,path+f'[{k}]',out)
                    else: out.append((path+f'[NEW {k} at {i}]','<MISSING>',x))
                return
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,path+f'[{i}]',out)
    else:
        if a!=b: out.append((path,a,b))
for tag,fn in FILES.items():
    old=json.loads(head(fn)); new=json.load(open(ROOT+'/'+fn,encoding='utf-8'))
    out=[]; walk(old,new,tag,out)
    print('=====',tag,len(out),'diffs')
    for p,a,b in out:
        print('--',p)
        if isinstance(a,str) and isinstance(b,str):
            sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
            for op,i1,i2,j1,j2 in sm.get_opcodes():
                if op!='equal':
                    ctxa=a[max(0,i1-120):i1]
                    print(f'   {op} @{i1}: before-ctx={ctxa!r}')
                    print(f'      old={a[i1:i2]!r}')
                    print(f'      new={b[j1:j2]!r}')
                    print(f'      after-ctx={a[i2:i2+80]!r}')
        else:
            print('   old=',json.dumps(a,ensure_ascii=False)[:1500])
            print('   new=',json.dumps(b,ensure_ascii=False)[:3000])
