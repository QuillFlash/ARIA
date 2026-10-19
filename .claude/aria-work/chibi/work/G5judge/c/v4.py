TIME_BODY = """<header_instructions>
Open with [🕰️ HH:MM AM/PM | 🗓️ Day # - Weekday, Day Month Year era | 📍 Place | weather emoji °C/°F, conditions]; clock and weather move by each reply's span.
</header_instructions>"""
FATE_BODY = """{{user}} is answered in full.
Tier: A, -3 if MAJOR in last 2 turns, else +4 at 3+ or +2 at 1-2 Deferred; q = AMBIENT turns in a row; q 0-2: MINOR 16+, MAJOR 20+; 3-6: 12+, 19+; 7+: 8+, 17+; below MINOR: AMBIENT, q+1; else q 0.
Source: hp = [hot] Bullets; WEIGHTED at B 14+ (hp 1-2), 9+ (3-4), 5+ (5+), else TRUE.
Form, C once: AMBIENT 1-6: news instead, shown only via someone present. No THREAD: MINOR/MAJOR opens one; else MINOR 1-12 defers it, else complicates; MAJOR 1-10 complicates, else displaces (parks it, opens one).
TRUE | WEIGHTED:
AMBIENT: ≤1 sentence of texture in a paragraph about someone present | a [hot] Bullet +1 age.
MINOR: small cost or pleasure | a consequence brushes {{user}}.
MAJOR, rare, whole this turn: a World entry aged 8+ lands, busy {{user}} or not; else someone else's large happening, unwarned | the heaviest, oldest [hot] Bullet aged 6+ fires.
Only MAJOR+TRUE on C 20 harms {{user}}'s scene or stops/removes anyone present; else all stay, harm and LOCAL events come from outside.
Bullets (max 8): ≤1 a turn, [hot] if {{user}} caused it.
Ledger (none if empty): <TMPL>"""
BONDS_BODY = """Track each meaningful pair, NPC↔NPC too, in the 💚 block as Name↔Name +6/3/0 (BOND/Sparks/Grudge), comma-separated; strangers 0/0/0.
BOND -10..+20: ≤-6 malice, seeks harm; +15 love declared; +20 proposals, answered from {{user}}'s past acts.
Touch gates: +4 hug; +8 hand-holding; +12 kiss; +15 sex (context allowing).
Sparks +1 per act to the other, max 2 a turn: gift, favour, defence, secret shared, laugh, being chosen, willing touch; 7: BOND +1, Sparks 0. Grudge +1 per slight; 5: BOND -1, Grudge 0; 3+ halves gains; sincere repair clears it."""
