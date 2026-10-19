import json, sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
from paths import *
import aria_budget as ab

d = json.load(open(W + '/c_final_body.json', encoding='utf-8'))
codex = d['prompts'][CODEX]['content']
d['tc']['anti_slop_block'] = codex[codex.index('{{trim}}\n') + len('{{trim}}\n'):]

def exact(text, state=None):
    st = dict(state or {})
    out = ab.render(text, st, random.Random(1))
    return len(out) / 4, st

cx, st = exact(codex)
gt, _ = exact(d['prompts'][GATE]['content'])
tg, _ = exact(d['tc']['post_history_gate'])
tb, _ = exact(d['tc']['anti_slop_block'])
echo = len(st['ariaEchoGate']) / 4
chop = len(st['ariaChopGate']) / 4
d['tokens'] = {
    CODEX: cx, 'ariaEchoGate': echo, 'ariaChopGate': chop, GATE: gt,
    'tc.post_history_gate': tg, 'tc.anti_slop_block': tb,
    'group_total (Codex + Echo + Chop + gate own lines)': cx + echo + chop + gt,
}

d['notes'] = (
    "DESIGN. Each rule has one home, as in the draft: the 🚪 Last-Mile Gate carries every rule's headline (all 15 own lines, "
    "their labels, order and every {{#if}} print unchanged) and the Codex carries the details, so Codex and gate stay ON together. "
    "Balance, Count, Paragraphs and Senses live only in the gate. Count and Senses each hold their thresholds and exceptions in "
    "one self-contained gate line, which removed the Codex's Count and Senses lines and their duplicate labels. "
    "TC. post_history_gate is the CC gate body plus TC's four 'A message written as {{user}}...' notes. anti_slop_block replaces "
    "TC sysprompt.content from '{{setvar::ariaEchoGate::- ' through '</anti_slop>'; it is byte-identical to the CC Codex after its "
    "comment and {{trim}} line, as in the source (TC's Codex has no comment of its own). "
    "OVERLAPS RELIED ON: G4 🎬 Voice & Scene Engine keeps how a reply ends, feelings shown as acts and the counsellor limit; "
    "G3 🧠 Logic Core keeps 'never a paragraph per plan line'; G1 ⚡ Main Prompt keeps Card Fidelity's speech and card mood, "
    "Epistemic Limits ({{user}}'s thoughts reach nobody), and should keep New People's 'card characters stay central' and the "
    "keep-them exception (the G1 judge's work file has both); the 🔦 Flash Gate's Work words line replaces the gate's Work line "
    "while the Codex Work line still applies; the 🩹 Claude 5 patch keeps net slang for Claude."
)

