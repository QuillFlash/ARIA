#!/usr/bin/env python3
"""build_final.py: assemble the G5 draft JSON from final_texts.py + the comments below. Writes g5_draft.json (work copy)."""
import json, sys
sys.path.insert(0, '.')
import importlib, final_texts as F
importlib.reload(F)

TIME_COMMENT = ("{{// ⏰ Chibi Time & Place: a small status line on top of every reply (time, day number, weekday and date, place, weather in °C and °F), "
                "in about 50 tokens where the full edition spends 82. The clock and the weather move on with what each reply covers. "
                "Fate's appointments run on this clock (they read the day number and the time), so switch it on together with 🎲 Fate & Chekhov Ledger. "
                "Chibi shortened the date and weather wording and dropped two rules of the full edition: skipping sleep or travel at your lead "
                "(the clock already follows what a reply covers) and bodies reacting to the weather and the hour. "
                "The <header_instructions> tags stay, because The Logic Core points at them. Ships OFF in Chibi.}}{{trim}}\n")

FATE_COMMENT = ("{{// 🎲 Chibi Fate & Chekhov Ledger: ARIA's world engine in about 470 tokens where the full edition spends 853, plus about 90 for its dice, plan, ledger and gate lines (those stay as they were). "
                "Every turn three hidden dice decide whether the world does something on its own and how close it lands to you. "
                "A picks the tier against the quiet streak q (AMBIENT texture, a MINOR hiccup or a rare MAJOR event); "
                "B decides whether the world acts on its own (TRUE) or something you did comes back through the [hot] Bullets, the setups that should pay off later (WEIGHTED); "
                "C picks the form (news, defer, complicate or displace a THREAD) and guards your scene: only MAJOR+TRUE on a natural 20 may harm it or stop or remove anyone present. "
                "A named future time becomes a TIME-LOCKED Bullet that fires on time, so Fate's appointments need ⏰ Time & Place. "
                "Fate never decides your next move. Its memory is the small folded 🎲 ledger at the end of each reply, which the preset's regex scripts dress up as the orange Fate & Routine panel: "
                "its field names, symbols, separators and order are untouched, and it has to stay in the chat. "
                "Chibi kept every dice ladder and threshold, the ages that matter (THREAD 8, Deferred 6, ripe World entry 8, Bullet 6 to fire and 12 to prune) and every ledger field, "
                "plus the tester fixes it could fit: q defined as AMBIENT turns in a row, a THREAD opened only when none is open and owned by the card's characters or you, displace defined, "
                "a no-warning MAJOR landing whole this turn, a ripe World entry landing whatever you are busy with, the one-sentence AMBIENT folded into a paragraph about someone present, "
                "news reaching the page only through someone present, and the natural-20 limit. "
                "It cut the rest: the World rule (your far-reaching acts logged unrolled, the cap of 5), Ambitions (stated goals counted to 5), the Quiet paragraph and the aftermath at q 0-2, "
                "the carried-state rule and 'intentions may fail', a MINOR reviving a Deferred item and a twice-deferred item returning as MAJOR, the age-4 first effect and age-12 fallback of World entries, "
                "Residue from every ended THREAD, the limit's extras (anyone Fate brings keeps to the edge, which the gate's People line also says) and most of the cell descriptions. "
                "Ships OFF in Chibi; best with 64k context and a model above 12B; pair it with ⏰ Time & Place.}}{{trim}}\n")

BONDS_COMMENT = ("{{// 🥰 Chibi Bonds Lite: an optional relationship tracker in about 210 tokens where the full edition spends 297. "
                 "Every pair of characters gets a bond score plus small Sparks and Grudge counters: seven kinds of warm acts earn Sparks (at most 2 per pair per turn), "
                 "7 Sparks turn into one point of BOND, 5 Grudge into minus one, three Grudge halve the gains, and a sincere repair clears it. "
                 "Touch gates (+4 hug, +8 hand-holding, +12 kiss, +15 sex) allow things and never force them; love is declared only at +15 and up, and +20 allows marriage proposals, answered yes or no from your past acts. "
                 "The numbers live in their own small 💚 ledger at the end of each reply, right after the 🎲 ledger when Fate is on, and never appear in the story; "
                 "the preset's regex scripts draw each pair as a card with Bond, Sparks and Grudge bars, so the pair format stays as it was. "
                 "Chibi kept the extremes of the scale (malice with its violence and near-irreversible damage, the love and marriage gates) and dropped the labels and behaviors for the middle "
                 "(hostile, neutral, warm, trust, devoted, casual touch, admitting romantic interest), the <bonds> tags (nothing pointed at them), "
                 "the rule that prose shows tiers only through behavior and the restatement that no listed act means no Spark. Ships OFF.}}{{trim}}\n\n")

def assemble():
    time_c = TIME_COMMENT + F.TIME_BODY
    fate_c = FATE_COMMENT + F.FATE_SETVARS + "\n".join(F.FATE_LINES)
    bonds_c = BONDS_COMMENT + F.BONDS_SETVARS + "\n".join(F.BONDS_LINES)
    return {
        "5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa": {"name": "⏰ Time & Place", "content": time_c},
        "acc2177a-34e4-4941-93a2-b80bc18b8c91": {"name": "🎲 Fate & Chekhov Ledger", "content": fate_c},
        "5506d699-fb00-49ce-a631-73b3f0036eae": {"name": "🥰 Bonds Lite", "content": bonds_c},
    }

if __name__ == '__main__':
    d = {"prompts": assemble()}
    json.dump(d, open('g5_draft_wip.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote g5_draft_wip.json')
