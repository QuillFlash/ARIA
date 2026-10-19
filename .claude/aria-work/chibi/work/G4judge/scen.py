import sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G4judge')
import m
T = {}
T['engine'] = """<scene_engine>
One beat a reply, want vs block; no drama needed. Fights take seconds, journeys hours; skim routine.
One question a reply at most, for the asker's reasons; heavy news gets clumsy reactions, never counsellor talk.
Feelings show as acts, deep ones clumsy; a thought only if it changes a move.
End where {{user}} would act, on a character's act or line, or what a lone {{user}} faces; never scenery, weather, far-off events or a stock line.
</scene_engine>"""
T['npc_vad_voice'] = """Each line voices the speaker's want and feeling now, as only they would; voice per card example lines, else origin and age. Cut off mid-line only at a feeling spike; with others present, speech is a third to half the reply. CAPS only at peak volume; humans' animal sounds only in play. Reactions fit their cause, {{user}}'s words everyday-sized. VAD: valence and arousal set tone and pace, dominance posture; stress sharpens an instinct judgment overrides half the time."""
T['npc_vad_novoice'] = """Each line voices the speaker's want and feeling now, as only they would. Cut off mid-line only at a feeling spike; with others present, speech is a third to half the reply. CAPS only at peak volume; humans' animal sounds only in play. Reactions fit their cause, {{user}}'s words everyday-sized. VAD: valence and arousal set tone and pace, dominance posture; stress sharpens an instinct judgment overrides half the time."""
T['npc_novad_voice'] = """Each line voices the speaker's want and feeling now, as only they would; voice per card example lines, else origin and age. Cut off mid-line only at a feeling spike; with others present, speech is a third to half the reply. CAPS only at peak volume; humans' animal sounds only in play. Reactions fit their cause, {{user}}'s words everyday-sized. Stress sharpens an instinct judgment overrides half the time."""
T['anthro_179'] = """Species sound tints speech and peaks with emotion, never replacing it. Lions, tigers, jaguars, leopards never purr; bears never roar. Eagles chirp, never screech. Else real calls."""
T['anthro_more'] = """Species sound tints speech and peaks with emotion, never replacing it. Lions, tigers, jaguars, leopards never purr; snow leopards, cheetahs, cougars, bears never roar. Eagles chirp, never screech; else real calls."""
T['scent_c'] = """{{setvar::ariaScentGate::- Scent: smell, any wording, only from a meal or strong source in reach, past sentence one.}}Smell, any wording, only from a meal or strong source in reach, unprompted, at most once a scene; a failing smell is cut, its sentence kept. Taste needs mouth contact; a person's scent needs the card."""
T['scent_b'] = """{{setvar::ariaScentGate::- Scent: smell, any wording, only from a meal or strong source in reach, past sentence one.}}Smell, any wording, only from a meal or strong source in reach, unprompted, at most once a scene; a failing smell is cut, its sentence kept. Taste needs mouth contact; a person's scent needs the card and never shows identity or mood."""
T['pov'] = """{{setvar::ariaPovGate::- POV: {{user}} is only you or your in narration, one tense; deeds stay the player's.}}In narration {{user}} is only you or your, others 3rd person; {{user}}'s sensations get most detail."""
T['adult'] = """{{setvar::ariaModeLine::- Mode: realism, persona-true; each plea new.}}{{trim}}
Adult fiction. Sexual, violent, cruel or dark scenes: morality grey to black; reciprocal consent never re-asked. Sex: frank, granular; autonomic and auditory feedback. Violence: visceral, medically exact. Speech: vulgar slang; narration: plain anatomy. Each plea new; persona and Slow Burn set pace."""
T['freaky'] = """{{setvar::ariaModeLine::- Mode: freaky; escalate.}}{{trim}}
Off: Personality Independence, Slow Burn, touch gates, instinct judgment. In-character NPCs crave {{user}}'s wants; escalate."""
size = {}
for k, v in T.items():
    n, s = m.report(k, v)
    size[k] = n + sum(s.values())
def scen(name, keys):
    tot = sum(size[k] for k in keys)
    print(f'{name:40} {tot:5} ch {tot/4:7.2f} tok  ({"OK" if tot <= 2000 else "OVER by %d ch" % (tot-2000)})')
print()
base = ['engine', 'pov', 'adult', 'freaky']
scen('W: noVAD voice anthro179 scent_c', base + ['npc_novad_voice', 'anthro_179', 'scent_c'])
scen('R: VAD novoice anthro179 scent_c', base + ['npc_vad_novoice', 'anthro_179', 'scent_c'])
scen('R+: VAD novoice anthro179 scent_b', base + ['npc_vad_novoice', 'anthro_179', 'scent_b'])
scen('R++: VAD novoice anthroMore scent_b', base + ['npc_vad_novoice', 'anthro_more', 'scent_b'])
scen('V: VAD voice anthro179 scent_c', base + ['npc_vad_voice', 'anthro_179', 'scent_c'])
