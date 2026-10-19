import sys, random, importlib.util, json
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
sys.path.insert(0, f'{S}/spec/frozen')
import aria_budget as ab
spec = importlib.util.spec_from_file_location('mk', f'{S}/chibi/work/G1/make_g1.py'); mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)

def tok(s): return ab.tokens(ab.render(s, {}, random.Random(1)))
Y = list(mk.MAIN_BODY); base = tok('\n'.join(Y))
def apply(lines, idx, old, new):
    assert lines[idx].count(old) == 1, (idx, old)
    out = list(lines); out[idx] = out[idx].replace(old, new); return out

# fallback ladder Y -> E, in order
cuts = [
 ('a', 8, "Real Characters: fallible people with wants and no plot armor.", "Real Characters: wants of their own, no plot armor.", "Real Characters line becomes"),
 ('b', 4, "OOC-named language", "OOC language", "Story Language"),
 ('c', 1, " unless OOC allows", "", "Correct Perspective: drop"),
 ('d', 9, " unless the card says otherwise", "", "Slow Burn: drop"),
 ('e', 7, "; at most one distinctive taste matches {{user}}'s", "", "Personality Independence: drop"),
 ('f', 6, "; mood and energy hold at the card's level, shifting over dozens of turns", "", "Card Fidelity: drop"),
]
cur = list(Y); prev = base; ladder = []
for tag, idx, old, new, label in cuts:
    cur = apply(cur, idx, old, new); t = tok('\n'.join(cur)); ladder.append((tag, prev - t, label, old, new)); prev = t
assert prev == 260, prev
# alternative cuts (each measured against Y alone)
alts = [
 ("; reads of {{user}} are guesses", 5, "; reads of {{user}} are guesses", ""),
 (" (speech however marked)", 5, " (speech however marked)", ""),
 (", even for modern things" if False else "even for modern things", 4, ", with inflected native words even for modern things", ""),
 ("; nerves keep stalls and restarts", 6, "; nerves keep stalls and restarts", ""),
 ("; {{user}}'s name changes only at the card's or {{user}}'s lead", 6, "; {{user}}'s name changes only at the card's or {{user}}'s lead", ""),
]
alt_out = []
for label, idx, old, new in alts:
    t = tok('\n'.join(apply(Y, idx, old, new))); alt_out.append((old, base - t))

R = [
 ("R1", 6, "whatever the name suggests;", "whatever the name suggests; a described body has only the parts listed;", "Card Fidelity, after \"whatever the name suggests;\""),
 ("R2", 10, "New People: a new name", "New People: newcomers keep to the scene's edge and leave when done, unless {{user}} keeps them; a new name", "New People, before \"a new name\""),
 ("R3", 10, "setting-fitting ones.", "setting-fitting ones, never Elara, Vane, Vance or Seraphina.", "New People, line end"),
 ("R4", 6, "nerves keep stalls and restarts;", "nerves keep stalls and restarts inside sentences that still reach their point;", "Card Fidelity nerves"),
 ("R5", 6, "nerves keep stalls and restarts;", "nerves keep stalls and restarts; embarrassment and incompetence stay unpolished, self-commentary in their own voice;", "Card Fidelity, after nerves"),
 ("R6", 6, "nerves keep stalls and restarts;", "nerves keep stalls and restarts; ease with one person stays with them; a quirk that fades for no story reason returns next reply;", "Card Fidelity, after nerves"),
 ("R7", 5, "reach nobody;", "reach nobody, first message included;", "Epistemic Limits"),
 ("R8", 5, "(speech however marked),", "(speech however marked; walls stop normal speech),", "Epistemic Limits"),
 ("R9", 4, "even for modern things.", "even for modern things, natives borrowing only from trade or online life.", "Story Language"),
 ("R10", 9, "Slow Burn: love after", "Slow Burn: love and sex grow from shared time; love after", "Slow Burn"),
 ("R11", 9, "otherwise.", "otherwise; intimacy stays persona-true.", "Slow Burn"),
 ("R12", 8, "with wants and no plot armor.", "with wants and no plot armor; they refuse, hold grudges and finish what they start; rudeness, ego, coldness or hostility needs a cause.", "Real Characters"),
 ("R13", 2, "write dark material frankly.", "write dark material frankly, moral judgment left to characters.", "Match"),
 ("R14", 3, "World: consequences", "World: impartial; consequences", "World"),
 ("R15", 3, "and last.", "and last; secrets stay hidden until found.", "World"),
 ("R16", 7, "tastes and opinions", "tastes, hobbies, opinions and quirks", "Personality Independence"),
 ("R17", 7, "fill card gaps once;", "fill card gaps once, from one trait and one setting element;", "Personality Independence"),
]
res = []
for rid, idx, old, new, where in R:
    t = tok('\n'.join(apply(Y, idx, old, new))); res.append((rid, t - base, where, old, new))

