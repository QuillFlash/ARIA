import sys, random, importlib.util, json
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
sys.path.insert(0, f'{S}/spec/frozen')
import aria_budget as ab
spec = importlib.util.spec_from_file_location('mk', f'{S}/chibi/work/G1/make_g1.py'); mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)

def tok(s):
    return ab.tokens(ab.render(s, {}, random.Random(1)))

Y = list(mk.MAIN_BODY)
base = tok('\n'.join(Y))
print('Y body tokens', base)

def apply(lines, idx, old, new):
    assert lines[idx].count(old) == 1, (idx, old)
    out = list(lines); out[idx] = out[idx].replace(old, new); return out

# cut patches Y -> E (applied in order)
cuts = [
 (1, " unless OOC allows", ""),
 (6, "; mood and energy hold at the card's level, shifting over dozens of turns", ""),
 (7, "; at most one distinctive taste matches {{user}}'s", ""),
 (9, " unless the card says otherwise", ""),
 (4, "OOC-named language", "OOC language"),
 (8, "Real Characters: fallible people with wants and no plot armor.", "Real Characters: wants of their own, no plot armor."),
]
cur = list(Y); prev = base
for idx, old, new in cuts:
    cur = apply(cur, idx, old, new)
    t = tok('\n'.join(cur))
    print(f'cut line {idx+1}: {old!r} -> {new!r}: {prev - t} saved, body now {t}')
    prev = t
E = cur
print('E body tokens', tok('\n'.join(E)))
json.dump({'Y': Y, 'E': E}, open(f'{S}/chibi/work/G1/YE.json', 'w'), ensure_ascii=False, indent=1)

# restore items on top of Y (each independent), measured against Y
R = [
 ("R1", 6, "whatever the name suggests;", "whatever the name suggests; a described body has only the parts listed;", "Card Fidelity: bodies (Gate Card line and the DeepSeek Bodies line also carry it)"),
 ("R2", 10, "New People: a new name", "New People: newcomers keep to the scene's edge and leave when done, unless {{user}} keeps them; a new name", "New People: edge and leave (Gate People line carries it)"),
 ("R3", 10, "setting-fitting ones.", "setting-fitting ones, never Elara, Vane, Vance or Seraphina.", "New People: the banned-name list"),
 ("R4", 5, "reach nobody;", "reach nobody, first message included;", "Epistemic: first message included"),
 ("R5", 5, "(speech however marked), were told or deduced;", "(speech however marked; walls stop normal speech), were told or deduced;", "Epistemic: walls"),
 ("R6", 4, "even for modern things.", "even for modern things; natives borrow only from trade or online life.", "Story Language: borrowing exception"),
 ("R7", 9, "Slow Burn: love after", "Slow Burn: love and sex grow from shared time; love after", "Slow Burn: grows from shared time"),
 ("R8", 9, "otherwise.", "otherwise; intimacy stays persona-true.", "Slow Burn: intimacy persona-true (Mode line also carries it)"),
 ("R9", 8, "with wants and no plot armor.", "with wants and no plot armor; they refuse, hold grudges and finish what they start; rudeness, ego, coldness or hostility needs a cause.", "Real Characters: grudges, finish, cause"),
 ("R10", 2, "write dark material frankly.", "write dark material frankly, moral judgment left to characters.", "Match: moral judgment (Gate Narration line carries it)"),
 ("R11", 3, "World: consequences", "World: impartial; consequences", "World: impartial"),
 ("R12", 3, "and last.", "and last; secrets stay hidden until found.", "World: secrets (Gate Secrets line carries it)"),
 ("R13", 6, "nerves keep stalls and restarts;", "nerves keep stalls and restarts inside sentences that still reach their point; embarrassment and incompetence stay unpolished, self-commentary in their own voice; ease with one person stays with them; a quirk that fades for no story reason returns next reply;", "Card Fidelity: nerve detail, polish, ease, quirk"),
 ("R14", 7, "tastes and opinions", "tastes, hobbies, opinions and quirks", "PI: full list of four"),
 ("R15", 7, "fill card gaps once;", "fill card gaps once, from one trait and one setting element;", "PI: how a gap is filled"),
]
for rid, idx, old, new, why in R:
    t = tok('\n'.join(apply(Y, idx, old, new)))
    print(f'{rid}: +{t - base:3}  {why}')
