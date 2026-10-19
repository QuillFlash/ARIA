#!/usr/bin/env python3
"""Assemble the G5 judge candidate (CC contents and TC segments) from c/v13.py and write cand.json (draft format, no notes)."""
import json, re, sys, importlib.util
W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G5judge'
sys.path.insert(0, W)
from group import SRC, FATE_SET, BONDS_SET, load_variant  # noqa: E402

V = load_variant(sys.argv[1] if len(sys.argv) > 1 else f'{W}/c/v14.py')

TIME_COMMENT = ("{{// ⏰ Chibi Time & Place: a small status line on top of every reply with the time, day number, weekday and date, "
                "place, and the weather in °C and °F with a word on conditions, in about 47 tokens where the full edition spends 82. "
                "The whole line moves on by the time each reply covers. Chibi dropped two rules of the full edition: skipping sleep or "
                "travel at your lead (the 🚪 Last-Mile Gate still opens a skip on a time marker) and bodies reacting to the weather and "
                "the hour. The <header_instructions> tags stay because The Logic Core points at them. Chibi's 🎲 Fate keeps no timed "
                "appointments, so this line is optional next to it. Ships OFF in Chibi.}}")
FATE_COMMENT = ("{{// 🎲 Chibi Fate & Chekhov Ledger: ARIA's world engine in about 323 tokens where the full edition spends 853, plus 61 for "
                "its dice, plan, ledger and gate lines (87 with 🥰 Bonds Lite on), which are the full edition's. Every turn three hidden dice decide whether "
                "the world does something on its own. A picks the tier against the quiet streak q: AMBIENT texture, a MINOR hiccup or a "
                "rare MAJOR event. B decides whether it comes from the world (TRUE) or from setups you caused, the [hot] Bullets "
                "(WEIGHTED). C picks the form: World news, or what happens to the open THREAD. Only MAJOR+TRUE on a natural 20 may harm "
                "your scene or stop or remove anyone present. Fate never decides your next move. Its memory is the small folded 🎲 "
                "ledger at the end of each reply, which the preset's regex scripts dress up as the orange Fate & Routine panel, so let "
                "it stay in the chat. Chibi keeps every dice ladder, threshold and ledger field (the ledger shows the age limits as "
                "age n/8, n/6 and n/12) and the tester fixes for q, threads, whole and unwarned MAJORs, ripe World entries, folded "
                "AMBIENT lines and the natural-20 limit. It leaves out the full edition's timed appointments, Ambitions, World and "
                "Quiet rules and some cell details; the full edition has them. Ships OFF in Chibi; best with 64k context and a model "
                "above 12B.}}")
BONDS_COMMENT = ("{{// 🥰 Chibi Bonds Lite: an optional relationship tracker in about 124 tokens where the full edition spends 297. Every "
                 "meaningful pair gets a BOND score from -10 to +20 plus Sparks and Grudge counters. Seven kinds of warm acts earn "
                 "Sparks, at most 2 per pair a turn; 7 Sparks become one point of BOND and 5 slights cost one; 3 Grudge halve the "
                 "gains and a sincere repair clears them. Touch gates (+4 hug, +8 hand-holding, +12 kiss, +15 sex) allow things and "
                 "never force them; love is declared only from +15, +20 opens marriage proposals answered from your past acts, and "
                 "at -6 or below a character seeks harm. The numbers live in their own small 💚 ledger at the end of each reply, after "
                 "the 🎲 ledger when Fate is on, and the preset's regex scripts draw each pair as a card with Bond, Sparks and Grudge "
                 "bars. Chibi dropped the middle of the full edition's scale (hostile, neutral, warm, trust, devoted) and the <bonds> "
                 "tags. Ships OFF.}}")

FATE_BODY = V.FATE_BODY.replace('<TMPL>', '')  # v13 embeds its own template
TIME_BODY, BONDS_BODY = V.TIME_BODY, V.BONDS_BODY

# CC contents: same newline pattern as the snapshot
time_cc = TIME_COMMENT + '{{trim}}\n' + TIME_BODY
fate_cc = FATE_COMMENT + '{{trim}}\n' + FATE_SET + '\n' + FATE_BODY
bonds_cc = BONDS_COMMENT + '{{trim}}\n\n' + BONDS_SET + '\n\n' + BONDS_BODY

# TC segments: the text between each module's {{#if .aria-x}} and its {{/if}}
tc_time = TIME_BODY + '\n'
tc_fate = FATE_SET + '\n' + FATE_BODY + '\n'
tc_bonds = BONDS_SET + '\n' + BONDS_BODY + '\n'   # ends on its own newline now that </bonds> is gone

out = {
    'prompts': {
        '5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa': {'name': '⏰ Time & Place', 'content': time_cc},
        'acc2177a-34e4-4941-93a2-b80bc18b8c91': {'name': '🎲 Fate & Chekhov Ledger', 'content': fate_cc},
        '5506d699-fb00-49ce-a631-73b3f0036eae': {'name': '🥰 Bonds Lite', 'content': bonds_cc},
    },
    'tc': {
        'time_place_block': tc_time,
        'fate_block': tc_fate,
        'bonds_block': tc_bonds,
        'switch_comment_time_place': '{{// ⏰ Time & Place: a status line on top of every reply (about 47 tokens in Chibi).}}',
        'switch_comment_fate': ('{{// 🎲 Fate & Chekhov Ledger: the world engine (about 323 tokens in Chibi). Adds a small 🎲 line to every '
                                'reply. Best with 64k context and a model above 12B.}}'),
        'switch_comment_bonds': ('{{// 🥰 Bonds Lite: hidden relationship tracker (about 124 tokens in Chibi). Adds a small 💚 line to '
                                 'every reply.}}'),
    },
}
json.dump(out, open(f'{W}/cand.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(f'{W}/tc_new_time.txt', 'w', encoding='utf-8').write(tc_time)
open(f'{W}/tc_new_fate.txt', 'w', encoding='utf-8').write(tc_fate)
open(f'{W}/tc_new_bonds.txt', 'w', encoding='utf-8').write(tc_bonds)
print('wrote cand.json')
