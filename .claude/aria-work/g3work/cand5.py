import sys
sys.path.insert(0,'.')
from lc import *
t = dict(
 cue = 'Begin with {{getvar::ariaThinkOpen}}, then {{getvar::logicCoreLines}} dashed lines, go and {{getvar::ariaThinkClose}}; the reply follows.',
 head_on = '{{getvar::ariaThinkOpen}} opens the reply, then {{getvar::logicCoreLines}} dashed lines, then go.',
 head_off = 'Reasoning: {{getvar::logicCoreLines}} dashed lines, then go.',
 frag = 'Fragments paraphrase speech, not reply sentences or drafts; settled once written; all under one reply paragraph',
 frag_on = '; go ends the thinking',
 ooc = 'notes or none; question gets only OOC answer, no header/ledger; commands shape reply.',
 scene = "positions; held items; last event; card wants/pronouns; gaps filled once.",
 knows = "what each character perceived or was told, not narration/{{user}}'s head; secrets kept.",
 voice_a = "per speaker: card resting mood vs VAD; want/feeling now, {{user}}'s move landing first as an act",
 voice_b = '; register/address; native words.',
 move = "one beat; each character's next act, help/hold too; result; stop point.",
 fresh = '1-2 new details, seen/heard, tied to an act; card features only when scene turns to them.',
 check = 'lists of 1-2; jokes small, card-true; sincere plain.',
 tail_on = '{{getvar::ariaThinkClose}} closes on the line after go. The reply starts on the line after that:',
 tail_off = 'Reply:',
 reply_a = 'header if <header_instructions>; plan blended in, never one paragraph per plan line',
 reply_b = 'Nothing above go enters the reply.',
)
s = body(t)
report(s,'cand5')
r,_ = render(s)
for ln in r.split('\n'): print(f'{len(ln):4} | {ln}')
