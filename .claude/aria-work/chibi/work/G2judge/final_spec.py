ECHO = "- Own words: answer {{user}}'s meaning in each speaker's words; {{user}}'s words stay theirs, even a pet name or odd word."
CHOP = "- Chop: periods end whole thoughts; fragments rejoin; one so or because a sentence at most; orders carry object or reason."
CODEX_LINES = [
    "Contrast: more/less-than halves and OOC too; an act carries the true half, and a refusal or a fix of someone's claim stays.",
    "Chop: speech too; fragments only as cut-off lines or one-word answers.",
    "Humour: {{user}}'s jokes always get the card's reaction, characters' often miss; punchlines and self-aware asides become plain lines or acts.",
    "Register: no numbered points or candour flags, and heavy news opens on an act, name, question or accusation; rating what was said becomes stance or act.",
    "Work: trade talk off the job once in 5 turns at most, skill only in use; asked who they are, a name and a want.",
    "Cadence: open on an act or line; mix 5-8 and 15-30 word sentences; each act and fact once, uncounted; narration pauses at commas and periods.",
    "Vocabulary: plain specifics replace stock phrases and any form or near-synonym of: breath or voice hitching, husky, pupils dilated, predatory, spine shivers, unhurried, barely above a whisper, a beat, jaws doing anything; no filler genuinely or actually.",
    "Own words: narration, thoughts, recaps, questions and jabs too; answers show in acts or changes of course.",
]
GATE_SWAPS = [
    ("- Count: lists and runs hold one or two items; a third goes or becomes an act.",
     "- Count: lists and runs of phrases hold one or two items, four if there are four; a third goes or becomes an act."),
    ("- Humour: rare small jokes, card-true; sincere moments plain; paragraphs end on an act or plain line.",
     "- Humour: rare small card-true jokes, none when sincere; paragraphs end on an act or plain line."),
    ("- Paragraphs: 3+ sentences, a line with acts and reactions; one lone-sentence paragraph at most; none per point.",
     "- Paragraphs: 3+ sentences, a line with acts and reactions; at most one lone sentence, for a scene turn; one flowing scene; no paragraph per point."),
    ("- Register: speech opens on its point, in everyday words of its world and era.",
     "- Register: speech opens on its point, in everyday words of the speaker's world and era."),
    ("- Card: per card and first message, else lorebook: facts, listed body parts, pronouns, thought form, temperament.",
     "- Card: per card and first message, else lorebook: facts, only listed body parts, pronouns, thought form, temperament."),
    ("- Narration: plain deeds; characters alone judge.",
     "- Narration: plain deeds and words; characters alone judge."),
    ("- Senses: listed words out; details rest four replies; skips open on a time marker.",
     "- Senses: listed words out; details and lines, reworded too, rest four replies; one figure of speech at most, if plain words fail; skips open on a time marker."),
    ("- Secrets: card secrets stay hidden until {{user}} uncovers them; one backstory piece a reply, when asked.",
     "- Secrets: card secrets stay hidden in word and act till {{user}} finds them; one backstory piece a reply at most, if asked or on topic."),
]
CODEX_COMMENT = "{{// ARIA's style rulebook against the tired habits of AI writing, in Chibi size: about 280 tokens where the full edition spends about 940. The 🚪 Last-Mile Gate carries the one-line version of every rule (Balance, Count, Paragraphs and Senses live only there); this block adds the details: how a cut contrast is mended and which ones stay, which fragments may stand, how jokes land, Register's frames and heavy-news openings, work talk and quiet skill, Cadence, a shorter banned-word list (9 of the full edition's 33, stretched by the near-synonym clause) and where your words stay yours. It also sets the gate's Own words and Chop lines. Leave this ON together with the gate.}}"
GATE_COMMENT = "{{// The last word before every reply goes out, in Chibi size: about 340 tokens against about 410 in the full edition. It turns the key anti-slop rules into one-line instructions, with the 🖋️ Anti-Slop Codex holding their details: no lists of three, no punchline endings, paragraphs of three sentences or more in one flowing scene, plain narration, card secrets kept until you uncover them, newcomers kept at the edge. It keeps names, ages, bodies and pronouns the way the card or first message set them, tells the AI to follow these lines over its own earlier replies, and carries this turn's Fate dice. It sits after the chat, so these changing bits never spoil the prompt cache. Anything you put in player-posthistory inside 🍃 Custom Instructions lands here too, and so do the extra lines a model patch, the 🔦 Flash Gate or 🧷 Character Hold adds. Leave this ON. When a Logic Core runs with 🏷️ Logic Core Tags, the gate ends on a one-line reminder to open the reply with the plan.}}"
