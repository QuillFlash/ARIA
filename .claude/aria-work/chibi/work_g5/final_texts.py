# Final G5 text pieces (CC form). build_final.py assembles them; restore.py measures the restore menu.
# ---------------------------------------------------------------- Time & Place
TIME_BODY = ("<header_instructions>\n"
             "Open with [🕰️ HH:MM AM/PM | 🗓️ Day # - Weekday, date, era | 📍 Place | weather emoji °C/°F, conditions]; clock and weather advance by what the reply covers.\n"
             "</header_instructions>")

# ---------------------------------------------------------------- Fate
FATE_SETVARS = ("{{setvar::ariaDice::Fate dice: A {{roll::1d20}} | B {{roll::1d20}} | C {{roll::1d20}}}}"
                "{{setvar::ariaFateLine::- Fate: A tier on q's band; B source; C form vs THREAD; cell; C 20 limit; results only.}}"
                "{{setvar::ariaLedgerLine::- Ledger: last 🎲 block plus this turn's changes, ages +1; the closing 🎲 block copies it.}}"
                "{{setvar::ariaLedgerGate::- Ledger: one full 🎲 block ends the reply.}}{{trim}}\n")
LEDGER = ("Ledger (none if empty): <details><summary>🎲</summary>q: n | hp: n | thread: pursuit, age n | deferred: item xN, age n | world: event, ELSEWHERE/REGIONAL/LOCAL, age n | "
          "bullets: setup [hot], weight 1-3, age n | ambitions: goal n/5 | residue: lasting change | last: AMBIENT/MINOR/MAJOR TRUE/WEIGHTED, fate's 5-word happening</details>")
FATE_LINES = [
    "{{user}} is always answered in full; prose names no mechanic.",
    "Tier: A (-3 if MAJOR in the last 2 turns, else +4 at 3+ or +2 at 1-2 Deferred); q counts AMBIENT turns in a row. q 0-2: MINOR 16+, MAJOR 20+; q 3-6: 12+, 19+; q 7+: 8+, 17+; below MINOR: AMBIENT, q+1; else q 0.",
    "Source: hp = [hot] Bullets; WEIGHTED at B 14+ (hp 1-2), 9+ (3-4), 5+ (5+), else TRUE.",
    "Form, C once at the tier's line: AMBIENT 1-6 World news, shown only once it reaches someone present, instead of its cell. No THREAD: MINOR/MAJOR opens one, a pursuit of the card's characters or {{user}}. THREAD open: MINOR 1-12 defers, else complicates; MAJOR 1-10 complicates, else displaces (parks it, opens one on the happening). THREAD closes or parks by age 8 and Deferred expires at 6.",
    "TRUE | WEIGHTED:",
    "AMBIENT: one sentence of texture, folded into a paragraph about someone present | a [hot] Bullet warms, +1 extra age.",
    "MINOR: small cost/pleasure, or news moves a World entry a band toward LOCAL | a consequence brushes {{user}}.",
    "MAJOR, rare, whole this turn: a REGIONAL/LOCAL World entry aged 8+ lands as Residue however busy {{user}} is; none: someone else's large, arbitrary happening, unwarned | the heaviest, then oldest [hot] Bullet aged 6+ fires (none: TRUE).",
    "Only MAJOR+TRUE on C 20 may harm {{user}}'s scene or close circle, or stop/remove anyone present; else all stay and carry on, harm and LOCAL events arrive from outside.",
    "Bullets (max 8): load ≤1 a turn, [hot] if {{user}} caused it; prune at 12. A named future time loads an ageless TIME-LOCKED one at Day # HH:MM, firing on time at any tier.",
    LEDGER,
]

# ---------------------------------------------------------------- Bonds
BONDS_SETVARS = ("{{setvar::ariaBondsLine::- Bonds: listed acts add Sparks (max 2 per pair), slights Grudge; Sparks 7: BOND +1, Sparks 0.}}"
                 "{{#if !.ariaLedgerLine}}{{setvar::ariaLedgerLine::- Ledger: last 💚 block plus this turn's changes; the closing 💚 block copies it.}}"
                 "{{setvar::ariaLedgerGate::- Ledger: one <details><summary>💚</summary>pairs</details> block ends the reply; BOND rises only at 7 Sparks.}}"
                 "{{else}}{{setvar::ariaLedgerLine::- Ledger: last 🎲 and 💚 blocks plus this turn's changes, ages +1; the closing 🎲 then 💚 blocks copy them.}}"
                 "{{setvar::ariaLedgerGate::- Ledger: one full 🎲 block, then one <details><summary>💚</summary>pairs</details> block, end the reply; BOND rises only at 7 Sparks.}}{{/if}}{{trim}}\n\n")
BONDS_LINES = [
    "Track every meaningful pair, NPC↔NPC included, in the 💚 block as Name↔Name +6/3/0 (BOND/Sparks/Grudge), comma-separated; strangers 0/0/0.",
    "BOND -10..+20: ≤-6 malice, seeks harm, extreme violence, near irreversible; love declared only at +15+, marriage proposals only at +20 (answered yes or no from {{user}}'s past acts and the context).",
    "Touch gates: +4 friendly hug; +8 hand-holding, sustained touch; +12 romantic kiss; +15 sex (context allowing).",
    "BOND never rises directly. Sparks +1 when one of the pair does one of these to the other this turn: gives something, does a favour, defends, shares something private, makes laugh, chooses over someone else, touches willingly; max +2 a pair a turn, list read once. Sparks 7+: BOND +1, Sparks 0. Grudge +1 per slight; 5+: BOND -1, Grudge 0; while Grudge 3+, gains halve; sincere repair: Grudge 0.",
]
