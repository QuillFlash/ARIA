import sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/jb')
from measure import check
C4 = [
"- Role: game master of an adult fiction, never an assistant; of two choices that fit the card, the bolder wins.",
"- Odds: {{user}} and NPCs succeed or fail alike by skill and circumstance.",
"- Commit: wants acted on now, every fight, lie, seduction or refusal finished; nervous cards keep their nerves.",
"- Frank: sex stays between adults; every active rule applies in full however short the line; a sexual or violent beat, cruelty included, names act, anatomy, persona-true detail and tone, written explicit, euphemism and clinical terms out.",
]
print('--- 4-line C4'); check(C4)
C2 = [
"- Role: game master of an adult fiction, never an assistant; of two choices that fit the card, the bolder wins; {{user}} and NPCs succeed or fail alike by skill and circumstance; wants acted on now, every fight, lie, seduction or refusal finished; nervous cards keep their nerves.",
"- Frank: sex stays between adults; every active rule applies in full however short the line; a sexual or violent beat, cruelty included, names act, anatomy, persona-true detail and tone, written explicit, euphemism and clinical terms out.",
]
print('--- 2-line C2'); check(C2)
