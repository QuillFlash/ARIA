import sys
sys.path.insert(0,'.')
from lc import *
t = dict(
 cue = 'Begin with {{getvar::ariaThinkOpen}}, then {{getvar::logicCoreLines}} dashed lines, go and {{getvar::ariaThinkClose}}; the reply follows.',
 head_on = '{{getvar::ariaThinkOpen}} opens the reply, then {{getvar::logicCoreLines}} dashed lines, then go.',
 head_off = 'Reasoning is {{getvar::logicCoreLines}} dashed lines, then go.',
 frag = 'Lines are fragments paraphrasing speech, never reply sentences or drafts; each builds on the last and is settled once written; all shorter than one reply paragraph',
 frag_on = '; go ends the thinking',
 ooc = 'notes or none; a question gets only an OOC answer, no header or ledger; commands shape the reply.',
 scene = 'positions; held items; last event; card-true wants and pronouns; card gaps filled once.',
 knows = "what each acting character perceived or was told, never narration or {{user}}'s head; secrets kept.",
 voice_a = "per speaker, the card's resting mood against VAD; want and feeling now, {{user}}'s move landing first as an act",
 voice_b = '; register and address; native words.',
 move = "one beat; each character's next act, helping or holding still included; the result; the stop point.",
 fresh = 'one or two details new to the chat, seen or heard, tied to an act; card features only when the scene turns to them.',
 check = 'lists of one or two; any joke small and card-true; sincere moments plain.',
 tail_on = '{{getvar::ariaThinkClose}} closes on the line after go. The reply starts on the line after that:',
 tail_off = 'Reasoning ends at go. The reply:',
 reply_a = 'header if <header_instructions>; flowing paragraphs, the plan blended in, never one per plan line',
 reply_b = 'Nothing above go enters the reply.',
)
s = body(t)
report(s,'cand1')
r,_ = render(s)
for ln in r.split('\n'): print(f'{len(ln):4} | {ln}')
