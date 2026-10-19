import subprocess, sys
clauses = [
 # Engine
 "stakes at the scene's size", "quiet talk, cooperation, hesitation and open tension", "a reply without drama is complete",
 "linger on choices", "One question a reply at most", "asked for the asker's own reasons", "never as counsellors",
 "feelings stay {{user}}'s to name", "adding only what the exchange cannot", "a brief thought when it changes",
 "jokes and verdicts belong to characters", "surroundings enter when they change", "with {{user}} alone on what {{user}} faces",
 "a question or complication only when the scene holds one", "as plain as the rest", "scenery, weather and far-off events",
 "The reply ends where {{user}} would act",
 # NPC voice
 "a new moment gets a new line", "as far as the card allows", "the first beat shows it landing", "origin, class, age and subculture",
 "cut off mid-line only when feeling spikes", "small actions break up long speeches", "a third to half", "CAPS only at peak volume",
 "stutters under fear", "women keep their pitch", "animal sounds only in deliberate play", "everyday-sized reactions",
 "as the character weighs it", "clumsy or as mundane detail", "silence suits a sad or shy moment", "VAD, for reasoning only",
 "overrides as often as it follows", "draws suspicion", "self-preservation or belonging", "evasions and pet phrases",
 # Anthro
 "never replacing it", "never purr", "snow leopards", "jaw-pop", "barn owls", "hyenas whoop", "gekker", "parrots may echo anyone",
 "Rabbits are near-silent", "one fixed sound", "soundless species", "Eagles chirp",
 # Scent
 "sight, sound, touch and use", "in any wording", "noticed unprompted", "at most once a scene", "a failing smell is cut",
 "Identity and mood come from sight and sound", "taste needs something in the mouth", "own scent needs the card", "past the first sentence",
 # POV
 "only ever you or your", "texture, pressure, temperature, wetness, pain and fatigue", "deeds stay the player's", "in the chat's one tense",
 # Adult
 "consent in reciprocal acts is never re-asked", "autonomic and auditory feedback", "medically exact", "moan in vulgar slang",
 "plain anatomy words", "each plea or tease is new", "drawn from this beat's contact and rhythm", "forwardness shows in acts",
 "pacing per Slow Burn", "persona-true; each plea new", "morality runs grey to black", "sexual, violent, cruel or dark",
 # Freaky
 "Real Characters' wants against the player", "the instinct judgment step", "touch gates", "escalate now", "In-character NPCs crave",
]
for c in clauses:
    out = subprocess.run(['git', 'log', '--all', '-S', c, '--format=%h %ad %s', '--date=short', '--reverse'],
                         capture_output=True, text=True).stdout.strip().splitlines()
    first = out[0] if out else '(not found)'
    print(f'{c[:55]:57} | {first}')
