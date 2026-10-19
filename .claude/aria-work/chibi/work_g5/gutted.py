import sys
sys.path.insert(0,'.')
import t, final_texts as F
LED = F.LEDGER
fate_g = "\n".join([
 "{{user}} is always answered in full; prose names no mechanic.",
 "Tier: A (-3 if MAJOR in the last 2 turns, else +4 at 3+ or +2 at 1-2 Deferred); q = AMBIENT streak. q 0-2: MINOR 16+, MAJOR 20+; q 3-6: 12+, 19+; q 7+: 8+, 17+; below MINOR: AMBIENT, q+1, else q 0.",
 "Source: hp = [hot] Bullets; WEIGHTED at B 14+ (hp 1-2), 9+ (3-4), 5+ (5+), else TRUE.",
 "C once at the tier's line: AMBIENT 1-6 World news. No THREAD: MINOR/MAJOR opens one. THREAD open: MINOR 1-12 defers, else complicates; MAJOR 1-10 complicates, else displaces. THREAD closes or parks by age 8, Deferred expires at 6.",
 "TRUE | WEIGHTED: AMBIENT: a sentence of texture | a [hot] Bullet warms. MINOR: small cost, or news nears LOCAL | a consequence brushes {{user}}. MAJOR: a World entry aged 8+ lands as Residue, else someone else's arbitrary happening | the oldest [hot] Bullet aged 6+ fires.",
 "Only MAJOR+TRUE on C 20 may harm {{user}}'s scene or stop/remove anyone present; else all stay.",
 "Bullets (max 8): ≤1 loaded a turn, [hot] if {{user}} caused it, pruned at 12; a named future time loads a TIME-LOCKED one at Day # HH:MM that fires on time.",
 LED])
bonds_g = "\n".join([
 "Track every meaningful pair, NPC↔NPC included, in the 💚 block as Name↔Name +6/3/0 (BOND/Sparks/Grudge), comma-separated; strangers 0/0/0.",
 "BOND -10..+20: ≤-6 malice, seeks harm, extreme violence, near irreversible; +20: marriage proposals, answered yes or no from {{user}}'s past acts.",
 "Touch gates: +4 friendly hug; +8 hand-holding, sustained touch; +12 romantic kiss; +15 sex (context allowing).",
 "BOND never rises directly. Sparks +1 when one of the pair does one of these to the other this turn: gives something, does a favour, defends, shares something private, makes laugh, chooses over someone else, touches willingly; max +2 a pair a turn. Sparks 7+: BOND +1, Sparks 0. Grudge +1 per slight; 5+: BOND -1, Grudge 0; while Grudge 3+, gains halve; sincere repair: Grudge 0."])
time_g = "<header_instructions>\nOpen with [🕰️ HH:MM AM/PM | 🗓️ Day # - Weekday, date, era | 📍 Place | weather emoji °C/°F, sky]; clock and weather advance by what the reply covers.\n</header_instructions>"
print('gutted Fate', t.n(fate_g), 'Bonds', t.n(bonds_g), 'Time', t.n(time_g))
print('sum with lines 112:', t.n(fate_g)+t.n(bonds_g)+t.n(time_g)+112)
