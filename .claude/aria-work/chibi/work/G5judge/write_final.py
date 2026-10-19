#!/usr/bin/env python3
"""Write $S/chibi/final/G5.json from cand.json plus exact tokens, notes and judge_notes."""
import json, sys, random
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
W = S + '/chibi/work/G5judge'
sys.path.insert(0, S + '/spec/frozen')
sys.path.insert(0, W)
import aria_budget as ab  # noqa: E402

d = json.load(open(f'{W}/cand.json', encoding='utf-8'))
TIME, FATE, BONDS = '5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa', 'acc2177a-34e4-4941-93a2-b80bc18b8c91', '5506d699-fb00-49ce-a631-73b3f0036eae'


def r(text, state=None):
    st = dict(state or {})
    out = ab.render(text, st, random.Random(1))
    return out, st


t_out, _ = r(d['prompts'][TIME]['content'])
f_out, fst = r(d['prompts'][FATE]['content'])
b_out, bst_alone = r(d['prompts'][BONDS]['content'])
_, bst = r(d['prompts'][BONDS]['content'], {'ariaLedgerLine': fst['ariaLedgerLine']})
q = lambda s: len(s) / 4
tok = {
    TIME: q(t_out),
    FATE: q(f_out),
    BONDS: q(b_out),
    'ariaDice': q(fst['ariaDice']),
    'ariaFateLine': q(fst['ariaFateLine']),
    'ariaLedgerLine (Fate alone)': q(fst['ariaLedgerLine']),
    'ariaLedgerGate (Fate alone)': q(fst['ariaLedgerGate']),
    'ariaLedgerLine (Fate + Bonds)': q(bst['ariaLedgerLine']),
    'ariaLedgerGate (Fate + Bonds)': q(bst['ariaLedgerGate']),
    'ariaBondsLine': q(bst['ariaBondsLine']),
    'ariaLedgerLine (Bonds alone)': q(bst_alone['ariaLedgerLine']),
    'ariaLedgerGate (Bonds alone)': q(bst_alone['ariaLedgerGate']),
}
tok['Fate lines with Bonds on: dice + plan + ledger + gate (ceiling 110)'] = (
    tok['ariaDice'] + tok['ariaFateLine'] + tok['ariaLedgerLine (Fate + Bonds)'] + tok['ariaLedgerGate (Fate + Bonds)'])
tok['Fate lines, Fate alone'] = (tok['ariaDice'] + tok['ariaFateLine'] + tok['ariaLedgerLine (Fate alone)']
                                 + tok['ariaLedgerGate (Fate alone)'])
tok['group G5 everything on (ceilings 45 + 300 + 110 + 120 + 30 = 605)'] = (
    tok[TIME] + tok[FATE] + tok[BONDS] + tok['Fate lines with Bonds on: dice + plan + ledger + gate (ceiling 110)'] + tok['ariaBondsLine'])
for k in ('time_place_block', 'fate_block', 'bonds_block'):
    tok['tc.' + k] = q(r(d['tc'][k])[0])
tok['whole Chibi CC everything ON, frozen checker (G1-G4 finals, this G5, G6 final, 55-token JB stand-in)'] = 2979
tok['same with the G5 draft instead'] = 3215
assert abs(tok['group G5 everything on (ceilings 45 + 300 + 110 + 120 + 30 = 605)'] - 605.0) < 1e-9, tok

