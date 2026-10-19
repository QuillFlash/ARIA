#!/usr/bin/env python3
"""menus.py: measure every restore item (text added to the primary) and cut item (text removed from the primary) in tokens."""
import sys
sys.path.insert(0, '.')
import importlib, final_texts as F, t
importlib.reload(F)

def tok(s): return t.n(s)

FATE = "\n".join(F.FATE_LINES)
BONDS = "\n".join(F.BONDS_LINES)
TIME = F.TIME_BODY

def apply(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)

# (id, module, description, old, new)   restore: new has more text than old
RESTORE = [
 ("F2", "Fate", "Ambitions rule (0/5, +1 per closed THREAD served, 5/5 becomes Residue and a LOCAL World entry)",
  "Ledger (none if empty):", "Ambitions: a want {{user}} states past this scene logs 0/5, +1 per closed THREAD served; 5/5: Residue and a LOCAL World entry.\nLedger (none if empty):"),
 ("F1m", "Fate", "World rule, short form (cap 5; far-reaching acts logged unrolled; news late or slanted)",
  "Ledger (none if empty):", "World (max 5): {{user}}'s far-reaching acts, unrolled, and news, late or slanted.\nLedger (none if empty):"),
 ("F1", "Fate", "World rule, full (adds: news by the era's channels, ledger-only until it reaches someone present, nobody ties effect to news aloud)",
  "Ledger (none if empty):", "World (max 5): {{user}}'s far-reaching acts, unrolled, and news by the era's channels, late or slanted, on the page only once it reaches someone present, else in the ledger alone; nobody ties effect to news aloud.\nLedger (none if empty):"),
 ("F3s", "Fate", "aftermath at q 0-2",
  "Bullets (max 8):", "q 0-2 is aftermath: nobody solves anything or opens a pursuit unforced.\nBullets (max 8):"),
 ("F3", "Fate", "Quiet paragraph in full (needs and the clock drive people; one thing changes without escalating; q 0-2 aftermath)",
  "Bullets (max 8):", "Quiet (AMBIENT or no THREAD): needs and the clock drive people, one thing changes without escalating; q 0-2: aftermath, nobody solves anything or opens a pursuit unforced.\nBullets (max 8):"),
 ("F4", "Fate", "a MINOR may revive a Deferred item; one deferred twice returns as MAJOR",
  "Deferred expires at 6.", "Deferred expires at 6 (a MINOR may revive one; deferred twice returns as MAJOR)."),
 ("F16", "Fate", "anyone fate brings keeps to the edge (the gate's People line also covers newcomers)",
  "arrive from outside.", "arrive from outside, and anyone fate brings keeps to the edge."),
 ("F11", "Fate", "limit extras: however dramatic the cell; arrivals come as news or changed circumstances",
  "or stop/remove anyone present; else all stay and carry on, harm and LOCAL events arrive from outside.", "or stop/remove anyone present, however dramatic the cell; else all stay and carry on, harm and LOCAL events arrive from outside as news or changed circumstances."),
 ("F10", "Fate", "AMBIENT detail: seen or heard where {{user}} is, never the reply's last line, never foreshadowed or revisited",
  "AMBIENT: one sentence of texture, folded", "AMBIENT: one sentence at most of texture seen or heard where {{user}} is, never foreshadowed or revisited, never the reply's last line, folded"),
 ("F6", "Fate", "carried state schedules nothing; intentions may fail",
  "answered in full; prose", "answered in full, though intentions may fail; carried state schedules nothing; prose"),
 ("F6b", "Fate", "intentions may fail only",
  "answered in full; prose", "answered in full, intentions may fail; prose"),
 ("F8", "Fate", "MINOR: a World entry aged 4+ lands its first effect",
  "a band toward LOCAL |", "a band toward LOCAL or, at age 4+, lands its first effect |"),
 ("F9", "Fate", "MAJOR TRUE also counts a younger World entry that news escalated",
  "aged 8+ lands as Residue", "aged 8+, or a younger one news escalated, lands as Residue"),
 ("F9b", "Fate", "MAJOR WEIGHTED falls back to TRUE also when a LOCAL World entry aged 12+ exists",
  "fires (none: TRUE).", "fires (none, or a LOCAL World entry aged 12+: TRUE)."),
 ("F7", "Fate", "TIME-LOCKED also sets THREAD",
  "firing on time at any tier.", "firing on time at any tier and setting THREAD."),
 ("F15", "Fate", "each THREAD or Deferred item that ends leaves Residue",
  "Deferred expires at 6.", "Deferred expires at 6, each end leaving Residue."),
 ("F12", "Fate", "'seen, handled later' for defers",
  "MINOR 1-12 defers,", "MINOR 1-12 defers (seen, handled later),"),
 ("F13", "Fate", "Bullets load test: setups a reader would notice unpaid",
  "load ≤1 a turn,", "load ≤1 a turn for setups a reader would notice unpaid,"),
 ("F14", "Fate", "ledger ages +1 at turn start",
  "Ledger (none if empty):", "Ledger (none if empty; ages +1 at turn start):"),
 ("T1", "Time", "bodies react to weather and hour",
  "by what the reply covers.", "by what the reply covers; bodies react to weather and hour."),
 ("T2", "Time", "sleep or travel skipped at the player's lead",
  "by what the reply covers.", "by what the reply covers, skipping sleep or travel at {{user}}'s lead."),
 ("T3", "Time", "full date wording: Day Month, Year CE/AD/fantasy era; general description of the weather",
  "Weekday, date, era | 📍 Place | weather emoji °C/°F, conditions]", "Weekday, Day Month, Year CE/AD/fantasy era | 📍 Place | weather emoji °C/°F, general description of the weather]"),
 ("B1", "Bonds", "+8..+15 trust, admits romantic interest; +16+ devoted",
  "near irreversible; love declared", "near irreversible; +8..+15 trust, admits romantic interest; +16+ devoted; love declared"),
 ("B2", "Bonds", "the rest of the scale with its behaviors (hostile, avoids; neutral, polite; warm, seeks company; casual touch), on top of B1",
  "near irreversible; love declared", "near irreversible; -5..-3 hostile, avoids; -2..+2 neutral, polite; +3..+7 warm, seeks company; +8..+15 trust, casual touch, admits romantic interest; +16+ devoted; love declared"),
 ("B3", "Bonds", "prose shows tiers only through behavior",
  "strangers 0/0/0.", "strangers 0/0/0; tiers show only through behavior."),
 ("B4", "Bonds", "marriage answer from all past acts",
  "yes or no from {{user}}'s past acts", "yes or no from all {{user}}'s past acts"),
]


