import sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G5judge')
from group import load_variant, measure
v = load_variant('c/v14.py')
base = {'T': v.TIME_BODY, 'F': v.FATE_BODY, 'B': v.BONDS_BODY}
_, b0, _ = measure(base['T'], base['F'], base['B'], verbose=False)
items = [
 ('R1 TIME-LOCKED appointments (RF; the reason Day # is in the header)', 'F', 'Bullets: ≤1 new unpaid setup a turn, [hot] if {{user}} caused it.', 'Bullets: ≤1 new unpaid setup a turn, [hot] if {{user}} caused it; a named future time loads an ageless TIME-LOCKED one at Day # HH:MM, firing on time and setting THREAD.'),
 ('R2 opening principle (RF step 0)', 'F', 'Tier: A -3', '{{user}} is answered in full; prose names no mechanic.\nTier: A -3'),
 ('R3 displace defined (beta 6)', 'F', 'else displaces.', 'else displaces (parks it, opens one on the happening).'),
 ('R4 THREAD owners (beta 7, DeepSeek V4 Pro)', 'F', 'MINOR/MAJOR opens one;', 'MINOR/MAJOR opens one, a pursuit of the card\'s characters or {{user}};'),
 ('R5 Ambitions (beta 6, Douyin wording)', 'F', 'Ledger (none if empty):', 'Ambitions: a want {{user}} states past this scene logs 0/5, +1 per closed THREAD serving it; 5/5: Residue and a LOCAL World entry.\nLedger (none if empty):'),
 ('R6 World rule, short (max 5; far-reaching acts unrolled; news late or slanted)', 'F', 'Ledger (none if empty):', 'World (max 5): {{user}}\'s far-reaching acts, unrolled, and news, late or slanted.\nLedger (none if empty):'),
 ('R7 Quiet core with aftermath (beta 7 liveliness list not included)', 'F', 'Ledger (none if empty):', 'Quiet (AMBIENT or no THREAD): needs and the clock drive people; one thing changes, unescalated; q 0-2: aftermath, nobody solves anything or opens a pursuit unforced.\nLedger (none if empty):'),
 ('R8 MAJOR WEIGHTED fallback when no Bullet is 6+', 'F', 'oldest [hot] Bullet aged 6+ fires.', 'oldest [hot] Bullet aged 6+ fires (none: TRUE).'),
 ('R9 heaviest Bullet first (uses the template\'s weight 1-3)', 'F', 'oldest [hot] Bullet', 'heaviest, then oldest [hot] Bullet'),
 ('R10 AMBIENT WEIGHTED cell (+1 age)', 'F', 'AMBIENT: ≤1 texture sentence in a paragraph about someone present.', 'AMBIENT: ≤1 texture sentence in a paragraph about someone present; WEIGHTED: a [hot] Bullet ages +1 instead.'),
 ('R11 Bullets max 8', 'F', 'Bullets: ≤1', 'Bullets (max 8): ≤1'),
 ('R12 limit: close circle and carry on', 'F', 'harms the scene or stops/removes anyone present; else all stay, harm comes from outside.', 'harms the scene or close circle or stops/removes anyone present; else all stay and carry on, harm comes from outside.'),
 ('R13 MINOR moves a World entry toward LOCAL', 'F', 'MINOR: small cost or pleasure |', 'MINOR: small cost or pleasure, or news moves a World entry a band toward LOCAL |'),
 ('R14 Bonds NPC↔NPC', 'B', 'Track meaningful pairs in', 'Track meaningful pairs, NPC↔NPC too, in'),
 ('R15 Bonds touch-gate wording (friendly hug, sustained touch, romantic kiss)', 'B', '+4 hug; +8 hand-holding; +12 kiss;', '+4 friendly hug; +8 hand-holding, sustained touch; +12 romantic kiss;'),
 ('R16 Bonds tiers show only through behavior', 'B', 'strangers 0/0/0.', 'strangers 0/0/0; prose shows tiers only through behavior.'),
 ('R17 Bonds: BOND never rises directly (the gate line also says it)', 'B', 'Sparks +1 per act', 'BOND never rises directly. Sparks +1 per act'),
 ('R18 Time: bodies react to weather and hour', 'T', "moved on by each reply's span.", "moved on by each reply's span; bodies react to weather and hour."),
 ('R19 Time: skip sleep or travel at the player\'s lead', 'T', "moved on by each reply's span.", "moved on by each reply's span; skip sleep or travel at {{user}}'s lead."),
 ('R20 Time: full date and weather wording', 'T', 'Weekday, Day Month Year era | 📍 Place | weather emoji °C/°F, conditions]', 'Weekday, Day Month, Year CE/AD/fantasy era | 📍 Place | weather emoji °C/°F, general description of the weather]'),
]
cuts = [
 ('K1 "rare" on MAJOR (the ladder already makes it rare)', 'F', 'MAJOR, rare, whole', 'MAJOR, whole'),
 ('K2 "new" on Bullets', 'F', '≤1 new unpaid', '≤1 unpaid'),
 ('K3 "Cells, " label (the plan line\'s "cell" then has no anchor)', 'F', 'Cells, TRUE | WEIGHTED:', 'TRUE | WEIGHTED:'),
 ('K4 Time "conditions" (the user\'s weather wording)', 'T', '°C/°F, conditions]', '°C/°F]'),
]
for label, k, old, new in items + cuts:
    cur = dict(base)
    assert cur[k].count(old) == 1, (label, cur[k].count(old))
    cur[k] = cur[k].replace(old, new)
    _, t, _ = measure(cur['T'], cur['F'], cur['B'], verbose=False)
    print(f'{t - b0:+7.2f}  {label}')