def ins(old, new):
    # show only the inserted text
    i = 0
    while i < len(old) and i < len(new) and old[i] == new[i]: i += 1
    j = 0
    while j < len(old) - i and j < len(new) - i and old[-1 - j] == new[-1 - j]: j += 1
    return new[i:len(new) - j]

counted_total = tok('\n'.join(Y)) + 3 + 32
lines = []
A = lines.append
A("G1 NOTES FOR THE JUDGE")
A("")
A("1. MAIN IS OVER ITS CEILING: %d tokens against 260 (+%d). READ THIS FIRST." % (base, base - 260))
A("CHIBI.md asks for two things that cannot both hold for this prompt. The nine labelled rules plus the two opening lines need about 300 tokens at one core each, because the labels alone cost 36 and the numbers and exceptions CHIBI.md names (dozens of turns, a date or two, fifth of five, at most one taste, nerves keep stalls, unless OOC allows, unless the card says otherwise) add about 45. I kept those and cut what the always-on Gate, the plan or NPC Voice already say (section 3), and I wrote every line as tightly as I could (lean fragments, no rationale).")
A("Group arithmetic with the relief valve: main %d + story 3 + impersonation 100 + reduce 32 = %d against rows 260 + 3 + 100 + 40 = 403 (+%d). Only 8 tokens could be saved inside the group (Reduce Reasoning), so the overshoot is real. In the fully-kitted-out count (main + story + reduce) it is %d against 303." % (base, base + 135, base + 135 - 403, counted_total))
A("")
A("2. FALLBACK TO EXACTLY 260 (apply in order, each step exact and measured; tokens saved in brackets; the six steps give 260):")
for tag, saved, label, old, new in ladder:
    if tag == 'a':
        A("  a) [-%d] Real Characters line becomes \"%s\"" % (saved, new))
    elif tag == 'b':
        A("  b) [-%d] Story Language: \"OOC-named language\" -> \"OOC language\"" % saved)
    else:
        A("  %s) [-%d] %s \"%s\"" % (tag, saved, label, old))
A("If you would rather keep the dozens-of-turns clause (f, the costliest), cut instead from: " + "; ".join("\"%s\" [-%d]" % (o, n) for o, n in alt_out) + ".")
A("")
A("3. RESTORE LIST if global slack appears (token cost added to the %d-token draft, each independent, inserted text exact; roughly best first):" % base)
order = ["R1","R2","R4","R3","R7","R5","R8","R9","R10","R11","R12","R15","R13","R6","R17","R14","R16"]
rm = {r[0]: r for r in res}
for rid in order:
    _, d, where, old, new = rm[rid]
    A("  %s [+%d] %s: insert \"%s\"" % (rid, d, where, ins(old, new)))
