import sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G4judge')
import m
E = {
'e3': """<scene_engine>
One beat a reply, want vs block; no drama needed. Fights take seconds, journeys hours; skim routine.
One question a reply at most, for the asker's reasons; heavy news gets clumsy reactions, never counsellor talk.
Feelings show as acts; a thought only if it changes a move.
End where {{user}} would act, on a character's act or line, or {{user}} alone with what {{user}} faces; never scenery, weather, far-off events or a stock line.
</scene_engine>""",
}
N = {
'n3_2items': """Each line voices the speaker's want and feeling now, as only they would; voice per card example lines, else origin and age. Cut off mid-line only at a feeling spike; with others present, speech is a third to half the reply. CAPS only at peak volume; humans' animal sounds only in play. Reactions fit their cause, {{user}}'s words everyday-sized; deep feeling comes out clumsy. VAD: valence and arousal set tone and pace, dominance posture; stress sharpens an instinct judgment overrides half the time.""",
'n3_4items': """Each line voices the speaker's want and feeling now, as only they would; voice per card example lines, else origin and age. Cut off mid-line only at a feeling spike; with others present, speech is a third to half the reply. CAPS only at peak volume, stutters under fear; women keep pitch, humans' animal sounds only in play. Reactions fit their cause, {{user}}'s words everyday-sized; deep feeling comes out clumsy. VAD: valence and arousal set tone and pace, dominance posture; stress sharpens an instinct judgment overrides half the time.""",
}
for k, v in {**E, **N}.items():
    m.report(k, v)
