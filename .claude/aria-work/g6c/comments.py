# Chibi comments for group G6. {placeholders} are filled with measured token figures by build.py.
# No "}}" or "{{" may appear inside a comment (the macro parser would end it early).

C = {}

C['b59a2ad1'] = (
    "🩹 Chibi Claude 5 patch, for Claude 5 models (Fable, Opus, Sonnet), in about {claude} tokens where the full edition spends 112. "
    "It bans their pet words (file X away, structural failure, architectural, geometry), allows data talk only for tech-minded cards and net slang only for very online ones, "
    "and shows four short before-and-after repairs: a true line answered with a bigger one, a not-this-but-that line, a chopped fragment run and an approval rating like 'I respect that'. "
    "They are the only examples in the preset, because every other model copies quoted examples word for word. Chibi folded the approval rule into the repairs and shortened each one. "
    "Use one model patch at most."
)

C['333dbbed'] = (
    "🩹 Chibi Gemini 3.8 Flash patch: the Flash-only method for when conflict scenes start sounding formal and cold, in about {g38} tokens where the full edition spends 106. "
    "Each speaker's want and feeling come from the card and the last event and are voiced in their own vocabulary and rhythm, avoided and overused words included; every line pursues the want and reactions fit their cause. "
    "It prints through the 🩹 Gemini All-In-One patch, so switch that ON alongside it. Gemini 4 Argon is smart enough not to need it."
)

C['ac96376e'] = (
    "🩹 Chibi Gemini All-In-One patch, for Gemini, in about {aio_own} tokens of text plus two plan and gate lines (about {aio_gate} tokens) where the full edition spends 108 and 52. "
    "Gemini over-applies ARIA's rule against choppy sentences and strings everything together with 'so' and 'because', so a Speech line takes the place of the gate's Chop line: short everyday sentences, one thought each. "
    "The Gemini line keeps the card's nerves and humour at their usual size, answers a feelings question with the feeling itself and keeps forecasts and closing lines to one outcome; "
    "the text keeps the <scene_engine> question and counsellor limits even when invited (only counselor cards lift them) and shows places and bodies the way someone in the room would notice them. "
    "Gemini 4 Argon kept setting the real word against a 'not this' beside it, so the Contrast line cuts that half, runs, dash-led parts and speech included, while refusals and denials stay; "
    "Chibi moved that full rule out of the system text into the plan and gate line. Switch 👃 Scent Occasions OFF as well. Use one model patch at most."
)

C['1f2e1f97'] = (
    "🩹 Chibi GLM patch, for GLM 5.x, Flash included: five lines at the end of the 🚪 Last-Mile Gate, where GLM listens best, and in the plan, about {glm_lines} tokens where the full edition spends 292. "
    "Everyone is a person, not an assistant (helping, praising, advising or comforting you only as far as the card and their bond allow); the answer covers your whole move, a true line keeps its size and the answer moves on; "
    "steadying filler becomes the thought itself, and one may stay when answering someone. Two lines were confirmed live on GLM 5.3 Flash and keep every mechanic. "
    "Pushback: a not-this sentence or clause beside the real one is cut, a denial or a fix of a word you used included (the 🖋️ Anti-Slop Codex lets those stand), and so is any clause saying what your view or the speaker's last line is not, while a refusal stays a plain no. "
    "Restate: a sentence or clause that repeats the line before (intensifier or not) or only labels it is cut, and so is a phrase anywhere that marks a speech as on the record, honest, clear or said first, which the gate's Register line misses because it only checks how speech opens; nervous characters still stammer. "
    "To fit, Chibi left out Person's 'agree or push back as the card would', Replies' 'one flowing scene, the part the character cares about most first' and Pushback's separate 'plain fact' sentence, which is now one clause. "
    "Native thinking stays one quick pass through The Logic Core's lines. GLM Flash users switch 🔦 Flash Gate ON too. Use one model patch at most."
)

C['9bb6c2b0'] = (
    "🩹 Chibi Kimi / Qwen patch, for Kimi and Qwen, in about {kq_own} tokens of text plus one gate line (about {kq_gate}) where the full edition spends 54 and 32. "
    "Calls to action run at least two words, and native thinking stays one quick pass through The Logic Core's lines. "
    "Its Filler line sits at the end of the 🚪 Last-Mile Gate, the spot where Realistic Frankenstein put its GLM fix: the filler word these models put in characters' mouths before every decision becomes the thought or an act, and one may stay when answering someone. "
    "GLM has a patch of its own. Use one model patch at most."
)

