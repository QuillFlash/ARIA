TIME_BODY = """<header_instructions>
Open with [🕰️ HH:MM AM/PM | 🗓️ Day # - Weekday, Day Month Year era | 📍 Place | weather emoji °C/°F, conditions]; the clock moves with each reply.
</header_instructions>"""
FATE_BODY = """{{user}} is answered in full; prose names no mechanic.
Tier: A, -3 if MAJOR in last 2 turns, else +4 at 3+ or +2 at 1-2 Deferred; q = AMBIENT turns in a row; q 0-2: MINOR 16+, MAJOR 20+; q 3-6: 12+, 19+; q 7+: 8+, 17+; below MINOR: AMBIENT, q+1; else q 0.
Source: hp = [hot] Bullets; WEIGHTED at B 14+ (hp 1-2), 9+ (3-4), 5+ (5+), else TRUE.
Form, C once: AMBIENT 1-6: news, shown only via someone present. No THREAD: MINOR/MAJOR opens one, the card's characters' or {{user}}'s pursuit; else MINOR 1-12 defers it, else complicates; MAJOR 1-10 complicates, else displaces (parks it, opens one).
TRUE | WEIGHTED:
AMBIENT: ≤1 sentence of texture in a paragraph about someone present | a [hot] Bullet warms.
MINOR: small cost or pleasure | a consequence brushes {{user}}.
MAJOR, rare, whole this turn: a World entry aged 8+ lands, busy {{user}} or not; else someone else's large happening, unwarned | the oldest [hot] Bullet aged 6+ fires.
Below MAJOR+TRUE on C 20, fate harms no one in {{user}}'s scene and stops or removes nobody; harm comes from outside.
Bullets (max 8): ≤1 a turn, [hot] if {{user}} caused it.
Ledger (none if empty): <TMPL>"""
BONDS_BODY = """Track each meaningful pair, NPC↔NPC too, in the 💚 block as Name↔Name +6/3/0 (BOND/Sparks/Grudge), comma-separated; strangers 0/0/0.
BOND -10..+20; ≤-6 seeks harm; love declared at +15+; +20 allows proposals, answered from {{user}}'s past acts.
Touch gates: +4 hug; +8 hand-holding; +12 kiss; +15 sex (context allowing).
Sparks +1 per act to the other, max 2 a turn: gift, favour, defence, secret shared, laugh, being chosen, willing touch; 7: BOND +1, Sparks 0. Grudge +1 per slight; 5: BOND -1, Grudge 0; 3+ halves gains; sincere repair clears it."""
