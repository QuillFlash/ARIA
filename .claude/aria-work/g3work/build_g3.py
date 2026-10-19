#!/usr/bin/env python3
"""Build chibi/drafts/G3.json from the final wording (final_text.py) and the composer (lc.py)."""
import json, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/g3work')
from lc import body, render, ab
from final_text import T

S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
ID_PLAIN = '15b770cf-6049-5f3b-b25d-be09728a65d5'
ID_TWIN = '591b8c15-985e-59f1-8c90-59e7cae236ae'

C_PLAIN = (
    "{{// 🧠 Chibi Logic Core: ARIA's planning step in about 220 tokens instead of 337 (about 254 with 🏷️ Logic Core Tags on). "
    "Before writing, the AI jots a few fragment lines: your out-of-character notes, where everyone is, what each character knows, "
    "how they sound and how your move lands, the one beat that happens next, the fresh details, and a last check on lists and jokes. "
    "Lines that other modules add (Mode, Fate, Bonds, Ledger, Layers, the 🔓 Jailbreak's Role and Frank, patch lines, Tally, Joins) join the plan and its line count. "
    "The wiring is the full edition's; only the wording is shorter. "
    "It arrives as the AI's own message after the chat, which helps many models settle into the scene. "
    "With Logic Core Tags off the AI plans inside its own reasoning. With them on, every reply opens with the plan inside <thinking> tags "
    "(The Logic Core itself starts on that tag, so a model that copies its own last message starts its reply on the tag SillyTavern folds away) "
    "and the gate gets a one-line reminder, which becomes the last line the model reads. "
    "The Tags-on sentences (opens the reply, then / closes on the line after go / The reply starts on the line after that / Every response starts with) "
    "stay word for word, because the echo-cleaning regex scripts match them. "
    "Leave this ON; if your model still overthinks, switch Reduce Reasoning on alongside it. Keep both Logic Cores above the gate in the list.}}{{trim}}\n"
)
C_TWIN = (
    "{{// 🧠 Chibi Logic Core, system-role twin: the same plan in the same size (about 220 tokens), sent as a system message. "
    "SillyTavern joins it with the 🚪 Last-Mile Gate into the very last message, so the model reads the plan rule as an instruction it was given. "
    "Try this one when your model keeps skipping the plan (MiMo V2.6 Pro has been doing that on some providers), and switch the plain Logic Core OFF. Never run both. "
    "Claude turns late system messages into user text, so Claude users keep the plain one. "
    "There is no user-role version, because a user message there breaks the jailbreak on many models.}}{{trim}}\n"
)
C_TC = (
    "{{// ARIA Chibi's end-of-prompt block, sent after your newest message every turn. "
    "The Logic Core (when aria-logic-core is on) plans the reply in about 220 tokens instead of 337; "
    "the Last-Mile Gate then gives the style rules as short instructions and carries this turn's Fate dice. "
    "Everything that changes from turn to turn lives here, so your backend can reuse the rest of the prompt. "
    "The Logic Core's Tags-on sentences stay word for word, because the regex scripts match them.}}{{trim}}\n"
)

plain = C_PLAIN + body(T)
twin = C_TWIN + body(T)
tc = C_TC + '{{#if .aria-logic-core}}' + body(T, tc=True) + '\n{{/if}}'
assert '{{#if .aria-logic-core}}' in tc


def tokens_of(text, state=None):
    t, st = render(text, state)
    return ab.tokens(t), len(t), st


def main():
    out = {
        'prompts': {
            ID_PLAIN: {'name': '🧠 The Logic Core', 'content': plain},
            ID_TWIN: {'name': '🧠 The Logic Core (system-role twin)', 'content': twin},
        },
        'tc': {'post_history_logic_core': tc},
        'tokens': {},
        'notes': open(S + '/g3work/notes.txt', encoding='utf-8').read().strip() if len(sys.argv) > 1 and sys.argv[1] == 'final' else '',
    }
    tp, cp, stp = tokens_of(plain)
    tt, ct, stt = tokens_of(twin)
    tcc, ccc, _ = tokens_of(tc, {'aria-logic-core': 'on'})
    _, _, st_on = tokens_of(plain, {'ariaThinkOpen': '<thinking>', 'ariaThinkClose': '</thinking>'})
    cue = ab.tokens(st_on.get('ariaPlanCue', ''))
    out['tokens'] = {ID_PLAIN: tp, ID_TWIN: tt, 'tc.post_history_logic_core': tcc, 'ariaPlanCue': cue}
    json.dump(out, open(S + '/chibi/drafts/G3.json' if len(sys.argv) > 1 and sys.argv[1] == 'final' else S + '/g3work/G3.try.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(S + '/g3work/draft_tc_lc.txt', 'w', encoding='utf-8').write(tc)
    print('plain', tp, cp, 'twin', tt, ct, 'tc', tcc, ccc, 'cue', cue)


if __name__ == '__main__':
    main()