NOTES = (
"FINAL G5 TEXTS (the judge's version; it replaces the drafter's notes, which described the 842-token draft and its floor and full "
"alternatives). Three CC prompts and their TC segments with ARIA 1.0's wiring unchanged: identifiers, names, roles, positions, the "
"setvar runs byte-identical to the snapshot (ariaDice with {{roll::1d20}} inside its setvar, ariaFateLine, both ariaLedgerLine and "
"ariaLedgerGate pairs with Bonds' #if, ariaBondsLine), the <header_instructions> tags (The Logic Core points at them) and the "
"snapshot's {{trim}} and newline pattern. The dice, plan, ledger and gate lines are the full edition's, word for word.\n"
"TIME & PLACE (82 -> 47): the header with every field, [🕰️ HH:MM AM/PM | 🗓️ Day # - Weekday, Day Month Year era | 📍 Place | "
"weather emoji °C/°F, conditions], in the user's own day-month-year-era and weather-description format (399c0eb), shortened; the "
"whole line moves on by each reply's span (the moving clock of e4b0fad, weather from beta 6).\n"
"FATE (853 -> 323.25): Tier reads A (-3 after a MAJOR in the last 2 turns, else +4 at 3+ or +2 at 1-2 Deferred), q is the AMBIENT "
"turns in a row, the 16+/20+, 12+/19+, 8+/17+ ladder, under MINOR AMBIENT with q+1, else q 0. Source reads B (hp = [hot] Bullets; "
"WEIGHTED at B 14+, 9+ or 5+ for hp 1-2, 3-4 or 5+, else TRUE). Form reads C once: AMBIENT 1-6 is World news via someone present; "
"with no THREAD a MINOR or MAJOR opens one, else MINOR 1-12 defers it, else complicates, and MAJOR 1-10 complicates, else displaces. "
"AMBIENT is one texture sentence at most inside a paragraph about someone present. Cells, TRUE | WEIGHTED: MINOR a small cost or "
"pleasure | a consequence brushes {{user}}; MAJOR, rare and whole this turn, a REGIONAL/LOCAL World entry aged 8+ lands whether "
"{{user}} is busy or not, else someone else's big, unwarned happening | the oldest [hot] Bullet aged 6+ fires. The natural-20 limit: "
"only MAJOR+TRUE on C 20 harms the scene or stops or removes anyone present; else all stay and harm comes from outside. Bullets: at "
"most one new unpaid setup a turn, [hot] if {{user}} caused it. The ledger template keeps every field and 'none if empty'; its value "
"shapes now carry the age limits, thread age n/8, deferred age n/6, bullets age n/12 (the full edition's close-or-park by 8, expiry "
"at 6 and pruning at 12).\n"
"BONDS (297 -> 124): the pair format and legend in the 💚 block, strangers 0/0/0; BOND -10..+20 with its extremes and gates (at -6 or "
"below a character seeks harm; love declared only at +15+; +20 proposals, answered from {{user}}'s past acts); Touch gates +4, +8, "
"+12, +15 with 'context allowing'; Sparks +1 per listed act to the other, at most 2 a turn, from seven acts; 7 Sparks give BOND +1 and "
"reset; Grudge +1 per slight, 5 give BOND -1 and reset, 3+ halve gains, a sincere repair clears it. The <bonds> wrapper is gone; "
"nothing pointed at it.\n"
"DROPPED (exact costs in the judge's restore menu): Fate's opening principle; the World, Ambitions and Quiet rules; timed "
"(TIME-LOCKED) appointments; the THREAD-owner and displace definitions; the AMBIENT WEIGHTED cell; MINOR's World escalation; "
"MAJOR's Residue, heaviest-first and no-Bullet fallback; the limit's close circle and carry-on; the Bullet cap of 8. Bonds: the middle "
"of the scale, NPC↔NPC, comma-separated, tiers shown only through behaviour, 'BOND never rises directly' (the gate keeps 'BOND rises "
"only at 7 Sparks'), 'list read once' and the touch-gate qualifiers. Time: the skip and bodies rules.\n"
"TC: tc.time_place_block, tc.fate_block and tc.bonds_block each replace the text between {{#if .aria-time-place}}, {{#if .aria-fate}} "
"or {{#if .aria-bonds}} and its own {{/if}} in sysprompt.content; each ends on a newline, Bonds now on its own newline because "
"</bonds> is gone, so the GLM patch text after it still starts a new line. tc.switch_comment_time_place, tc.switch_comment_fate and "
"tc.switch_comment_bonds each replace the {{// ... }} comment right before {{.aria-time-place = off}}, {{.aria-fate = off}} and "
"{{.aria-bonds = off}}.")

