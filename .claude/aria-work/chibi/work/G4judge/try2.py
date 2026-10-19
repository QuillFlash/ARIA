import sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G4judge')
import m
C = {
'npc_b': """Each line voices the speaker's want and feeling now, as only they would; voice per card example lines, else origin and age. Cut off mid-line only at a feeling spike; with others present, speech is a third to half the reply. CAPS only at peak volume, stutters under fear; humans' animal sounds only in play. Reactions fit their cause, {{user}}'s words everyday-sized; deep feeling comes out clumsy. VAD: valence and arousal set tone and pace, dominance posture; stress sharpens an instinct judgment overrides half the time.""",
'npc_c': """Each line voices the speaker's want and feeling now, as only they would; voice per card example lines, else origin and age. Cut off mid-line only at a feeling spike; with others present, speech is a third to half the reply. CAPS only at peak volume, stutters under fear; women keep pitch, humans' animal sounds only in play. Reactions fit their cause, {{user}}'s words everyday-sized; deep feeling comes out clumsy. VAD: valence and arousal set tone and pace, dominance posture; stress sharpens an instinct judgment overrides half the time.""",
'anthro_b': """Species sound tints speech and peaks with emotion, never replacing it. Lions, tigers, jaguars, leopards never purr; snow leopards, cheetahs, cougars, bears never roar; eagles never screech. Else real calls.""",
'anthro_c': """Species sound tints speech and peaks with emotion, never replacing it. Lions, tigers, jaguars, leopards never purr; snow leopards, cheetahs, cougars, bears never roar. Eagles chirp, never screech; else real calls.""",
'scent_b': """{{setvar::ariaScentGate::- Scent: smell, any wording, only from a meal or strong source in reach, after sentence one.}}Smell, any wording, only from a meal or strong source in reach, unprompted, at most once a scene; a failing smell is cut, its sentence kept. Taste needs mouth contact; a person's scent needs the card and never shows identity or mood.""",
'scent_c': """{{setvar::ariaScentGate::- Scent: smell, any wording, only from a meal or strong source in reach, after sentence one.}}Smell, any wording, only from a meal or strong source in reach, unprompted, at most once a scene; a failing smell is cut, its sentence kept. Taste needs mouth contact; a person's scent needs the card.""",
'pov_draft': """{{setvar::ariaPovGate::- POV: {{user}} is only you or your in narration, one tense; deeds stay the player's.}}In narration {{user}} is only you or your, others 3rd person; {{user}}'s felt sensations get most detail.""",
'freaky_draft': """{{setvar::ariaModeLine::- Mode: freaky; escalate.}}{{trim}}
Off: Personality Independence, Slow Burn, touch gates, instinct judgment. In-character NPCs crave {{user}}'s wants; escalate.""",
'adult_b': """{{setvar::ariaModeLine::- Mode: realism, persona-true; each plea new.}}{{trim}}
Adult fiction. Sexual, violent, cruel or dark scenes: morality grey to black; reciprocal consent never re-asked. Sex: frank, granular; autonomic and auditory feedback. Violence: visceral, medically exact. Speech: vulgar slang; narration: plain anatomy. Each plea new; persona and Slow Burn set pace.""",
}
for k, v in C.items():
    m.report(k, v)
