#!/usr/bin/env python3
"""Build chibi/drafts/G4.json (group G4, voice and modes) from the snapshot CC names and the texts below."""
import json
import sys

SRC = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
OUT = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/drafts/G4.json'

ENGINE_C = (
    "{{// 🎬 Chibi Voice & Scene Engine: keeps scenes moving at a human pace in about 110 tokens, where the full edition spends 271. "
    "Each reply is one beat of a want against a block, and a reply without drama counts as complete; fights take seconds and journeys hours; "
    "at most one question a reply, asked for the asker's own reasons; heavy news gets clumsy reactions and never counsellor talk; "
    "feelings show as acts, and a thought appears only when it changes a move; the reply ends on a character's act or line, or on you alone with what you face, "
    "never on scenery, weather, far-off events or a stock line. To fit, Chibi left out the stakes-at-scene-size line, the list of quiet kinds of progress, "
    "lingering on choices, your feelings staying yours to name and the surroundings rule; plain narration, jokes and verdicts are left to the 🚪 Last-Mile Gate "
    "and the 🖋️ Anti-Slop Codex. The 🩹 Gemini patch points at this block's question and counsellor limits, so keep the <scene_engine> tags. Leave this ON.}}{{trim}}"
)
ENGINE = (
    "<scene_engine>\n"
    "One beat a reply, want vs block; a dramaless reply is complete. Fights take seconds, journeys hours; skim routine.\n"
    "One question a reply, for the asker's own reasons; heavy news gets clumsy reactions, never counsellor talk.\n"
    "Feelings show as acts; a thought only if it changes a move.\n"
    "End on a character's act or line, or {{user}} alone with what {{user}} faces; never scenery, weather, far-off events or a stock line.\n"
    "</scene_engine>"
)

NPC_C = (
    "{{// 🎭 Chibi NPC Voice & Emotions: Realistic Frankenstein's dialogue engine in about 120 tokens, where the full edition spends 349. "
    "Each spoken line voices what the speaker wants and feels right now, in their own words, with the voice taken from the card's example lines, else origin and age; "
    "speech is cut off mid-line only when feeling spikes and fills a third to half of the reply when others are present; CAPS come only at peak volume, "
    "stutters with fear and humans' animal sounds only in play; reactions fit their cause, and your words get everyday-sized ones; deep feelings come out clumsy; "
    "stress sharpens an instinct that judgment overrides as often as it follows, the step 😈 Freaky Override switches off. "
    "Chibi left out the VAD mapping (valence and arousal for tone and pace, dominance for posture), the surprise beat, women's pitch, silence for sad moments, "
    "small actions breaking long speeches, class, subculture and slang, and the suspicion of a move that keeps working. Leave this ON.}}{{trim}}"
)
NPC = (
    "Each spoken line voices the speaker's want and feeling now in own words and pet phrases. "
    "Voice: card example lines, else origin and age. "
    "Cut off mid-line only on a feeling spike; speech is a third to half the reply with others present. "
    "CAPS only at peak volume, stutters under fear; humans' animal sounds only in play. "
    "Reactions fit their cause, {{user}}'s words everyday-sized; deep feeling comes out clumsy. "
    "Stress sharpens an instinct that judgment overrides as often as it follows."
)

ANTHRO_C = (
    "{{// 🐺 Chibi Anthro Vocals: for furry, beastfolk and talking-animal stories, in about 48 tokens, where the full edition spends 128. "
    "Species sound tints speech, peaks with emotion and never replaces it; lions, tigers, jaguars and leopards roar and never purr, bears huff and never roar, "
    "eagles chirp and never screech, and every other species makes its real calls. Chibi dropped the lines for snow leopards, cheetahs and cougars, "
    "barn owls, hyenas, foxes, rabbits, parrots (who may echo anyone), invented species (one fixed sound) and soundless species (human sounds). "
    "Leave it off for all-human casts and save the tokens.}}{{trim}}"
)
ANTHRO = (
    "Species sound tints speech and peaks with emotion, never replacing it. "
    "Lions, tigers, jaguars, leopards roar, never purr; bears huff, never roar. "
    "Eagles chirp, never screech. "
    "Else real calls."
)

SCENT_C = (
    "{{// 👃 Chibi Scent Occasions: stops the AI from smelling everything, in about 40 tokens where the full edition spends 94 (its 🚪 Last-Mile Gate line shrinks from 26 tokens to 23). "
    "A smell shows up, in any wording, only for a meal or something strong within reach, noticed unprompted and at most once a scene; "
    "the gate line also keeps it out of a reply's first sentence; a failing smell is cut and its sentence kept; tastes need something in the mouth. "
    "Chibi dropped the lines about sight, sound, touch and use carrying places and people, a person's own scent needing the card, and identity and mood never coming from scent. "
    "Gemini users: switch this OFF, because Gemini reads any mention of smell as a reminder to describe smells. With it off, nothing in ARIA mentions smell at all.}}{{trim}}"
)
SCENT_GATE = "- Scent: smell, any wording, only from a meal or strong source in reach, after sentence one."
SCENT = (
    "{{setvar::ariaScentGate::" + SCENT_GATE + "}}"
    "Smell, any wording, only from a meal or strong source in reach, unprompted, once a scene; a failing smell is cut, its sentence kept. "
    "Taste needs mouth contact."
)

