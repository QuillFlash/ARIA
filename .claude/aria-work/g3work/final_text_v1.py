"""Final wording pieces for the Chibi Logic Core (G3). Used by build_g3.py."""
N = '{{getvar::logicCoreLines}}'
OPEN = '{{getvar::ariaThinkOpen}}'
CLOSE = '{{getvar::ariaThinkClose}}'

T = dict(
 # Tags-on sentences stay word for word (the echo-cleaning regex scripts match them)
 cue = f'Begin with {OPEN}, then {N} dashed lines, go and {CLOSE}; the reply follows.',
 head_on = f'{OPEN} opens the reply, then {N} dashed lines, then go.',
 head_off = f'Reasoning: {N} lines, then go.',
 frag = 'Fragments paraphrase speech, not reply sentences/drafts; settled once written; under one reply paragraph',
 frag_on = '; go ends the thinking',
 ooc = 'notes/none; question: only OOC answer, no header/ledger; commands shape reply.',
 scene = 'positions; held items; last event; card wants/pronouns; gaps filled once.',
 knows = "what each perceived or was told, not narration/{{user}}'s head; secrets kept.",
 voice_a = "per speaker, card mood vs VAD; want/feeling now, {{user}}'s move lands first as an act",
 voice_b = '; register/address; native words.',
 move = "one beat; everyone's next act, help/hold too; result; stop point.",
 fresh = '1-2 new, seen/heard, tied to an act; card features only if scene turns to them.',
 check = 'lists 1-2; small jokes; sincere plain.',
 tail_on = f'{CLOSE} closes on the line after go. The reply starts on the line after that:',
 tail_off = 'Reply:',
 reply_a = 'header if <header_instructions>; plan blended in, never a paragraph per plan line',
 reply_b = 'Nothing above go enters the reply.',
)
