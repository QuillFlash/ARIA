import json, re, sys, random
sys.path.insert(0,'/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/g3work')
sys.path.insert(0,'/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
S='/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/'
cc=json.load(open(S+"chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json",encoding='utf-8'))
scripts={r['scriptName']:r for r in cc['extensions']['regex_scripts']}
names=[n for n in scripts if 'echoed Logic Core' in n or 'echoed Logic Core closing' in n]
print(names)
def conv(find):
    m=re.match(r'^/(.*)/([a-z]*)$',find,re.S)
    pat,fl=m.group(1),m.group(2)
    flags=0
    if 'i' in fl: flags|=re.I
    return re.compile(pat,flags),('g' in fl)
def js_to_py_repl(s):
    return re.sub(r'\$(\d)',r'\\\1',s.replace('\\','\\\\')) if False else s
def apply(find,repl,text):
    rx,g=conv(find)
    def f(m):
        out=repl
        for i in range(1,10):
            out=out.replace('$%d'%i,m.group(i) or '' if i<=rx.groups else '')
        return out
    return rx.sub(f,text,count=0 if g else 1)
def render(s,state):
    st=dict(state); return ab.render(s,st,random.Random(1))
src=json.load(open(S+'g3work/src_g3.json',encoding='utf-8'))
mine=json.load(open(S+'chibi/drafts/G3.json',encoding='utf-8'))
state={'ariaThinkOpen':'<thinking>','ariaThinkClose':'</thinking>'}
sid='15b770cf-6049-5f3b-b25d-be09728a65d5'
for label,d in (('SOURCE',src),('MINE',mine)):
    t=render(d['prompts'][sid]['content'],state)
    # emulate a model echoing the template at the start of its reply, then real prose
    echo=t+'\n\nShe turned away from the window.'
    print('=====',label)
    for n in scripts:
        if not ('echoed Logic Core' in n): continue
        r=scripts[n]
        out=apply(r['findRegex'],r['replaceString'],echo)
        print('--',n[:80],'| placement',r['placement'])
        print(repr(out[:300]))

print('\n\n########## detailed script 1 + 3 on SOURCE / MINE / PARTIAL (tails)')
par=json.load(open(S+'chibi/drafts/G3.partial.json',encoding='utf-8'))
def strip_style(s): return re.sub(r'<details style="[^"]*"><summary style="[^"]*">','<details><summary>',s)
for label,d in (('SOURCE',src),('MINE',mine),('PARTIAL',par)):
    t=render(d['prompts'][sid]['content'],state)
    echo=t+'\n\nShe turned away from the window.'
    for n in ['ARIA - Fold an echoed Logic Core template into a Thoughts box (display only)','ARIA - Keep an echoed Logic Core template out of the prompt (all depths, cache-safe)','ARIA Impersonate - strip an echoed Logic Core template']:
        r=scripts[n]; out=apply(r['findRegex'],r['replaceString'],echo)
        print('==',label,'|',n[:60]); print(repr(strip_style(out)[-260:]))
# TC variants
tcsrc=open(S+'g3work/src_tc_lc.txt',encoding='utf-8').read()
tcmine=open(S+'g3work/draft_tc_lc.txt',encoding='utf-8').read()
st2=dict(state); st2['aria-logic-core']='on'
for label,txt in (('TC SOURCE',tcsrc),('TC MINE',tcmine)):
    t=render(txt,st2)
    echo=t+'\n\nShe turned away from the window.'
    for n in ['ARIA - Keep an echoed Logic Core template out of the prompt (all depths, cache-safe)','ARIA Impersonate - strip an echoed Logic Core template']:
        r=scripts[n]; out=apply(r['findRegex'],r['replaceString'],echo)
        print('==',label,'|',n[:60]); print(repr(out[-200:]))