d['judge_notes'] = (
    "VERDICT: approved with fixes. Exact sizes (characters / 4, comments stripped): Codex 281.5, ariaEchoGate 28.5, ariaChopGate 30.5, "
    "gate own lines 338.5 (measured with no gate prints set, Work line included); group 679.0 of the 680 ceiling sum. "
    "TC post_history_gate 338.5, TC anti_slop_block 281.5. "
    "WIRING. skeleton.py OK for both CC prompts; skeleton.py --text OK for the TC gate and the TC Codex block against the snapshot "
    "segments. The frozen checker on in-memory copies of the snapshot presets with this group swapped in reports no wiring, order "
    "or cache errors (CC everything ON 5983 -> 5232, TC 5806 -> 5055). JB.md adds nothing to these two prompts. "
    "RESTORED. Each clause was traced to the commit that introduced it; most are tester fixes. "
    "(1) Paragraphs: 'one flowing scene', 'no paragraph per point' and the lone sentence 'for a scene turn' (u/BSPiotr's "
    "GLM 5.3 Flash fix, 6993aed); the draft's 'none per point' was ambiguous and had lost the flowing scene. "
    "(2) Secrets: hidden 'in word and act', 'at most' on the backstory limit, and 'if asked or on topic' (6993aed); the draft had "
    "narrowed backstory to 'when asked' and dropped 'at most'. "
    "(3) Contrast: the Kimi K3 repair 'an act carries the true half' (3c0ff96), and the exception scoped to someone's actual claim "
    "(the false-positive set verified in 8f71074); it now names two items, a refusal or a fix of someone's claim, a denial being a fix. "
    "(4) Own words: 'odd word' (the Kimi/GLM 'ma chérie' echo fix, 89c65f0), and 'thoughts' back in the scope list (MiMo handed the "
    "player's words back inside a character's thought, 2dbc996; the draft's 'words and thoughts stay theirs' had turned it into "
    "{{user}}'s own thoughts, which Epistemic Limits already covers). "
    "(5) Senses: 'details and lines' rest four replies (Flash repeated whole lines, 2dbc996), 'reworded too', and a figure of speech "
    "only 'if plain words fail' (the simile check beta 7's judges restored). "
    "(6) Cadence: 'each act and fact once, uncounted' (issue #10's reversed, restated and timed actions, fe6c27f, and RF's 'past "
    "events uncounted', 190fa6a); the draft said 'each fact once'. "
    "(7) Chop gate: 'at most' on the one-so-or-because limit; the draft's 'one so or because a sentence' read as a quota. "
    "(8) Register: 'the speaker's world and era' (beta 7's provenance test); the draft's 'its world' read as the setting's world. "
    "It also carries most of the dropped office, legal, therapy and net idiom clause. "
    "(9) Card: 'only listed body parts' (the tail MiMo V2.6 Pro added, 2dbc996); G1 left bodies to the gate. "
    "(10) Narration: 'plain deeds and words'; G4 dropped its plain-narration sentence and relies on this line. "
    "(11) Work: quiet competence, 'skill only in use' (beta 7), kept in the Codex so it survives the Flash Gate's Work swap. "
    "(12) Humour: punchlines and self-aware asides become 'plain lines or acts' (beta 7's 'the statement behind it'; the draft "
    "said acts only). "
    "(13) Count: one gate line, 'lists and runs of phrases', with the four-item exception, so the rule of three is checked whole at "
    "the last mile; 'runs of phrases' covers parallel phrases, fragment runs and and-chains. 'unhurried' stays in the word list "
    "(Kimi used it, 32f062f). "
    "STYLE FIXES. Eight lines had exactly three semicolon fragments (Codex Humour, Register, Vocabulary and Senses; gate Humour, "
    "Paragraphs and Senses; ariaChopGate), and Contrast's exceptions were a three-item series. Every line now has 1, 2 or 4 "
    "fragments and every series has 2, 4 or more items. The Chop line lost its 'so fragments rejoin' rationale. There are no "
    "quoted examples. Kept as written: the gate's 'not/n't/never', the verbatim shared Kimi K3 line that patch gate lines repeat; "
    "'rare small card-true jokes', one noun phrase rather than a series; 'per card and first message, else lorebook', an order of "
    "precedence. "
    "SIZE AND ROW OVERAGE. The gate is 48.5 over its 290 row target and the Codex 48.5 under its 330, with the group total inside "
    "680. The overage is the restored tester fixes whose only copies are gate lines (Paragraphs, Secrets, Senses, Card, Narration), "
    "plus Count's exception moved into the gate. The source gate was about 407. Cost: about 48 more uncached tokens a turn and "
    "48 fewer cached ones; moving Count and Senses details back into the Codex would add about 9 tokens the group does not have "
    "and still leave the gate near 328. ariaChopGate is 0.5 over its 30 (tok.py rounds it to 30). "
    "NEWLY DROPPED TO PAY: the Codex Senses line 'doors and machines make plain sounds' (RF door sounds; partly covered by "
    "'Narration: plain deeds and words' and 'plain specifics replace stock phrases'); 'dust motes' from the word list; the Codex's "
    "generic 'no frame announcing speech', which the gate's 'speech opens on its point' carries while the Codex keeps the two "
    "concrete frames. "
    "STILL DROPPED FROM THE SOURCE (skins, overlaps or details): Balance's two skins (Cadence's 'each act and fact once' catches "
    "restatement); Count's 'jokes and questions included'; Chop's 'qualifiers and afterthoughts inside it' and 'force and comedy go "
    "into word choice or an act' (fragments are a closed list); Humour's reaction examples, 'pass unnoticed', closing buttons (the "
    "gate's paragraph-ending rule) and running bits; Register's 'talk to someone', 'talk about the talk', labelled points, "
    "restated question and idiom list; Work's 'a job is a fact about a life'; Cadence's 'traits fold into motion', 'in order', "
    "own-subject openings, litotes, reification and hyphen-strung coinages; 24 of the 33 banned words, 'truly' and the quoted "
    "templates; Senses' familiar traits, tells as acts (G4) and 'from their parts'; Own words' 'jokes included'; the gate's "
    "reply-ending clause (G4), Card's 'voice' and 'resting' (G1, NPC Voice), and People's 'card characters stay central' (G1). "
    "If room appears, restore in this order: traits fold into motion, hyphen-strung coinages, familiar traits go unremarked, force "
    "and comedy into word choice or acts, doors and machines, running bits."
)

json.dump(d, open(FINAL, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', FINAL)
print(json.dumps(d['tokens'], ensure_ascii=False, indent=1))
