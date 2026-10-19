"""Build the judged G3 file: the draft's texts with the judge's wording fixes and Chibi comments.

usage: python3 build_final.py OUT.json
Edits are applied to the shared body (plain Logic Core, system-role twin and the TC post_history part alike),
each asserted to occur exactly once, so the three stay identical after their comments.
"""
import json, random, sys
S = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work"
sys.path.insert(0, S + "/spec/frozen")
import aria_budget as ab

P, T = '15b770cf-6049-5f3b-b25d-be09728a65d5', '591b8c15-985e-59f1-8c90-59e7cae236ae'
D = json.load(open(S + "/chibi/drafts/G3.json", encoding='utf-8'))

EDITS = [
    # Tags-off head: the reasoning stops at go (source "Reasoning ends at go.", beta 2 echo fix dd8cc5f)
    ("Reasoning: {{getvar::logicCoreLines}} lines, then go.",
     "Reasoning: {{getvar::logicCoreLines}} lines; go ends it."),
    # "all" back on the length cap; "each building on the last" back as "built on"; funded by "no reply drafts"
    ("Fragments paraphrase speech, not reply sentences/drafts, settled once written, under one reply paragraph",
     "Fragments paraphrase speech, no reply drafts, settled and built on, all under a reply paragraph"),
    # Fresh gets its noun back
    ("- Fresh: 1-2 new; seen/heard; tied to acts;",
     "- Fresh: 1-2 new details; seen/heard; tied to acts;"),
    # Tags-on head: no "A, then B, then C" triplet; the regex anchors only "opens the reply, then "
    ("opens the reply, then {{getvar::logicCoreLines}} dashed lines, then go.",
     "opens the reply, then {{getvar::logicCoreLines}} dashed lines and go."),
]

CC_COMMENT = ("{{// 🧠 Chibi Logic Core: ARIA's planning step in about 220 tokens instead of 337 (about 253 instead of 357 "
              "with 🏷️ Logic Core Tags on). Before writing, the AI jots a few fragment lines: your out-of-character notes, "
              "where everyone is, what each character knows, how they sound and how your move lands, the one beat that "
              "happens next, the fresh details, and a last check on lists and jokes. Lines that other modules add (Mode, "
              "Fate, Bonds, Ledger, Layers, the 🔓 Jailbreak's Role and Frank, patch lines, Tally, Joins) join the plan "
              "and its line count. The wiring is the full edition's; only the wording is shorter. It arrives as the AI's "
              "own message after the chat, which helps many models settle into the scene. With Logic Core Tags off the AI "
              "plans inside its own reasoning and ends it at go. With them on, every reply opens with the plan inside "
              "<thinking> tags (The Logic Core itself starts on that tag, so a model that copies its own last message "
              "starts its reply on the tag SillyTavern folds away) and the gate gets a one-line reminder, which becomes "
              "the last line the model reads. The phrases the echo-cleaning regex scripts match (opens the reply, then / "
              "closes on the line after go / The reply starts on the line after that / Nothing above go enters the reply "
              "/ Every response starts with) stay word for word. Leave this ON; if your model still overthinks, switch Reduce "
              "Reasoning on alongside it. Keep both Logic Cores above the gate in the list.}}")

TC_COMMENT = ("{{// The Chibi Edition's end-of-prompt block, sent after your newest message every turn. The Logic Core "
              "(when aria-logic-core is on) plans the reply in about 250 tokens, 280 with aria-thinking-tags on (the full "
              "edition's takes about 360 and 380); the Last-Mile Gate then gives the style rules as short instructions and "
              "carries this turn's Fate dice. Everything that changes from turn to turn lives here, so your backend can "
              "reuse the rest of the prompt. The Logic Core phrases the regex scripts match (opens the reply, then / closes "
              "on the line after go / The reply starts on the line after that / Nothing above go enters the reply / Every "
              "response starts with) stay word for word.}}")


def apply(text, edits):
    for old, new in edits:
        n = text.count(old)
        assert n == 1, (old, n)
        text = text.replace(old, new)
    return text


def swap_comment(text, comment):
    head, sep, rest = text.partition('}}{{trim}}')
    assert sep and head.startswith('{{//') and '{{' not in head[4:], 'comment shape'
    return comment + '{{trim}}' + rest


def build():
    d = json.loads(json.dumps(D))
    for pid in (P, T):
        d['prompts'][pid]['content'] = apply(d['prompts'][pid]['content'], EDITS)
    d['prompts'][P]['content'] = swap_comment(d['prompts'][P]['content'], CC_COMMENT)
    d['tc']['post_history_logic_core'] = swap_comment(apply(d['tc']['post_history_logic_core'], EDITS), TC_COMMENT)
    return d


def exact(text, state):
    st = dict(state)
    return len(ab.render(text, st, random.Random(1))) / 4, st


if __name__ == '__main__':
    d = build()
    tags = {"ariaThinkOpen": "<thinking>", "ariaThinkClose": "</thinking>"}
    off, _ = exact(d['prompts'][P]['content'], {})
    twin, _ = exact(d['prompts'][T]['content'], {})
    on, st = exact(d['prompts'][P]['content'], tags)
    tc_off, _ = exact(d['tc']['post_history_logic_core'], {"aria-logic-core": "on"})
    tc_on, _ = exact(d['tc']['post_history_logic_core'], dict(tags, **{"aria-logic-core": "on"}))
    cue = len(st['ariaPlanCue']) / 4
    d['tokens'] = {
        P: off,
        T: twin,
        'tc.post_history_logic_core': tc_off,
        '15b770cf / 591b8c15 with Logic Core Tags on': on,
        'tc.post_history_logic_core with aria-thinking-tags on': tc_on,
        'ariaPlanCue (Tags on, unchanged)': cue,
        'group G3 (row ceiling 220, Tags off, no module lines; plain and twin never run together)': off,
    }
    json.dump(d, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(json.dumps(d['tokens'], ensure_ascii=False, indent=1))