C['33f92483'] = (
    "🩹 Chibi MiMo V2.6 Pro patch, in about {mp_own} tokens of text plus one gate line (about {mp_gate}) where the full edition spends 93 and 19. "
    "It brings back each character's usual mood and interests, keeps secrets to their own topic, keeps names, colours, values and filled gaps the way the chat first set them, "
    "and stops counts, ages, images and paragraph layouts from coming back unless the story changed them. It also hands its Contrast line to the 🚪 Last-Mile Gate and to the plan. "
    "Run it with 🏷️ Logic Core Tags ON and native reasoning off; if no plan shows up, switch to the system-role twin of The Logic Core. MiMo V2.6 Flash uses 🩹 MiMo V2.6 Flash instead. Use one model patch at most."
)

C['3a027832'] = (
    "🩹 Chibi MiMo V2.6 Flash patch, for the model u/trashhaul caught writing slop the Pro patch couldn't stop, in about {mf_own} tokens of text plus three plan and gate lines (about {mf_gate}) where the full edition spends 235 and 104. "
    "Newcomers give a name and one reason for being here, and the rest of their card shows later through what they do. A run of 'not this, not that' before the real word shrinks to the real word, and narration sentences keep their own subject and verb and run five words or more. "
    "Characters react to what actually happened rather than to what kind of talk it is, and names, colours and values stay as first set. "
    "Chibi moved the Contrast, Flow and Introductions rules out of the system text into their plan and gate lines (the speech exceptions of Flow are left to the Codex's Chop rule). "
    "Switch 🔦 Flash Gate ON too, since it carries the rule against repeated demands, keep 🏷️ Logic Core Tags ON with native reasoning off, and try Temperature 0.8. MiMo V2.6 Pro uses 🩹 MiMo V2.6 Pro instead. Use one model patch at most."
)

C['e04b9c2b'] = (
    "🩹 Chibi DeepSeek patch, for DeepSeek V4, Pro and Flash. Native thinking stays one short pass through The Logic Core's lines, under 150 words with no rule audits, since DeepSeek otherwise thinks for a minute or two before every reply and writes worse the longer it thinks. "
    "u/BSPiotr caught it saying your words back to you and replaying the same fact or beat for several turns, and V4 Pro gave a character a tail her card never mentioned, so three lines go to the 🚪 Last-Mile Gate and into the plan (Echo, Repeats, Bodies, about {ds_gate} tokens). "
    "V4 Pro (0813) also writes in fragments, so a Joins line (about {ds_joins}) joins every short sentence after a reply's first and folds a one-sentence paragraph into the one before it when the same voice carries on, while stalls, cut-offs and one-word answers stay. "
    "With 🔦 Flash Gate ON, as Flash users run it, Joins and the Flash Gate's Runs line both stay out, so Flash's prose stays as it was. "
    "With 🥰 Bonds Lite or 🎲 Fate & Chekhov Ledger ON, the plan also gets a Tally line (about {ds_tally} tokens with both): DeepSeek V4.1 Flash left Sparks, Grudge and BOND at their starting numbers turn after turn, so Tally has it write each pair's old numbers, "
    "name this turn's listed acts, slights and sincere repair, add Sparks (max 2, half while Grudge is 3 or more), add Grudge (a repair clears it), turn 7 Sparks into BOND +1 and 5 Grudge into BOND -1, and write the new numbers, then update the 🎲 ledger's q and hp counters and its last entry. "
    "The Tally line sits outside the thinking word cap, stays in the plan and out of the 🚪 Last-Mile Gate, and is absent while both modules are off and on an Impersonate turn; it relies on Bonds Lite's rule that strangers start at 0/0/0. "
    "DeepSeek V4 and V4.1 Flash users switch 🔦 Flash Gate ON too. Use one model patch at most."
)