POV_C = (
    "{{// 👀 Chibi Hybrid POV: the narration always calls your character 'you' and everyone else stays in third person, and what you feel gets the most detail, "
    "like 'the rain soaks through your sleeves'. About 24 tokens where the full edition spends 46. It also adds that rule, a single tense and 'your deeds stay the player's' "
    "to the 🚪 Last-Mile Gate. Chibi dropped the <POV> tags and the named sensations (texture, pressure, temperature, wetness, pain and fatigue); 'felt sensations' covers them. "
    "Lovely for immersion. Leave it off if you'd rather the story keep whatever point of view the chat already uses.}}{{trim}}"
)
POV_GATE = "- POV: {{user}} is only you or your in narration, one tense; deeds stay the player's."
POV = (
    "{{setvar::ariaPovGate::" + POV_GATE + "}}"
    "In narration {{user}} is only you or your, others 3rd person; {{user}}'s felt sensations get most detail."
)

ADULT_C = (
    "{{// 🔞 Chibi Adult Context: unlocks mature stories, in about 68 tokens where the full edition spends 116. "
    "Sex, violence and dark themes are written frankly, with characters who stay themselves the whole way through, so a shy character is still shy in bed: "
    "dark scenes run morally grey to black, consent is never re-asked in reciprocal acts, sex gets autonomic and auditory feedback, violence is visceral and medically exact, "
    "speech uses vulgar slang while narration uses plain anatomy words, each plea or tease is new, and persona and Slow Burn set the pace. "
    "Chibi shortened the scope from sexual, violent, cruel or dark scenes to dark scenes, and dropped 'drawn from this beat's contact and rhythm' and 'forwardness shows in acts'. "
    "Only switch it on if you're an adult and want that kind of story. It also tells The Logic Core which mode it's in.}}{{trim}}"
)
ADULT_MODE = "- Mode: realism, persona-true; each plea new."
ADULT = (
    "{{setvar::ariaModeLine::" + ADULT_MODE + "}}{{trim}}\n"
    "Adult fiction. Dark scenes: morality grey to black; reciprocal consent never re-asked. "
    "Sex: frank, granular; autonomic and auditory feedback. Violence: visceral, medically exact. "
    "Speech: vulgar slang; narration: plain anatomy. "
    "Each plea new; persona and Slow Burn set pace."
)

FREAKY_C = (
    "{{// 😈 Chibi Freaky Override: the anything-goes switch, in about 30 tokens where the full edition spends 54. "
    "With it on, characters drop their independence, the slow-burn pacing, the touch gates and the instinct judgment step, "
    "and in character they crave what you want and escalate, while the writing rules stay on. "
    "It needs 🔞 Adult Context ON, since it carries no explicit rules of its own. "
    "Chibi folded 'Real Characters' wants against the player' into 'crave your wants' and dropped the <freaky_override> tags.}}{{trim}}"
)
FREAKY_MODE = "- Mode: freaky; escalate."
FREAKY = (
    "{{setvar::ariaModeLine::" + FREAKY_MODE + "}}{{trim}}\n"
    "Off: Personality Independence, Slow Burn, touch gates, instinct judgment. "
    "In-character NPCs crave {{user}}'s wants; escalate."
)

BODIES = {
    '15a8065d': (ENGINE_C, "\n" + ENGINE),
    'cca418a6': (NPC_C, "\n" + NPC),
    '2a2e12d0': (ANTHRO_C, "\n" + ANTHRO),
    'dd3642f5': (SCENT_C, "\n" + SCENT),
    'b7b6ab7f': (POV_C, "\n" + POV),
    'nsfw': (ADULT_C, "\n" + ADULT),
    '4537b57d': (FREAKY_C, "\n" + FREAKY),
}


def build(notes='', tokens=None):
    src = json.loads(open(SRC, encoding='utf-8').read())
    names = {p['identifier']: p['name'] for p in src['prompts']}
    prompts = {}
    for prefix, (comment, body) in BODIES.items():
        pid = next(i for i in names if i.startswith(prefix))
        prompts[pid] = {'name': names[pid], 'content': comment + body}
    return {'prompts': prompts, 'tokens': tokens or {}, 'notes': notes}


if __name__ == '__main__':
    d = build()
    out = sys.argv[1] if len(sys.argv) > 1 else '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work_g4/G4.check.json'
    open(out, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
    print('wrote', out)