JUDGE = (
"VERDICT: approved with fixes; this file replaces the draft (842) and its floor (733) and full (1,184) alternatives.\n"
"SIZE DECIDED EVERYTHING ELSE. The group is exactly 605.00 (2,420 characters) against the 605 sum of its ceilings: Time & Place 47 "
"(ceiling 45, +2), Fate own 323.25 (300, +23.25), Fate's dice, plan, ledger and gate lines with Bonds on 87.25 (110, -22.75; 61 with "
"Fate alone), Bonds own 124 (120, +4), Bonds plan line 23.5 (30, -6.5). Netted per module: Fate +0.5 with its lines, Bonds -2.5 "
"with its plan line, Time +2, so zero in all. tok.py: 47, 323, 124 (TC blocks 47, 324, 124 with their trailing newline). The draft asked the "
"judge not to cut to 605 without deciding which must-keep to lose. Decided on the cap: with the G1-G4 finals, the G6 final (556 on "
"its kitted-out path, +109 over its table share) and a 55-token JB stand-in, the frozen checker's CC everything ON is 3,215 with the "
"draft and 2,979 with this G5. The user's cap is 3,000, so the draft breaks it, and so would any G5 overage above about 20. The "
"2,850 aim is out of reach already through G1 (+23 a normal turn) and G6.\n"
"HOW THE 237 CAME OUT. Wording first: Douyin fragments, digits and symbols, Form merged into one sentence, AMBIENT out of the cells "
"table. Then the age limits moved into the ledger's value shapes (thread age n/8, deferred age n/6, bullets age n/12) instead of being "
"dropped; without the Deferred expiry, Tier's +4 at 3+ Deferred would stick once three items pile up. Then the details the snapshot "
"carries from Realistic Frankenstein rather than from testers, then tester fixes another final already covers: THREAD owners (G1 "
"Main's 'card characters stay central' with G2's People line), anyone Fate brings keeps to the edge (G2 People), AMBIENT never the "
"last line (G4 Engine's ending rule), 'prose names no mechanic' (G3's 'Nothing above go enters the reply'), 'answered in full' (G2 "
"Own words' 'answer {{user}}'s meaning'), Time's skip rule (G2 Senses' 'skips open on a time marker', G4's 'travel hours'). Kept on "
"purpose while cutting: 'AMBIENT 1-6' still says World news, or with no World rule nothing would log World entries and MAJOR's "
"ripe-entry branch would never fire; 'REGIONAL/LOCAL' stays on that entry, so an ELSEWHERE one never lands.\n"
"TESTER FIXES KEPT, traced with git log: q defined, a THREAD opens only when none is open and otherwise meets it, MAJOR whole this "
"turn, 'last' logs fate's own happening, the C 20 limit in the plan line (fe6c27f, Issue #10); everyone stays, harm from outside, a "
"ripe World entry lands however busy {{user}} is, a MAJOR with nothing logged gives no warning (31c8b43, 684cbeb, GLM and Kimi); "
"die-by-die Tier, Source and Form (76a53ac); MAJOR rare (ece78b2); AMBIENT one sentence folded into a paragraph about someone present, "
"news on the page only via someone present (6993aed); the ledger's value shapes, 'none if empty', the plan Ledger line and the gate "
"line (6061a45, MiMo); Time's moving clock and weather (e4b0fad, 76a53ac) and the user's date and weather format (399c0eb); Bonds' "
"MiMo fixes, warm acts adding only Sparks and 'BOND rises only at 7 Sparks' in plan and gate (9bf530a, 5e037d1); the extremes "
"(d6b1cd7).\n"
"FIXES TO THE DRAFT BEYOND SIZE. (1) Time had swapped the user's own date format (Day Month, Year, era; 399c0eb) for 'date, era'; "
"restored as 'Day Month Year era'. (2) The Fate plan line's 'cell' step had lost its anchor when the draft dropped the source's "
"'Cells' label; back as 'Cells, TRUE | WEIGHTED:'. (3) The draft's cells table listed exactly three rows; AMBIENT, which no longer "
"depends on B, now has its own line and the table holds MINOR and MAJOR. (4) Comments rewritten for this text: Chibi sizes, what "
"Chibi leaves out, ships OFF, and Time no longer advertises appointments Chibi's Fate does not keep.\n"
"WIRING. skeleton.py OK for all three CC prompts; skeleton.py --text OK for all three TC segments against the snapshot's "
"(tc_src_*.txt and tc_new_*.txt in $S/chibi/work/G5judge). No JB.md addition touches G5. Frozen checker on in-memory copies: "
"snapshot CC with this G5, no errors (everything ON 5,983 -> 5,245); with the G1-G4 finals as well, only the two JB-order reports "
"the pre-JB snapshot gives once G3's JB print is in; TC snapshot with these segments and switch comments, no errors (everything ON "
"5,806 -> 5,068). Render matrix with the G1-G4 and G6 finals, Time, Fate and Bonds in all 8 on/off mixes, normal and Impersonate: no "
"doubled space, edge whitespace, blank line or leftover macro, and the plan's announced count equals its dashed lines (9, 11, 11, "
"12). TC renders each block on its own lines with no blank line.\n"
"REGEX. The Fate & Routine panel, ledger-row and q/hp label scripts, run in node on a ledger in the old (age n) and the new (age n/8) "
"shape, give identical rows; the Impersonate ledger strip and the open-ledger closer see the same structure (no '<' in any value). "
"The bond bars render comma-, semicolon- and newline-separated pairs alike, so 'comma-separated' could go; they scale BOND by 20, "
"Sparks by 7 and Grudge by 5, which the kept range and thresholds match. The header still matches both Impersonate header strips. "
"The TC regex file's copies of all these scripts are identical to CC's.\n"
"STYLE. Douyin do-this wording; no quoted examples; no rationale aimed at the model. Fragments per line or sentence: Tier 7, Source 2, "
"Form 1 + 2, AMBIENT 1, MINOR and MAJOR 2 cells each, MAJOR's TRUE cell 2, limit 2, Bullets 1; Bonds 2, 4, 4, then 2 + 4; Time 1. "
"Series: Source thresholds 4, Form's THREAD branches 4, Spark acts 7, header fields 4, touch gates 4. The only threes are the fixed "
"vocabularies the panels, plans and Tally read, as in the source: AMBIENT/MINOR/MAJOR, ELSEWHERE/REGIONAL/LOCAL, BOND/Sparks/Grudge "
"and the three dice. Plan and gate lines are unchanged fragment lines.\n"
"RESTORE MENU (exact change to the group total; each needs the same amount cut elsewhere in the Chibi, since about 21 tokens of cap "
"room are left; most valuable first; old text -> new text in the final prompt):\n"
"R4+R3 (+20.75) THREAD owners (ece78b2, DeepSeek V4 Pro) and displace defined (76a53ac): 'MINOR/MAJOR opens one; else MINOR 1-12 "
"defers, else complicates, MAJOR 1-10 complicates, else displaces.' -> 'MINOR/MAJOR opens one, a pursuit of the card's characters or "
"{{user}}; else MINOR 1-12 defers, else complicates, MAJOR 1-10 complicates, else displaces (parks it, opens one on the happening).' "
"Alone: R4 +11.00, R3 +9.75.\n"
"R2 (+12.75) opening principle: 'Tier: A -3' -> '{{user}} is answered in full; prose names no mechanic.' + newline + 'Tier: A -3'.\n"
"R1 (+26.00) timed appointments: '[hot] if {{user}} caused it.' -> '[hot] if {{user}} caused it; a named future time loads an "
"ageless TIME-LOCKED one at Day # HH:MM, firing on time and setting THREAD.' Then the Time comment can advertise appointments again.\n"
"R8 (+3.25) WEIGHTED MAJOR with no [hot] Bullet aged 6+: 'aged 6+ fires.' -> 'aged 6+ fires (none: TRUE).'\n"
"R9 (+3.75) heaviest first, the use of the template's weight 1-3: 'oldest [hot] Bullet' -> 'heaviest, then oldest [hot] Bullet'.\n"
"R11 (+2.00) Bullet cap: 'Bullets: ≤1' -> 'Bullets (max 8): ≤1'.\n"
"R5 (+31.75) Ambitions (76a53ac): before 'Ledger (none if empty):' add 'Ambitions: a want {{user}} states past this scene logs 0/5, +1 "
"per closed THREAD serving it; 5/5: Residue and a LOCAL World entry.' + newline.\n"
"R6 (+19.50) World, short: before the Ledger line add 'World (max 5): {{user}}'s far-reaching acts, unrolled, and news, late or "
"slanted.' + newline.\n"
"R7s (+16.25) Quiet, short: before the Ledger line add 'Quiet turns: one thing changes, unescalated; q 0-2 is aftermath.' + newline. "
"R7 (+42.50) the fuller form: 'Quiet (AMBIENT or no THREAD): needs and the clock drive people, one thing changes unescalated; q 0-2 is "
"aftermath, nobody solving anything or opening a pursuit unforced.' Neither carries beta 7's liveliness list.\n"
"R13 (+12.25) MINOR moves World entries: 'MINOR: small cost or pleasure |' -> 'MINOR: small cost or pleasure, or news moves a World "
"entry a band toward LOCAL |'.\n"
"R12 (+7.25) limit extras: 'harms the scene or stops/removes anyone present; else all stay, harm comes from outside.' -> 'harms the "
"scene or close circle or stops/removes anyone present; else all stay and carry on, harm comes from outside.'\n"
"R10 (+10.50) AMBIENT WEIGHTED cell: 'about someone present.' (the AMBIENT line) -> 'about someone present; WEIGHTED: a [hot] Bullet "
"ages +1 instead.'\n"
"R16 (+11.25) Bonds tiers only through behaviour, also the only no-numbers-in-prose rule with Fate off: 'strangers 0/0/0.' -> "
"'strangers 0/0/0, tiers shown in prose only through behaviour.'\n"
"R17 (+6.75) 'BOND never rises directly. ' before 'Sparks +1 per act'.\n"
"R15 (+8.75) touch-gate wording: '+4 hug; +8 hand-holding; +12 kiss;' -> '+4 friendly hug; +8 hand-holding, sustained touch; +12 "
"romantic kiss;'.\n"
"R14 (+3.50) 'Track meaningful pairs in' -> 'Track meaningful pairs, NPC↔NPC too, in'.\n"
"R18+R19 (+18.75) Time: \"moved on by each reply's span.\" -> \"moved on by each reply's span; skip sleep or travel at {{user}}'s "
"lead, and bodies react to weather and hour.\" Alone: bodies +8.50, skip +9.25 (as one extra fragment each; together they must share "
"one, as here, or the line has three).\n"
"R20 (+9.75) the snapshot's full date and weather wording: 'Day Month Year era' -> 'Day Month, Year CE/AD/fantasy era' and "
"'conditions' -> 'general description of the weather'.\n"
"CUT MENU, only if the build's 3,000 check bites: 'rare' on MAJOR -1.50 (the ladder already makes it rare); 'new' on Bullets -1.00; "
"'conditions' in the header -3.00 (the user's weather wording); 'Cells, ' -1.75 (the plan's 'cell' loses its anchor).\n"
"CROSS-GROUP FLAGS. G1 Main must keep 'Card characters stay central, as do newcomers {{user}} keeps'; G2's gate must keep People, Own "
"words ('answer {{user}}'s meaning') and 'skips open on a time marker'; G3 must keep 'header if <header_instructions>' and 'Nothing "
"above go enters the reply'; G4's Engine must keep its ending rule (never scenery, weather or far-off events), and Freaky's 'touch "
"gates' still names the kept 'Touch gates:' label. G6's DeepSeek Tally reads listed acts, slights, sincere repair, max 2, half at "
"Grudge 3+, the 7 and 5 conversions, strangers 0/0/0, q, hp, [hot] Bullets and last, all kept in the same words.\n"
"BUILD AND DOCS. Marinara: sections[10], [11] and [12] hold Time, Fate and Bonds inside {{#if world_engine contains \"TIME\"}}, "
"\"FATE\" and \"BONDS\"; replace their text with these bodies in Marinara's comment style ('{{// text }}'), drop the <bonds> wrapper "
"lines, and update the Time comment, which still says to keep it ON whenever Fate is on. The Logic Core and gate sections inline the "
"Fate, Bonds, Ledger and dice lines, which are unchanged. Then re-run compare.py. Docs: the guide's Fate and Time text describes "
"appointments, Ambitions, World news by the era's channels, Quiet turns and the Time pairing; the Chibi part should say Chibi's Fate "
"leaves these out and shows ages as n/8, n/6 and n/12, and that Time & Place is optional next to it.\n"
"REMAINING CONCERNS. (a) Chibi's Fate is a lighter engine than ARIA's; the menu's first three items (R4+R3, R2, R1) are the ones to "
"buy back if room appears. (b) The ledger template now differs from the full edition's ('age n/8' and so on): a deliberate move, "
"checked against every panel and strip regex; a chat carried between editions shows both shapes, which render alike. (c) With no "
"Logic Core (TC's lean start), nothing keeps Fate or Bonds mechanics out of the prose (R2, R16). (d) B now matters only on MINOR and "
"MAJOR turns, and a WEIGHTED MAJOR whose [hot] Bullets are all younger than 6 is left to the model (R8). (e) Without the Ambitions "
"and World rules, the ambitions and world fields fill from AMBIENT news and the field names alone, and nothing feeds residue. (f) "
"Zero slack: the group sits at exactly 605.00.")

out = {'prompts': d['prompts'], 'tc': d['tc'], 'tokens': tok, 'notes': NOTES, 'judge_notes': JUDGE}
json.dump(out, open(S + '/chibi/final/G5.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in tok.items():
    print(f'{v:9.2f}  {k}')
print('notes', len(NOTES), 'judge_notes', len(JUDGE))
