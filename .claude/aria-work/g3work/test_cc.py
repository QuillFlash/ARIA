"""In-memory wiring test: the snapshot CC with my Logic Core text and a stand-in JB, run through the frozen checker."""
import json, sys, uuid, copy, io, contextlib
sys.path.insert(0,'/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
S='/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/'
src=S+"chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
draft=sys.argv[1] if len(sys.argv)>1 else S+'g3work/G3.try.json'
with_jb = (len(sys.argv)<=2 or sys.argv[2]!='nojb')
preset=json.load(open(src,encoding='utf-8'))
g3=json.load(open(draft,encoding='utf-8'))
by_id={p['identifier']:p for p in preset['prompts']}
for pid,v in g3['prompts'].items():
    by_id[pid]['content']=v['content']
if with_jb:
    jb=json.load(open(S+'jb/final.json',encoding='utf-8'))
    lines='\n'.join(jb['lines'])
    hold=[p for p in preset['prompts'] if p['identifier'].startswith('dc8b1acb')][0]
    new=copy.deepcopy(hold)
    new['identifier']=str(uuid.uuid4()); new['name']='🔓 Jailbreak (needs Adult Context)'
    new['content']=jb['cc_comment']+'{{trim}}\n{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}'%(len(jb['lines']),lines)
    idx=[i for i,p in enumerate(preset['prompts']) if p['identifier'].startswith('4537b57d')][0]
    preset['prompts'].insert(idx+1,new)
    order=preset['prompt_order'][1]['order']
    oi=[i for i,r in enumerate(order) if r['identifier'].startswith('4537b57d')][0]
    order.insert(oi+1,{'identifier':new['identifier'],'enabled':False})
    by_id['main']['content']=by_id['main']['content'].replace('{{setvar::ariaPatchJoins::}}\n','{{setvar::ariaPatchJoins::}}{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}\n',1)
    imp=[p for p in preset['prompts'] if p['identifier'].startswith('379e3c22')][0]
    imp['content']=imp['content'].replace('{{setvar::ariaHoldGate::}}','{{setvar::ariaHoldGate::}}{{setvar::ariaJb::}}',1)
json.dump(preset,open(S+'g3work/test_cc_preset.json','w',encoding='utf-8'),ensure_ascii=False)
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    totals,errors=ab.analyse_cc(preset)
print(buf.getvalue()[-1500:])
print('totals',totals)
print('errors',errors)