A("Where the long form still lives: bodies = Gate Card line and the DeepSeek patch Bodies line; resting temperament = Gate Card line and the plan's Voice line; newcomers' place = Gate People line; secrets = Gate Secrets line and the plan's Knows line; verdicts = Gate Narration line and the Scene Engine; looks, speech and thought form = NPC Voice and Gate Card; intimacy persona-true = the Adult Mode line.")
A("")
A("4. MAIN MECHANICS, source -> draft.")
A("Kept: game master playing everyone but {{user}}; OOC first; {{user}}'s words, deeds, thoughts and knowledge stay the player's unless OOC allows; match tone, tense, POV, format, length; dark material frankly; consequences fit skill and circumstance and last; {{user}}'s or the OOC language; inflected native words even for modern things; NPCs know only what they saw, heard (speech however marked), were told or deduced; narration and {{user}}'s thoughts reach nobody; reads of {{user}} are guesses; gender and pronouns from card and first message, else lorebook, whatever the name suggests; mood and energy hold, shifting over dozens of turns; nerves keep stalls and restarts; {{user}}'s name changes only at the card's or {{user}}'s lead; tastes and opinions from card or archetype and setting, never {{user}}; fill card gaps once; at most one distinctive taste matches; fallible, wants, no plot armor; love after a date or two is love-bombing unless the card says otherwise; a new name is the fifth of five setting-fitting ones. All nine labels kept (Correct Perspective is named by the preset's own impersonation_prompt setting; the plan points at Story Language, Epistemic Limits, Card Fidelity and Personality Independence; Freaky and Adult name Personality Independence, Slow Burn and Real Characters).")
A("Cut or shortened (restore ids above): genre, 'impartial and consistent', 'directly'; moral judgment left to characters (R13); secrets until found (R15); a described body has only the listed parts (R1); newcomers keep to the edge and leave when done (R2); banned names (R3); first message included, walls, {{user}}'s past from the chat and card, strangers notice what strangers would (R7, R8); looks, speech, thoughts, movement set by the card; 'or chat' as a gender source; nerves 'inside a sentence that still reaches its point' (R4); embarrassment and incompetence unpolished, self-commentary in their own voice (R5); ease with one person, a faded quirk returns next reply (R6); speakers say I, the name returns after a jab or pet name; hobbies (R16); one trait and one setting element (R17); Real Characters: card's scale, cooperate, hesitate, withdraw, grudges, call out lies, carry out decisions fully, doing nothing is a turn, rudeness needs a cause (R12); Slow Burn: affection, confessions, grows from shared time and history (R10), intimacy persona-true (R11); borrowing only from trade or online life (R9).")
A("")
A("5. OTHER PROMPTS.")
A("Impersonation Turn 100 (ceiling 100): all seven mechanics kept (write the next message; plan only {{user}}'s move from persona and earlier messages; knows only what was perceived or told; start on the first word or action; stop where another character would answer; no header, character lines, 🎲 or 💚 block whatever the plan says; this turn's POV replaces any earlier one: first person present unless earlier messages differ). Dropped the <impersonation_turn> wrapper pair (10 tokens, referenced nowhere), kept <POV>. 'they' replaces repeated {{user}} (no gendered pronouns).")
A("Reduce Reasoning 32 (ceiling 40): the three constraints are kept (one simple plan; skip crafting, drafting, refining; write outside the thinking block at once). The <reasoning_constraints> wrapper (12 tokens) and the 'Strictly follow' header are gone, and 'crafting, drafting and refining' was a list of three, so rechecking makes it four.")
A("Story Context 3, Custom Instructions 0, Logic Core Tags 0 (it still sets ariaThinkOpen 2 and ariaThinkClose 3): comments only. Custom Instructions had its comment twice; it is now once, and the rendered output is identical (checked with the checker's render). README (disabled): new short Chibi README in Aria's voice with the sizes (3,000 fully kitted out, about 1,500 as shipped), the differences, the guide link and a five-step soundcheck. Sampling Advice: shortened comment, same facts.")
A("")
A("6. SKELETON (skeleton.py against the snapshot CC): Main differs by exactly setvar::ariaJb and setvar::ariaJbLines appended to the blanking run; Impersonation Turn by exactly setvar::ariaJb; the other six prompts are OK. tc.main_prompt differs from the TC source span by the same two blanks only.")
A("")
A("7. FLAGS.")
A("(i) Cross-group dependency: Main now leans on the Gate's Card, Knows, Secrets, People and Narration lines for bodies, resting temperament, newcomers' place, secrets and verdicts, so G2 must keep their cores. (ii) The plan's Voice line points 'register' at Card Fidelity, but speech now lives in NPC Voice; G3 may re-point it. (iii) The preset-level impersonation_prompt names 'Correct Perspective'; keep that label in Main and in Marinara. (iv) The README stamps say 'Version 1.0 beta 8'; sync them if ARIA's stamp changes. (v) TC splice: tc.main_prompt replaces the span from {{setvar::ariaDice::}} to the {{/if}} that closes the player-instructions block; tc.readme_comment replaces the whole first {{// README ... }}{{trim}} unit; tc.custom_instructions_comment replaces only that comment macro (the {{trim}} after it stays).")
open(f'{S}/chibi/work/G1/notes.txt', 'w', encoding='utf-8').write('\n'.join(lines))
print('\n'.join(lines))
print()
print('notes chars', len('\n'.join(lines)))
