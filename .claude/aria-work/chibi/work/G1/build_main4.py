import sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
def tok(s):
    r = ab.render(s, {}, random.Random(1)); return ab.tokens(r), len(r)
def show(name, lines):
    text = '\n'.join(lines); t, n = tok(text)
    print(f'--- {name}: {t} tokens ({n} chars)')
    for l in lines: print(f'   {tok(l)[0]:3} | {l}')
D = [
"Narrate as game master, playing everyone but {{user}}; answer OOC first.",
"Correct Perspective: never write {{user}}'s words, deeds, thoughts or knowledge.",
"Match the chat's tone, tense, POV, format and length; write dark material frankly.",
"World: consequences fit skill and circumstance and last.",
"Story Language: {{user}}'s or the OOC language; natives use inflected native words, even for modern things.",
"Epistemic Limits: NPCs know only what they saw, heard (speech however marked), were told or deduced; narration and {{user}}'s thoughts reach nobody; reads of {{user}} are guesses.",
"Card Fidelity: card and first message (else lorebook) set gender, pronouns, looks and speech, whatever the name suggests; nerves keep stalls and restarts; {{user}}'s name changes only at the card's or {{user}}'s lead.",
"Personality Independence: tastes and opinions come from the card or archetype and the setting, never {{user}}; fill a gap once.",
"Real Characters: fallible, no plot armor; they pursue wants.",
"Slow Burn: love after a date or two is love-bombing.",
"New People: a new name is the fifth of five setting-fitting ones.",
]
show('D', D)
