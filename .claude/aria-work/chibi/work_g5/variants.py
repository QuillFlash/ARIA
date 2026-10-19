#!/usr/bin/env python3
"""variants.py: write the floor and full variants of G5 next to the primary draft (same format)."""
import json, sys
sys.path.insert(0, '.')
import importlib, final_texts as F, build_final as B, t
importlib.reload(F); importlib.reload(B)

LED = F.LEDGER

# ------------------------------------------------------------------ FLOOR (gutted) variant
FLOOR_TIME = ("<header_instructions>\n"
              "Open with [🕰️ HH:MM AM/PM | 🗓️ Day # - Weekday, date, era | 📍 Place | weather emoji °C/°F, sky]; clock and weather advance by what the reply covers.\n"
              "</header_instructions>")
FLOOR_FATE = [
    "{{user}} is always answered in full; prose names no mechanic.",
    F.FATE_LINES[1],
    "Source: hp = [hot] Bullets; WEIGHTED at B 14+ (hp 1-2), 9+ (3-4), 5+ (5+), else TRUE.",
    "C once at the tier's line: AMBIENT 1-6 World news, on the page once it reaches someone present. No THREAD: MINOR/MAJOR opens one. THREAD open: MINOR 1-12 defers, else complicates; MAJOR 1-10 complicates, else displaces. THREAD closes or parks by age 8, Deferred expires at 6.",
    "TRUE | WEIGHTED:",
    "AMBIENT: a sentence of texture, folded into a paragraph about someone present | a [hot] Bullet warms.",
    "MINOR: small cost, or news nears LOCAL | a consequence brushes {{user}}.",
    "MAJOR: a World entry aged 8+ lands as Residue, else someone else's arbitrary happening | the oldest [hot] Bullet aged 6+ fires.",
    "Only MAJOR+TRUE on C 20 may harm {{user}}'s scene or stop/remove anyone present; else all stay.",
    "Bullets (max 8): ≤1 loaded a turn, [hot] if {{user}} caused it, pruned at 12; a named future time loads a TIME-LOCKED one at Day # HH:MM that fires on time.",
    LED,
]
FLOOR_BONDS = [
    "Track every meaningful pair, NPC↔NPC included, in the 💚 block as Name↔Name +6/3/0 (BOND/Sparks/Grudge), comma-separated; strangers 0/0/0.",
    "BOND -10..+20: ≤-6 malice, seeks harm, extreme violence, near irreversible; +20: marriage proposals, answered yes or no from {{user}}'s past acts.",
    "Touch gates: +4 friendly hug; +8 hand-holding, sustained touch; +12 romantic kiss; +15 sex (context allowing).",
    "BOND never rises directly. Sparks +1 when one of the pair does one of these to the other this turn: gives something, does a favour, defends, shares something private, makes laugh, chooses over someone else, touches willingly; max +2 a pair a turn. Sparks 7+: BOND +1, Sparks 0. Grudge +1 per slight; 5+: BOND -1, Grudge 0; while Grudge 3+, gains halve; sincere repair: Grudge 0.",
]

# ------------------------------------------------------------------ FULL variant (every mechanic of the source, in Chibi wording)
FULL_TIME = ("<header_instructions>\n"
             "Open with [🕰️ HH:MM AM/PM | 🗓️ Day # - Weekday, Day Month, Year CE/AD/fantasy era | 📍 Place | weather emoji °C/°F, general description of the weather]; clock and weather advance by what the reply covers, skipping sleep or travel at {{user}}'s lead; bodies react to weather and hour.\n"
             "</header_instructions>")