ORDER = ['F2', 'F1m', 'F3s', 'F4', 'B1', 'T1', 'B4', 'F6b', 'F7', 'F15', 'F9b', 'F8', 'F16', 'F9', 'F11', 'F12', 'F13', 'F14', 'T2', 'B3', 'F10', 'F6', 'T3', 'F1', 'F3', 'B2']
RESTORE.sort(key=lambda r: ORDER.index(r[0]))

# CUT items: text removed from the primary (old -> new), lowest regret first
CUT = [
 ("K1", "Fate", "(none: TRUE) when no Bullet qualifies", " (none: TRUE)", ""),
 ("K2", "Fate", "AMBIENT: +1 extra age", ", +1 extra age.", "."),
 ("K3", "Fate", "'rare' on MAJOR", "MAJOR, rare, whole", "MAJOR, whole"),
 ("K4", "Time", "'Open with' (the template then stands alone in its tags)", "Open with [", "["),
 ("K5", "Fate", "displace definition: parks it, opens one on the happening", " (parks it, opens one on the happening)", ""),
 ("K6", "Fate", "what a THREAD is: a pursuit of the card's characters or {{user}}", ", a pursuit of the card's characters or {{user}}", ""),
 ("K7", "Bonds", "list read once", ", list read once.", "."),
 ("K8", "Fate", "or close circle", " or close circle", ""),
 ("K9", "Bonds", "(context allowing)", " (context allowing)", ""),
 ("K10", "Bonds", "love declared only at +15+", "love declared only at +15+, marriage proposals only at +20", "marriage proposals only at +20"),
 ("K11", "Fate", "prose names no mechanic", "; prose names no mechanic.", "."),
]

def src(mod):
    return {"Fate": FATE, "Bonds": BONDS, "Time": TIME}[mod]

if __name__ == '__main__':
    base = {m: tok(src(m)) for m in ("Fate", "Bonds", "Time")}
    print('PRIMARY', base, 'own sum', sum(base.values()))
    print('--- RESTORE (tokens added)')
    for i, mod, desc, old, new in RESTORE:
        x = apply(src(mod), old, new)
        print(f'{i:4} {mod:5} +{tok(x) - base[mod]:5.1f}  {desc[:110]}')
    print('--- CUT (tokens saved)')
    for i, mod, desc, old, new in CUT:
        x = apply(src(mod), old, new)
        print(f'{i:4} {mod:5} -{base[mod] - tok(x):5.1f}  {desc[:110]}')
