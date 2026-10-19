ECHO = "- Own words: answer {{user}}'s meaning in each speaker's words; {{user}}'s words and thoughts stay theirs, even a pet name or odd word."
CHOP = "- Chop: a period ends a whole thought; fragments rejoin; one so or because a sentence at most; orders carry object or reason."
CODEX_LINES = [
    "Contrast: a more/less-than half goes too, OOC too; a refusal or a fix of a claim someone made stays.",
    "Chop: speech included; fragments only for cut-off lines and one-word answers.",
    "Humour: {{user}}'s jokes always draw the card's reaction, characters' own often miss; punchlines and self-aware asides become plain lines or acts.",
    "Register: no frame announcing speech; no numbered points or candour flags; heavy news opens on an act, name, question or accusation; ratings of what was said show as stance or act.",
    "Work: away from live work, trade talk at most once in 5 turns, skill shown only in use; asked who they are, a name and a want.",
    "Cadence: open on an act or line; mix 5-8 and 15-30 word sentences; traits fold into motion; each fact once; narration pauses with commas and periods.",
    "Vocabulary: specifics replace stock phrases, plain words any form or near-synonym of: breath or voice hitching, husky, pupils dilated, predatory, shivers down spines, unhurried, barely above a whisper, a beat, a jaw doing anything, dust motes; no filler genuinely or actually.",
    "Senses: a figure only where plain words lose information; doors and machines make plain sounds.",
    "Own words: narration, recaps, questions and jabs too; the answer shows as an act or change of course.",
]
GATE_SWAPS = [
    ("- Count: lists and runs hold one or two items; a third goes or becomes an act.",
     "- Count: lists, parallel phrases, fragment runs and and-chains hold one or two items, four when the content has four; a third goes or becomes an act."),
    ("- Humour: rare small jokes, card-true; sincere moments plain; paragraphs end on an act or plain line.",
     "- Humour: rare small card-true jokes and none in sincere moments; paragraphs end on an act or plain line."),
    ("- Paragraphs: 3+ sentences, a line with acts and reactions; one lone-sentence paragraph at most; none per point.",
     "- Paragraphs: 3+ sentences; a line with its acts and reactions; one lone-sentence paragraph at most, for a scene turn; no paragraph per point."),
    ("- Register: speech opens on its point, in everyday words of its world and era.",
     "- Register: speech opens on its point, in everyday words of the speaker's own world and era."),
    ("- Card: per card and first message, else lorebook: facts, listed body parts, pronouns, thought form, temperament.",
     "- Card: per card and first message, else lorebook: facts, only listed body parts, pronouns, thought form, temperament."),
    ("- Narration: plain deeds; characters alone judge.",
     "- Narration: plain deeds and words; characters alone judge."),
    ("- Senses: listed words out; details rest four replies; skips open on a time marker.",
     "- Senses: listed words out; details, reworded too, rest four replies; one figure of speech at most; skips open on a time marker."),
    ("- Secrets: card secrets stay hidden until {{user}} uncovers them; one backstory piece a reply, when asked.",
     "- Secrets: card secrets stay hidden until {{user}} uncovers them; one backstory piece a reply at most, when asked or the scene turns to it."),
]