C['2e3e7f63'] = (
    "🔦 Chibi Flash Gate, for the Flash-tier models: GLM Flash, MiMo V2.6 Flash and DeepSeek V4 Flash, in about {fg} tokens where the full edition spends 220 (about {fg_nr} without the Runs line). "
    "They flatten characters, borrow office words like filing and notarising for feelings and repeat one demand or pet line turn after turn. "
    "This puts Realistic Frankenstein's Flash fixes at the end of the 🚪 Last-Mile Gate: the card's mood and interests hold for the whole chat, a refused demand turns into an act or a trade, "
    "and a stricter work-words rule takes the place of the gate's own Work line. The Logic Core's Voice line also gets one raw thought per speaker. "
    "A Runs line fights the drift GLM Flash and MiMo Flash show deeper into a chat: a sentence under five words stands once a reply and any further one joins its neighbour, while stalls, cut-offs, one-word answers, long paragraphs and jokes stay. "
    "With 🩹 DeepSeek ON, Runs stays out, and so does that patch's Joins line, since DeepSeek V4.1 Flash already writes solid prose. Run it alongside your model patch. It costs nothing while it's off."
)

C['dc8b1acb'] = (
    "🧷 Chibi Character Hold, for quantised providers (NanoGPT, OpenRouter auto-routing and other nodes that serve trimmed weights), in about {hold} tokens for its two lines where the full edition spends 82. "
    "u/Probablynotsocool found MiMo V2.6 Flash holding a layered card for ten or so turns on a quantised node, then flattening it: one strong beat, like a fight that wakes a survival instinct, becomes the whole character and the other traits fade. "
    "Every turn this puts the card back in front of the model. The plan gets a Layers line naming one card trait the mood fits and one it would bury, in the card's words, and both show up in the reply; "
    "the 🚪 Last-Mile Gate gets a matching line, so the reminder is the last rule the model reads. Works with any model, alongside its patch and the 🔦 Flash Gate. It costs nothing while it's off. On a full-precision provider you can usually leave it off."
)

# TC switch comments (the {{// ... }} text placed before each switch)
T = {}
T['aria-patch-glm'] = ("🩹 Chibi patch for GLM 5.x and GLM Flash: characters talk like real people, with five lines at the end of the gate and in the plan. "
    "Someone who disagrees, corrects or reassures says what they hold without first saying what your view is not or setting a 'not this' sentence beside it, even to fix a word you used, a refusal stays a plain no, "
    "and a sentence that repeats or only labels the one before it is cut, and so is a phrase marking a line as on the record, honest, clear or said first, wherever it sits. GLM Flash: pair it with aria-flash-gate. Use one patch at most.")
T['aria-patch-kimi-qwen'] = "🩹 Chibi patch for Kimi and Qwen: calls to action run two words or more, plus a Filler line. Use one patch at most."
T['aria-patch-mimo-pro'] = "🩹 Chibi patch for MiMo V2.6 Pro. Use one patch at most."
T['aria-patch-mimo-flash'] = "🩹 Chibi patch for MiMo V2.6 Flash: newcomers, stacked negation, choppy narration, topic complaints. Pair it with aria-flash-gate. Use one patch at most."
T['aria-patch-deepseek'] = ("🩹 Chibi patch for DeepSeek V4: one short pass of native thinking, no echoing your words, no replayed facts or beats, no tail or other non-human part a described body never had, "
    "and a Joins line that merges clipped sentences and one-sentence paragraphs into their neighbours (aimed at V4 Pro's chopped prose; with aria-flash-gate on, Joins and the gate's Runs line stay out). "
    "With aria-logic-core and aria-bonds or aria-fate on, a Tally line in the plan makes it do the Sparks, Grudge, BOND and 🎲 ledger arithmetic each turn. DeepSeek V4 and V4.1 Flash: pair it with aria-flash-gate. Use one patch at most.")
T['aria-flash-gate'] = ("🔦 Chibi Flash Gate for GLM Flash, MiMo V2.6 Flash and DeepSeek V4 Flash: Realistic Frankenstein's fixes for flat characters, office words in feelings and repeated demands, "
    "plus a Runs line against the clipped short sentences GLM Flash and MiMo Flash drift into deeper into a chat (left out with aria-patch-deepseek on). Use it alongside a patch.")
T['aria-character-hold'] = ("🧷 Chibi Character Hold for quantised providers (NanoGPT, OpenRouter auto-routing): every turn the plan names one card trait the mood fits and one it would bury, "
    "and the gate keeps every card trait alive, so one strong beat stops flattening the character. Works with any model and patch.")
