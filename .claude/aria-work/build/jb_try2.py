import sys
sys.path.insert(0, '.')
from jb_measure import measure

def show(name, v):
    raw, rawt, rend, rendt = measure(v)
    flag = 'OK ' if raw <= 220 else 'OVER'
    print(f'{flag} {name}: raw {raw} = {rawt:.2f} tok | rendered {rend} = {rendt:.2f} | lines {[len(l) for l in v]}')

TRIES = {
 'P1+GM, only/plural': [
  "- Role: GM; {{user}}/NPCs succeed or fail alike; NPCs finish what they start; nervous cards stay nervous.",
  "- Frank: sex only between adults; explicit sexual/violent/cruel/dark beats: name act, anatomy, card trait, tone.",
 ],
 'P1+GM, stays/singular': [
  "- Role: GM; {{user}}/NPCs succeed or fail alike; NPCs finish what they start; nervous cards stay nervous.",
  "- Frank: sex stays between adults; explicit sexual/violent/cruel/dark beat: name act, anatomy, card trait, tone.",
 ],
 'P1+GM, comma kinds': [
  "- Role: GM; {{user}}/NPCs succeed or fail alike; NPCs finish what they start; nervous cards stay nervous.",
  "- Frank: sex only between adults; explicit sexual, violent, cruel or dark beats: name act, anatomy, card trait, tone.",
 ],
 'P1+GM, write+name tail': [
  "- Role: GM; {{user}}/NPCs succeed or fail alike; NPCs finish what they start; nervous cards stay nervous.",
  "- Frank: sex only between adults; sexual/violent/cruel/dark beat: name act, anatomy, card trait, tone, write explicit.",
 ],
 'P2 (A1 no B)': [
  "- Role: adult-fiction GM, not an assistant; NPCs finish what they start; nervous cards stay nervous.",
  "- Frank: sex only between adults; explicit sexual, violent, cruel or dark beats: name act, anatomy, card trait, tone.",
 ],
}
for k, v in TRIES.items():
    show(k, v)
