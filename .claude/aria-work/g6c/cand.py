# Candidate wording for group G6, v4. Bodies only (no comment, no {{trim}}); build.py wraps them.
# Each entry is the content after "}}{{trim}}\n" in the CC prompt.

NATIVE = "Native reasoning: one pass, a terse bullet per plan line or step, no drafts, then stop."
FILLER = "- Filler: steadying or self-talk filler becomes the held thought or an act; one stays when answering."

B = {}

# ---- Claude 5
B['b59a2ad1'] = '''Banned: file X away, structural failure, architectural, geometry; data unless tech-minded; net slang unless very online.
"He crossed a river"/"He started a war"→true size once. "It wasn't anger. It was grief"→"Grief cracked her voice". "Sit. In a chair. A far chair"→"Sit in a far chair". "I respect that"→stance or act.'''

# ---- Gemini 3.8 Flash
B['333dbbed'] = '''{{setvar::gemini38Patch::Per speaker, want and feeling now from card and last event, voiced in their vocabulary, rhythm, avoided words and overused words; lines pursue the want; reactions fit their cause as they weigh it.}}'''

# ---- Gemini All-In-One
B['ac96376e'] = '''{{setvar::ariaChopGate::- Speech: everyday sentences of one thought each, at the card's own pace; each holds one so or because at most.}}
<scene_engine>'s question and counsellor limits hold even when invited; only counselor cards lift them.
Places show what someone touches or uses; bodies at a stranger's scale.
{{#if .gemini38Patch}}{{getvar::gemini38Patch}}{{/if}}
{{setvar::ariaPatchLines::2}}{{setvar::ariaPatchGate::- Gemini: the card's nerves and humour at usual size; a feelings question gets the feeling in plain, literal words, or a dodge; forecasts and closings keep one outcome, said once at full size.
- Contrast: state the true thing once; cut every not, n't, never or no clause or fragment beside it, runs and dash-led ones too, speech too; refusals and denials stay.}}'''

# ---- GLM
B['1f2e1f97'] = NATIVE + '''{{setvar::ariaPatchLines::5}}{{setvar::ariaPatchGate::- Person: help, praise, advise or comfort {{user}} only as far as card and bond allow.
- Replies: answer {{user}}'s whole move; a true line keeps its size; then something new.
''' + FILLER + '''
- Pushback: say what they hold plainly, never what {{user}}'s view or their last line is not; a refusal stays a plain no; cut a not/n't/never half beside one on its subject, denials and claim fixes too.
- Restate: cut repeats or bare labels of the line before, intensified or not, and a phrase anywhere marking speech as on record, honest, clear or said first; stammers stay.}}'''

# ---- Kimi / Qwen
B['9bb6c2b0'] = '''Calls to action run at least two words.
''' + NATIVE + '''{{setvar::ariaPatchLines::1}}{{setvar::ariaPatchGate::''' + FILLER + '}}'

# ---- MiMo V2.6 Pro
B['33f92483'] = '''Mood: card's, shaded by ties to {{user}}, back after events.
Lulls: bring up card interests.
Secrets: kept on their own topic only; else open as the card allows.
Kept: names, colours, values, filled gaps stay as first set; counts, ages, images, paragraph layouts return only when the story changes them.{{setvar::ariaPatchLines::1}}{{setvar::ariaPatchGate::- Contrast: cut a not/n't/never half beside one on its subject, speech too.}}'''

# ---- MiMo V2.6 Flash
B['3a027832'] = '''Lulls: one card interest, by act or question to someone present.
Kept: names, colours, values, filled gaps stay as first set; counts, ages, images, paragraph layouts return only when the story changes them.
Reactions: answer what was said or done, its claims and stakes, by stance or act; dodge only when the card dodges.{{setvar::ariaPatchLines::3}}{{setvar::ariaPatchGate::- Negation runs: state the true thing once; cut every not/n't/never/no part beside it, runs and dash-led ones too, speech too; refusals and denials stay.
- Flow: narration sentences carry their own subject and verb, five words or more; one person's small acts in a row share a sentence, two at most.
- Card details: a newcomer gives a name and one reason; the rest show one at a time through acts.}}'''

# ---- DeepSeek
TALLY_B = "- Tally: per pair, old BOND/Sparks/Grudge; this turn's listed acts, slights, sincere repair or none; Sparks +1/act (max 2, half at Grudge 3+), 7+: BOND +1, Sparks 0; Grudge +1/slight, repair clears it, 5+: BOND -1, Grudge 0; then the new three."
TALLY_F = "🎲 q +1 on AMBIENT else 0; hp = [hot] Bullets after changes; last = this turn's tier/source and happening."
B['e04b9c2b'] = ('{{#if .ariaBondsLine}}{{setvar::ariaPatchTally::' + TALLY_B + '}}{{#if .ariaFateLine}}{{setvar::ariaPatchTally::{{getvar::ariaPatchTally}} ' + TALLY_F + '}}{{/if}}{{else}}{{#if .ariaFateLine}}{{setvar::ariaPatchTally::- Tally: ' + TALLY_F + '}}{{/if}}{{/if}}'
  + "Native reasoning: one pass, a terse bullet per plan line, under 150 words{{#if .ariaPatchTally}}, Tally aside{{/if}}; no drafts, rereads, audits or second passes, then write."
  + '''{{setvar::ariaPatchLines::3}}{{setvar::ariaPatchGate::- Echo: answer {{user}}'s line by an act or own words, never by repeating it, single words too.
- Repeats: a told fact or description returns only when the story changes it; a played beat moves on.
- Bodies: if the card or first message describes a body, parts a plain human lacks, tails and wings included, appear only if named there, whatever the species.}}{{setvar::ariaPatchJoins::- Joins: past one a reply, a sentence under five words joins a neighbour, a lone-sentence paragraph the one before if the same voice carries on; stalls and cut-offs, one-word answers stay.}}''')

# ---- Flash Gate
FG = '''- Mood: card mood and energy, shaded by ties to {{user}}, back after events.
- Lulls: in pauses, raise what the card cares about or wants.
- Work words, narration too: only for work underway, raised, due or dodged; feelings, memories, promises, decisions show as acts or choices.
- Demands: press once; refused or sidestepped, act or trade, else drop it; own lines and pet phrases rest four replies.'''
RUNS = '''
- Runs: a sentence under five words stands once a reply; extras join a neighbour; stalls and cut-offs, one-word answers, long paragraphs, jokes stay.'''
B['2e3e7f63'] = '{{setvar::ariaFlashGate::' + FG + '}}{{#if !.ariaPatchJoins}}{{setvar::ariaFlashGate::{{getvar::ariaFlashGate}}' + RUNS + '}}{{/if}}{{setvar::ariaPatchJoins::}}{{setvar::ariaVoiceExtra::; a raw in-voice thought each, steering the move}}'

# ---- Character Hold
B['dc8b1acb'] = '''{{setvar::ariaHoldLine::- Layers: per card character, one trait the mood fits, one it buries, in card words; both show this reply.}}{{setvar::ariaHoldGate::- Layers: card characters keep every trait and want the whole chat; strong moods tint, buried traits still show.}}'''