FULL_FATE = [
    "{{user}} is always answered in full, intentions may fail; carried state schedules nothing; prose names no mechanic.",
    "World (max 5): {{user}}'s far-reaching acts, unrolled, and news arriving by the era's channels, late or slanted, on the page only once it reaches someone present, else in the ledger alone; nobody ties effect to news aloud.",
    "Ambitions: a want {{user}} states past this scene logs 0/5, +1 per closed THREAD served; 5/5: Residue and a LOCAL World entry.",
    F.FATE_LINES[1],
    F.FATE_LINES[2],
    "Form, C once at the tier's line: AMBIENT 1-6 World news, shown only once it reaches someone present, instead of its cell. No THREAD: MINOR/MAJOR opens one, a pursuit the card's characters or {{user}} take up. THREAD open: MINOR 1-12 defers (seen, handled later), else complicates; MAJOR 1-10 complicates, else displaces (parks it, opens one on the happening). THREAD closes or parks by age 8 and Deferred expires at 6 (a MINOR may revive one; deferred twice returns as MAJOR), each end leaving Residue.",
    "TRUE | WEIGHTED:",
    "AMBIENT: one sentence at most of texture seen or heard where {{user}} is, folded into a paragraph about someone present and never the reply's last line, never foreshadowed or revisited | a [hot] Bullet warms, +1 extra age.",
    "MINOR: small cost/pleasure, or news moves a World entry a band toward LOCAL or, at age 4+, lands its first effect | a consequence brushes {{user}}.",
    "MAJOR, rare, whole this turn: a REGIONAL/LOCAL World entry aged 8+, or a younger one news escalated, lands as Residue however busy {{user}} is; none: someone else's large, arbitrary happening, unwarned | the heaviest, then oldest [hot] Bullet aged 6+ fires (none, or a LOCAL World entry aged 12+: TRUE).",
    "Only MAJOR+TRUE on C 20 may harm {{user}}'s scene or close circle, or stop/remove anyone present, however dramatic the cell; else all stay and carry on, harm and LOCAL events arrive from outside as news or changed circumstances, and anyone fate brings keeps to the edge.",
    "Quiet (AMBIENT or no THREAD): needs and the clock drive people, one thing changes without escalating; q 0-2: aftermath, nobody solves anything or opens a pursuit unforced.",
    "Bullets (max 8): load ≤1 a turn for setups a reader would notice unpaid, [hot] if {{user}} caused it; prune at 12. A named future time loads an ageless TIME-LOCKED one at Day # HH:MM, firing on time at any tier and setting THREAD.",
    LED.replace("Ledger (none if empty):", "Ledger (none if empty; ages +1 at turn start):"),
]
FULL_BONDS = [
    "Track every meaningful pair, NPC↔NPC included, in the 💚 block as Name↔Name +6/3/0 (BOND/Sparks/Grudge), comma-separated; strangers 0/0/0; tiers show only through behavior.",
    "BOND -10..+20: ≤-6 malice, seeks harm, extreme violence, near irreversible; -5..-3 hostile, avoids; -2..+2 neutral, polite; +3..+7 warm, seeks company; +8..+15 trust, casual touch, admits romantic interest; +16+ devoted; love declared only at +15+; +20: marriage proposals, answered yes or no from all {{user}}'s past acts and the context.",
    F.BONDS_LINES[2],
    F.BONDS_LINES[3],
]

def pack(time_body, fate_lines, bonds_lines):
    return {"prompts": {
        "5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa": {"name": "⏰ Time & Place", "content": B.TIME_COMMENT + time_body},
        "acc2177a-34e4-4941-93a2-b80bc18b8c91": {"name": "🎲 Fate & Chekhov Ledger", "content": B.FATE_COMMENT + F.FATE_SETVARS + "\n".join(fate_lines)},
        "5506d699-fb00-49ce-a631-73b3f0036eae": {"name": "🥰 Bonds Lite", "content": B.BONDS_COMMENT + F.BONDS_SETVARS + "\n".join(bonds_lines)},
    }}

if __name__ == '__main__':
    json.dump(pack(FLOOR_TIME, FLOOR_FATE, FLOOR_BONDS), open('g5_floor.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(pack(FULL_TIME, FULL_FATE, FULL_BONDS), open('g5_full.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('written')
