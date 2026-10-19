## 7. Meet Chibi me (the Chibi Edition)

Guess who shrank in the wash? It's me, Aria, in my brand-new chibi form! 🎀

(Nangong Yu: Smol Aria is STILL loud, dearie.)

The Chibi Edition is the same band with a smaller backpack, packed for small context windows, small local models and thrifty wallets. Every entry, toggle and switch of the full edition is still here, with the same names and the same wiring, so sections 3 to 6 and 8 all apply to it. What changed is the wording: each rule keeps its checkable core (its numbers, thresholds and exceptions) and loses the extra explaining, in the concise style of Realistic Frankenstein's Douyin Edition. Chibi is brand new, though, and no live model has met it yet. If your model and your wallet can take the full me, that's still the tested pick.

### The three files

Chibi comes in three files that sit next to the full ones, plus the regex file my Text Completions editions share:

| File | For | Install it like |
|---|---|---|
| `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json` | Online models: Claude, Gemini, DeepSeek, OpenRouter and friends | [Section 2](#2-install-me-in-five-steps) |
| `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json` | Models on your own computer | [Section 6](#6-run-me-on-your-own-computer) |
| `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition — Agent Gating.json` | Marinara Engine | Below |

- **Chat Completions.** Follow the five steps of section 2 with the Chibi file. The prompt list still starts with 🌳 README and ⚡ ARIA Main Prompt, and the README entry's title line says Chibi Edition. Allow the regex scripts when SillyTavern asks. They're the very same ones the full file carries.
- **Text Completions.** Follow section 6 with the Chibi file. Both dropdowns should read **ARIA 1.0 beta 8 Chibi Edition (Text Completions)**, and the five settings, the switch lines, the thinking setup and the speed tips are all the same. One difference: Chibi starts with 🧠 The Logic Core already ON, because without it my lean start would be only about 1,300 tokens. The regex file is shared too: `regex/ARIA 1.0 Regex Scripts (Text Completions).json` serves both Text Completions editions, so one copy covers whichever one you run. Make it the current copy, though. An older copy can leave the last lines of a plan behind when a model echoes it, so delete the old ARIA scripts from the **Global** list before you import the new file, as section 6 describes.
- **Marinara Engine.** The third file is a Marinara preset, built on u/BSPiotr's Marinara layout. Import it into Marinara Engine like any Marinara preset, then pick your options in its choice blocks (adult mode, point of view, core modules, world engine, model patch, Logic Core, Logic Core options and State backend) instead of flipping toggles. The Marinara file carries no regex scripts, so there are no panels and no 💭 Thoughts box there. Chibi's starting choices leave 🎲 Fate and ⏰ Time & Place unticked. The file also ships five sections switched off in Marinara's own section list: 😈 Freaky Override, 🐺 Anthro Vocals, 🩹 Claude 5, 🩹 Gemini and 🩹 MiMo V2.6 Pro. Picking one of those choices doesn't bring that entry's own text until you switch its section on too.

### How big am I?

Measured with `python3 tools/aria_budget.py` (and the Marinara render checker for the third file), which counts rendered text with comments stripped (characters ÷ 4). My cap is 3,000 tokens fully kitted out, and every path but one stays at or under it:

| Configuration | Full edition | Chibi Edition |
|---|---|---|
| Chat Completions, shipped default | ~4,230 | ~1,500 |
| Chat Completions, fully kitted out (everything ON, with the largest patch, 🩹 GLM) | ~6,110 | 2,978 |
| An Impersonate turn against that | ~190 fewer | ~120 fewer |
| Text Completions, lean start | ~2,900 | ~1,590 |
| Text Completions, plus The Logic Core, Fate and Time & Place | ~4,320 | ~2,025 |
| Text Completions, everything ON (🩹 GLM, 🔦 Flash Gate, 🧷 Character Hold and 🔓 Jailbreak included) | ~6,100 | 2,997 |
| Marinara, everything ticked with 🩹 GLM, no agents | ~6,120 | 2,984 |
| Marinara, the same with the Agents state backend | ~6,380 | 3,070 |

Chibi's Chat Completions file ships 🎲 Fate & Chekhov Ledger and ⏰ Time & Place OFF, which is how its shipped default lands near 1,500 (the full file ships both ON). Chibi's Text Completions file starts with The Logic Core ON and the full one starts with it OFF, so those two lean starts aren't a fair match: switch The Logic Core off and Chibi's lean start would be about 1,290.

The Agents state backend in Marinara is my one exception to the cap, on purpose. Its protocol note adds about 86 tokens (the full edition's adds about 260), so with 🩹 GLM everything ticked comes to 3,070, about 70 over. Every other patch stays at or under 3,000 there; the nearest is 🩹 MiMo V2.6 Flash at 2,999.

Here's where the tokens went, entry by entry, with everything ON in the Chat Completions file (the checker's own table):

| Entry | Full edition | Chibi Edition |
|---|---|---|
| ⚡ ARIA Main Prompt | 716 | 306 |
| 🔞 Adult Context | 116 | 75 |
| 😈 Freaky Override | 54 | 30 |
| 👀 Hybrid POV | 46 | 22 |
| 🎬 Voice & Scene Engine | 271 | 110 |
| 🎭 NPC Voice & Emotions | 349 | 114 |
| 🐺 Anthro Vocals | 128 | 45 |
| 🖋️ Anti-Slop Codex | 936 | 282 |
| 👃 Scent Occasions | 94 | 47 |
| ⏰ Time & Place | 82 | 47 |
| 🎲 Fate & Chekhov Ledger | 853 | 323 |
| 🥰 Bonds Lite | 297 | 124 |
| 🧠 The Logic Core, with every module's lines in it | 916 | 596 |
| 🚪 Last-Mile Gate, with every module's lines in it | 1,150 | 815 |
| Reduce Reasoning | 78 | 17 |

### How I differ from the full edition

- **Every module is compressed.** Rules are short do-this sentences, one rule per clause, and plan and gate lines are fragments joined by semicolons. The checkable core of each rule survives: its numbers and thresholds, its exceptions (a nervous card keeps its stammers, a refusal stays a plain no) and each patch's own lines. Restatements, explaining and overlaps are what went, plus a few small details that most entries' comments list. That comment is the note at the top of an entry's text, and it costs no tokens. The 🩹 Claude 5 patch still holds the preset's only quoted repairs, shortened.
- **Each rule lives in one place.** The ⚡ Main Prompt leaves bodies, resting temperament, what characters know, secrets, newcomers at the edge and verdict-free narration to the 🚪 Last-Mile Gate, and the 🖋️ Anti-Slop Codex is written as the details of the gate's rules (Balance, Count, Paragraphs and Senses live only in the gate). So keep all three ON, the Main Prompt, the Codex and the gate.
- **Fate and Time ship OFF.** Switch 🎲 Fate on when your model and context can take it. ⏰ Time & Place is optional next to it, since Chibi's Fate keeps no timed appointments to hang a clock on.
- **A lighter Fate.** The three dice, the tier ladder with its thresholds, the ledger fields and the tester fixes (for q, threads, whole and unwarned MAJOR events, ripe World entries, folded AMBIENT lines and the natural-20 limit) are all there. What Chibi's Fate leaves out are the full edition's timed appointments, Ambitions, World-news and Quiet-turn rules, plus some cell details. So it won't log a goal you state as an Ambition, fire an appointment on time, or run the full edition's rules for how news reaches the page and for quiet turns.
- **Ledger ages written n/8, n/6 and n/12.** Chibi puts the age limits into the ledger itself: a thread's age reads n/8, a Deferred item's n/6 and a Bullet's n/12, where the full edition writes plain ages. The same regex scripts dress the ledger up as the same orange panel.
- **A lighter Bonds.** The BOND scale from -10 to +20, the Sparks, Grudge and conversions (7 Sparks make one point, 5 Grudge cost one, 3 Grudge halve the gains and a sincere repair clears them) and the touch gates (+4 hug, +8 hand-holding, +12 kiss, +15 sex) are all kept, and so is the teal 💚 panel. The long description of each tier (hostile, neutral, warm, trust, devoted) and the `<bonds>` tags are gone.
- **The 🔓 Jailbreak is in, and OFF.** It needs 🔞 Adult Context and a Logic Core, like the full one. It's the same two plan lines, a Role line and a Frank line, in about 55 tokens instead of 130. Sex still stays between adults, and the same parts of Realistic Frankenstein's jailbreaks stay out. Chibi's version leaves out the full one's bolder-choice rule and its acting-on-wants and every-rule-in-full wording.
- **Marinara's Agents path runs over 3,000.** That's the one exception above, and it's on purpose.

### Chibi's Text Completions switches

Chibi keeps every `aria-*` switch under the same name. This table flips one switch at a time from Chibi's shipped state, so The Logic Core is already on and each row includes its plan line. The last column is the full edition measured the same way, with The Logic Core on too, so it isn't the table in section 6, which flips from the full file's shipped state with it off.

| Switch | Starts | Chibi | Full edition |
|---|---|---|---|
| `aria-logic-core` | on | ~300 | ~405 |
| `aria-thinking-tags` | on | ~55 | ~40 |
| `aria-adult` | off | ~85 | ~130 |
| `aria-freaky` | off | ~30 | ~50 |
| `aria-jailbreak` | off | ~55 | ~130 |
| `aria-hybrid-pov` | off | ~45 | ~85 |
| `aria-npc-voice` | on | ~115 | ~350 |
| `aria-anthro` | off | ~45 | ~130 |
| `aria-scent` | on | ~70 | ~120 |
| `aria-time-place` | off | ~45 | ~85 |
| `aria-fate` | off | ~390 | ~930 |
| `aria-bonds` | off | ~200 | ~380 |
| `aria-patch-glm` | off | ~360 | ~610 |
| `aria-patch-kimi-qwen` | off | ~80 | ~120 |
| `aria-patch-mimo-pro` | off | ~110 | ~130 |
| `aria-patch-mimo-flash` | off | ~290 | ~445 |
| `aria-patch-deepseek` | off | ~310 | ~440 |
| `aria-flash-gate` | off | ~125 | ~215 |
| `aria-character-hold` | off | ~55 | ~90 |

With the 🩹 DeepSeek patch, the Tally line adds about 40 tokens with Fate, 75 with Bonds or 95 with both (the full edition's adds about 50, 90 and 125).

### Which me should I pick?

- **Plenty of context and budget, or you want the version the testers have run?** The full me.
- **A small context window, a small local model, or you pay by the token?** Chibi me! Start from the defaults, and switch 🎲 Fate on when your model can take the extra weight.
- **Not sure?** Try the full me first, and swap to Chibi if it feels heavy. Both editions keep the same toggle names, so your habits carry over.

