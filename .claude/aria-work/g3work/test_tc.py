"""In-memory wiring test for TC: the snapshot TC with my post_history Logic Core part and a stand-in JB, through the frozen checker."""
import json, sys, io, contextlib
sys.path.insert(0,'/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
S='/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/'
src=S+"chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
draft=sys.argv[1] if len(sys.argv)>1 else S+'g3work/G3.try.json'
mode=sys.argv[2] if len(sys.argv)>2 else 'jb'
preset=json.load(open(src,encoding='utf-8'))
g3=json.load(open(draft,encoding='utf-8'))
sp=preset['sysprompt']
ph=sp['post_history']; i=ph.index('<final_gate>')
sp['post_history']=g3['tc']['post_history_logic_core']+ph[i:]
if mode=='jb':
    jb=json.load(open(S+'jb/final.json',encoding='utf-8'))
    c=sp['content']
    c=c.replace('{{.aria-freaky = off}}\n','{{.aria-freaky = off}}\n{{// jb}}{{.aria-jailbreak = off}}\n',1)
    c=c.replace('{{setvar::ariaPatchJoins::}}\n','{{setvar::ariaPatchJoins::}}{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}\n',1)
    block='{{#if .aria-jailbreak}}{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}{{/if}}'%(len(jb['lines']),'\n'.join(jb['lines']))
    c=c.replace('{{/if}}{{#if .aria-hybrid-pov}}',  '{{/if}}'+block+'{{#if .aria-hybrid-pov}}',1)
    sp['content']=c
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    totals,errors=ab.analyse_tc(preset)
print(buf.getvalue()[-900:])
print('totals',totals)
print('errors',errors)
