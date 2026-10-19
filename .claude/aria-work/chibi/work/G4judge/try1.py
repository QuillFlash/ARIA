import sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G4judge')
import m
C = {
'engine_draft': """<scene_engine>
One beat a reply, want vs block; a dramaless reply is complete. Fights take seconds, journeys hours; skim routine.
One question a reply, for the asker's own reasons; heavy news gets clumsy reactions, never counsellor talk.
Feelings show as acts; a thought only if it changes a move.
End on a character's act or line, or {{user}} alone with what {{user}} faces; never scenery, weather, far-off events or a stock line.
</scene_engine>""",
'engine_a': """<scene_engine>
One beat a reply, want vs block; a dramaless reply is complete. Fights take seconds, journeys hours; skim routine.
One question a reply at most, for the asker's reasons; heavy news gets clumsy reactions, never counsellor talk.
Feelings show as acts; a thought only if it changes a move.
End where {{user}} would act, on a character's act or line, or {{user}} alone with what {{user}} faces; never scenery, weather, far-off events or a stock line.
</scene_engine>""",
'engine_b': """<scene_engine>
One beat a reply, want vs block, at scene-sized stakes; no drama needed. Fights take seconds, journeys hours; skim routine.
One question a reply at most, for the asker's reasons; heavy news gets clumsy reactions, never counsellor talk.
Feelings show as acts; a thought only if it changes a move.
End where {{user}} would act, on a character's act or line, or {{user}} alone with what {{user}} faces; never scenery, weather, far-off events or a stock line.
</scene_engine>""",
'npc_draft': """Each spoken line voices the speaker's want and feeling now in own words and pet phrases. Voice: card example lines, else origin and age. Cut off mid-line only on a feeling spike; speech is a third to half the reply with others present. CAPS only at peak volume, stutters under fear; humans' animal sounds only in play. Reactions fit their cause, {{user}}'s words everyday-sized; deep feeling comes out clumsy. Stress sharpens an instinct that judgment overrides as often as it follows.""",
'npc_a': """Each line voices the speaker's want and feeling now, in own words and pet phrases; voice per card example lines, else origin and age. Cut off mid-line only on a feeling spike; with others present, speech is a third to half the reply. CAPS only at peak volume, stutters under fear; women keep pitch, humans' animal sounds only in play. Reactions fit their cause, {{user}}'s words everyday-sized; deep feeling comes out clumsy. VAD: valence and arousal set tone and pace, dominance posture; stress sharpens an instinct that judgment overrides half the time.""",
'vad_only': """VAD: valence and arousal set tone and pace, dominance posture.""",
'anthro_draft': """Species sound tints speech and peaks with emotion, never replacing it. Lions, tigers, jaguars, leopards roar, never purr; bears huff, never roar. Eagles chirp, never screech. Else real calls.""",
'anthro_a': """Species sound tints speech and peaks with emotion, never replacing it. Lions, tigers, jaguars, leopards never purr; snow leopards, cheetahs, cougars, bears never roar. Eagles chirp, never screech; else real calls.""",
'scent_draft': """{{setvar::ariaScentGate::- Scent: smell, any wording, only from a meal or strong source in reach, after sentence one.}}Smell, any wording, only from a meal or strong source in reach, unprompted, once a scene; a failing smell is cut, its sentence kept. Taste needs mouth contact.""",
'scent_a': """{{setvar::ariaScentGate::- Scent: smell, any wording, only from a meal or strong source in reach, after sentence one.}}Smell, any wording, only from a meal or strong source in reach, unprompted, at most once a scene; a failing smell is cut, its sentence kept. Taste needs mouth contact, a person's scent the card; identity and mood never come from scent.""",
'adult_draft': """Adult fiction. Dark scenes: morality grey to black; reciprocal consent never re-asked. Sex: frank, granular; autonomic and auditory feedback. Violence: visceral, medically exact. Speech: vulgar slang; narration: plain anatomy. Each plea new; persona and Slow Burn set pace.""",
'adult_a': """Adult fiction. Sexual, violent, cruel or dark scenes: morality grey to black; reciprocal consent never re-asked. Sex: frank, granular; autonomic and auditory feedback. Violence: visceral, medically exact. Speech: vulgar slang; narration: plain anatomy. Each plea new; persona and Slow Burn set pace.""",
}
for k, v in C.items():
    m.report(k, v)
