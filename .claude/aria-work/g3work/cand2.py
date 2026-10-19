import sys
sys.path.insert(0,'.')
from lc import *
t = dict(
 cue = 'Begin with {{getvar::ariaThinkOpen}}, then {{getvar::logicCoreLines}} dashed lines, go and {{getvar::ariaThinkClose}}; the reply follows.',
 head_on = '{{getvar::ariaThinkOpen}} opens the reply, then {{getvar::logicCoreLines}} dashed lines, then go.',
 head_off = 'Reasoning: {{getvar::logicCoreLines}} dashed lines, then go.',
 frag = 'Fragments paraphrase speech, never reply sentences or drafts; each builds on the last, settled once written; all shorter than one reply paragraph',
 frag_on = '; go ends the thinking',
 ooc = 'notes or none; a question gets only an OOC answer, no header/ledger; commands shape the reply.',
 scene = 'positions; held items; last event; card wants and pronouns; card gaps filled once.',
 knows = "what each acting character perceived or was told, not narration or {{user}}'s head; secrets kept.",
 voice_a = "per speaker, card resting mood vs VAD; want and feeling now, {{user}}'s move landing first as an act",
 voice_b = '; register and address; native words.',
 move = "one beat; each character's next act, help or hold included; result; stop point.",
 fresh = '1-2 details new to the chat, seen or heard, tied to an act; card features only when the scene turns to them.',
 check = 'lists of 1-2; any joke small, card-true; sincere moments plain.',
 tail_on = '{{getvar::ariaThinkClose}} closes on the line after go. The reply starts on the line after that:',
 tail_off = 'Reasoning ends at go. Reply:',
 reply_a = 'header if <header_instructions>; flowing paragraphs, plan blended in, never one per plan line',
 reply_b = 'Nothing above go enters the reply.',
)
s = body(t)
report(s,'cand2')
r,_ = render(s)
for ln in r.split('\n'): print(f'{len(ln):4} | {ln}')
