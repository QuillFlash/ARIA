import sys, itertools, importlib.util
spec=importlib.util.spec_from_file_location('tryfile','/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/g3work/try.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
from lc import *
N='{{getvar::logicCoreLines}}'
# slot: list of (text, penalty)
slots = {
 'head_off': [('Reasoning: '+N+' dashed lines, then go.',0), ('Reasoning: '+N+' lines, then go.',1.0), ('Reasoning: '+N+' lines, go.',2.5)],
 'frag': [
   ('Fragments paraphrase speech, never reply sentences or drafts; settled once written; all under one reply paragraph',0),
   ('Fragments paraphrase speech, not reply sentences or drafts; settled once written; under one reply paragraph',0.5),
   ('Fragments paraphrase speech, not reply sentences/drafts; settled once written; under one reply paragraph',0.8),
   ('Fragments paraphrase speech, not reply sentences/drafts; settled once written; under a reply paragraph',1.3)],
 'ooc': [
   ('notes or none; a question gets only an OOC answer, no header/ledger; commands shape the reply.',0),
   ('notes or none; questions get only OOC answer, no header/ledger; commands shape reply.',0.7),
   ('notes or none; question: only OOC answer, no header/ledger; commands shape reply.',1.0),
   ('notes/none; question: only OOC answer, no header/ledger; commands shape reply.',1.3)],
 'scene': [("positions; held items; last event; card wants/pronouns; gaps filled once.",0)],
 'knows': [
   ("what each character perceived or was told, not narration/{{user}}'s head; secrets kept.",0),
   ("what each perceived or was told, not narration/{{user}}'s head; secrets kept.",0.7)],
 'voice': [
   ("per speaker, card resting mood vs VAD; want/feeling now, {{user}}'s move lands first as an act{EXTRA}; register/address; native words.",0),
   ("per speaker, card mood vs VAD; want/feeling now, {{user}}'s move lands first as an act{EXTRA}; register/address; native words.",0.6),
   ("per speaker, card mood vs VAD; want/feeling now, {{user}}'s move lands first as act{EXTRA}; register/address; native words.",1.2)],
 'move': [
   ("one beat; each character's next act, help or hold included; result; stop point.",0),
   ("one beat; everyone's next act, help/hold too; result; stop point.",0.8)],
 'fresh': [
   ('1-2 new details, seen/heard, tied to an act; card features only when scene turns to them.',0),
   ('1-2 new, seen/heard, tied to an act; card features only when scene turns to them.',0.8),
   ('1-2 new, seen/heard, tied to an act; card features only if scene turns to them.',1.0),
   ('1-2 new, seen/heard, tied to act; card features only if scene turns to them.',1.8)],
 'check': [
   ('lists 1-2; small card-true jokes; sincere plain.',0),
   ('lists 1-2; small jokes; sincere plain.',1.5)],
 'reply_a': [
   ('header if <header_instructions>; plan blended in, never a paragraph per plan line',0),
   ('header if <header_instructions>; plan blended in, no paragraph per plan line',0.6)],
}
def build(choice):
    t = dict(m.BASE)
    t['head_off']=choice['head_off'][0]
    t['frag']=choice['frag'][0]
    t['ooc']=choice['ooc'][0]
    t['scene']=choice['scene'][0]
    t['knows']=choice['knows'][0]
    v=choice['voice'][0].split('{EXTRA}')
    t['voice_a']=v[0]; t['voice_b']=v[1]
    t['move']=choice['move'][0]
    t['fresh']=choice['fresh'][0]
    t['check']=choice['check'][0]
    t['reply_a']=choice['reply_a'][0]
    return t
names=list(slots)
best=[]
for combo in itertools.product(*[slots[n] for n in names]):
    choice=dict(zip(names,combo))
    pen=sum(c[1] for c in combo)
    s=body(build(choice))
    r,_=render(s)
    best.append((pen,len(r),choice))
ok=[b for b in best if b[1]<=880]
ok.sort(key=lambda b:(b[0],b[1]))
print('combos',len(best),'ok',len(ok))
for pen,L,ch in ok[:5]:
    print('PEN',pen,'LEN',L)
    for k,v in ch.items(): print('  ',k,':',v[0])
