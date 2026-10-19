TMPL = "<details><summary>🎲</summary>q: n | hp: n | thread: pursuit, age n/8 | deferred: item xN, age n/6 | world: event, ELSEWHERE/REGIONAL/LOCAL, age n | bullets: setup [hot], weight 1-3, age n/12 | ambitions: goal n/5 | residue: lasting change | last: AMBIENT/MINOR/MAJOR TRUE/WEIGHTED, fate's 5-word happening</details>"
TIME_BODY = """<header_instructions>
Open with [🕰️ HH:MM AM/PM | 🗓️ Day # - Weekday, Day Month Year era | 📍 Place | weather emoji °C/°F, conditions], moved on by each reply's span.
</header_instructions>"""
FATE_BODY = """Tier: A, -3 if MAJOR in last 2 turns, else +4 at 3+ or +2 at 1-2 Deferred; q = AMBIENT turns in a row; q 0-2: MINOR 16+, MAJOR 20+; 3-6: 12+, 19+; 7+: 8+, 17+; under MINOR: AMBIENT, q+1; else q 0.
Source: hp = [hot] Bullets; WEIGHTED at B 14+ (hp 1-2), 9+ (3-4), 5+ (5+), else TRUE.
Form, C once: AMBIENT 1-6 is World news via someone present. No THREAD: MINOR/MAJOR opens one; else MINOR 1-12 defers, else complicates, MAJOR 1-10 complicates, else displaces.
AMBIENT: ≤1 texture sentence in a paragraph about someone present.
TRUE | WEIGHTED:
MINOR: small cost or pleasure | a consequence brushes {{user}}.
MAJOR, rare, whole this turn: a REGIONAL/LOCAL World entry aged 8+ lands, busy {{user}} or not; else someone else's big, unwarned happening | oldest [hot] Bullet aged 6+ fires.
Only MAJOR+TRUE on C 20 harms the scene or stops/removes anyone present; else all stay, harm comes from outside.
Bullets: ≤1 new unpaid setup a turn, [hot] if {{user}} caused it.
Ledger (none if empty): """ + TMPL
BONDS_BODY = """Track meaningful pairs in the 💚 block: Name↔Name +6/3/0 (BOND/Sparks/Grudge); strangers 0/0/0.
BOND -10..+20; ≤-6 seeks harm; love declared only at +15+; +20 proposals, answered from {{user}}'s past acts.
Touch gates: +4 hug; +8 hand-holding; +12 kiss; +15 sex (context allowing).
Sparks +1 per act to the other, max 2 a turn: gift, favour, defence, confiding, laugh, being chosen, willing touch; 7: BOND +1, Sparks 0. Grudge +1 per slight; 5: BOND -1, Grudge 0; 3+ halves gains; sincere repair clears it."""
