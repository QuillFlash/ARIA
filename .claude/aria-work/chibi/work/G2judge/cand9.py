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
