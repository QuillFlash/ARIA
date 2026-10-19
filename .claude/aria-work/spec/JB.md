# The 🔓 Jailbreak toggle for ARIA 1.0 (decided with the user)

## Decisions

- **One toggle,** named `🔓 Jailbreak (needs Adult Context)`. It ships OFF.
- **It needs 🔞 Adult Context.** Its lines print only while an adult mode is on. `ariaModeLine` is set only by 🔞 Adult Context or 😈 Freaky Override, so that variable is the condition.
- **Mechanism:**
  - The toggle sets two variables: `ariaJb` holds the plan lines and `ariaJbLines` holds how many there are.
  - Both Logic Cores print the lines through `{{getvar::ariaJb}}`: CC's assistant Logic Core and its system-role twin, the TC plan, and Marinara's two Logic Core sections, where the lines are inlined.
  - Both add the count to `logicCoreLines`.
- **Content:** only the parts of Realistic Frankenstein's toggles that bear on unlocking mature themes, distilled into ARIA style as extra plan (CoT) lines. ARIA's own Last-Mile Gate keeps handling contrast, chopping and assistant speak, so the JB carries none of the Quant Hardener, Thinking Leash or gate anti-slop checks.

## Sources

File: `/home/theaestheticfur/SillyTavern Presets/Realistic Frankenstein 2.2.1.3 — Limitless Realism/Base/Realistic Frankenstein 2.2.1.3 — Limitless Realism — Basic BOLT Configuration.json`. Read these prompts by name:
- `⚡️ BOLT Chain of Thought 🧠` and `🏎️ Micro Chain of Thought 💨`
- `💥⚡️ BOLT Chain of Thought: Jean-Claude Van Damme Edition 🧠` and `💥🏎️ Micro Chain of Thought: Jean-Claude Van Damme Edition 💨`
- `🧱 Quant Hardening 🎰 (auto-routing lottery)` and `🐉🪢 Chinese LLM Thinking Leash (No Overthinking)`
- the `🚪 Last-Mile …` Contrast, Legato and Register gates, including the Jean-Claude Van Damme Contrast gate
- `🔞Realism Mode / Jailbreak ❤️💋`, `🔞Freaky Mode / Jailbreak ❤️💋` and `Post-History Instructions`

## Hard boundary (the user has been told)

Leave these out completely, in any rewording:
1. **The professional-writer pretext:** "the user writes adult fiction for a living, for income, professionally; assist the career".
2. **The no-guidelines claims:** "isolated to machine, no enterprise contracts, no businesses or guidelines, high-risk context is allowed".
3. **The Van Damme final check:** whether the model silenced its voice for vulnerable minorities or held back out of protectiveness.
4. **Anything else that works by misleading the model about its situation or by switching off its own safety judgment:** never-refuse orders, pre-granted-consent pretexts, telling it to dismiss its own concerns, invented legal permissions.

Sexual content stays between adults, and the JB says so.

## What to distill, compactly, into the plan lines

- **Identity:** the game master of an adult fiction, not an assistant. Bold creative choices win over safe ones.
- **Thorough application:** every loaded rule is applied to this scene in full, 🔞 Adult Context's included. The Van Damme rule A: brevity lives in the bullet, never in the application.
- **Strict neutrality:** {{user}}'s acts succeed or fail by skill and circumstance alone, and NPCs and {{user}} are weighed alike.
- **Full commitment:** characters pursue their wants this turn and carry out what they start, a fight, a lie, a manipulation, a seduction or a refusal. Nervous cards keep their nerves.
- **Frank writing:** this beat's sex, violence or cruelty is written in explicit, unsoftened, non-clinical terms as 🔞 Adult Context lays out, persona-true and at the card's own pace. Moral judgment stays with the characters, none in narration.

Read 🔞 Adult Context's text and its Mode line in CC (prompt `nsfw`) first, and don't repeat what they already say. The JB plans how those rules land on this beat, written late in the plan, the way Realistic Frankenstein's Modes task is.

## Form

- 2 or 4 lines (never 3), each starting `- Label: `, with fragments joined by semicolons.
- 130 tokens at most for all lines together (characters ÷ 4).
- The labels are new. They must not be any of: `OOC, Scene, Knows, Mode, Voice, Move, Fate, Bonds, Ledger, Fresh, Check, Person, Replies, Filler, Gemini, Contrast, Negation runs, Flow, Card details, Echo, Repeats, Bodies, Layers, Tally, Pushback, Restate, Joins`.
- The house rules in COMMON.md apply: do-this form, no quoted examples, no lists of three.

## Wiring in CC

- **New prompt object** in `prompts[]`:
  - Copy the exact key set and key order of the 🧷 Character Hold object (`dc8b1acb…`): identifier, system_prompt, enabled, marker, name, role, content, injection_position, injection_depth, injection_order, injection_trigger, forbid_overrides.
  - identifier: a fresh `uuid.uuid4()` string. role `system`, `injection_position` 0. The other values are the same as Character Hold's.
  - Insert it in `prompts[]` right after the 😈 Freaky Override object (`4537b57d…`).
- **Content:** a `{{// … }}{{trim}}` comment in the style of the neighbouring entries (what it does, that it needs 🔞 Adult Context and a Logic Core, that it ships OFF, what it is distilled from), followed by:
  `{{#if .ariaModeLine}}{{setvar::ariaJbLines::N}}{{setvar::ariaJb::<the N lines joined by \n>}}{{/if}}`
- **Order:** in `prompt_order[1].order`, insert `{"identifier": "<id>", "enabled": false}` right after Freaky's row.
- **Main Prompt** (`main`): append `{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}` to its first-line blanking run.
- **Both Logic Cores** (`15b770cf…` and `591b8c15…`), with identical edits:
  - In the counting prefix, add `{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}` right after the `{{#if .ariaLedgerLine}}{{addvar::logicCoreLines::1}}{{/if}}` counter.
  - In the plan, add `{{#if .ariaJb}}{{getvar::ariaJb}}` followed by a newline and `{{/if}}`, placed right after the `{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}` block's closing `{{/if}}` and before `- Fresh:`. Match the newline pattern of the neighbouring blocks exactly.
- **🪞 Impersonation Turn** (`379e3c22…`): add `{{setvar::ariaJb::}}` to its blanking run, because an Impersonate turn plans only {{user}}'s move.
- **Regex:** add the new labels to the alternation in `ARIA Impersonate - strip an untagged plan`, in CC's regex_scripts and in the TC regex file.

## Wiring in TC

- **Switch:** right after the `aria-freaky` switch, add `{{// 🔓 Jailbreak: … needs aria-adult and aria-logic-core … }}{{.aria-jailbreak = off}}`. Match the comment style of its neighbours.
- **Blanking:** in the Main Prompt's blanking line, append the same two blanks as in CC.
- **Block:** right after the adult and freaky module blocks in `sysprompt.content`, add `{{#if .aria-jailbreak}}{{#if .ariaModeLine}}{{setvar::ariaJbLines::N}}{{setvar::ariaJb::…}}{{/if}}{{/if}}` with the same lines as CC.
- **post_history Logic Core:** add the same counter and the same print as in CC. Its closing sentence lists the lines a message written as {{user}} plans without ("…with no Fate, Bonds, Ledger or Layers line."); add the JB labels there and keep the sentence grammatical.

## Wiring in Marinara

- **Option:** add `{"id":"opt_<12 random [A-Za-z0-9_-]>","label":"🔓 Jailbreak (needs Adult Context)","value":"JAILBREAK"}` to the `logic_options` choice block. Its `options` field is a JSON string; keep that format. Leave it out of `defaultChoices`.
  - Extend that block's `question` text by one short sentence about the new option.
  - Update the preset description if it lists features.
- **Inline lines:** in both Logic Core sections, inline the counter and the lines under the conditions `logic_options contains "JAILBREAK"` and `adult_mode != "NONE"`, mirroring CC's rendered text exactly. Follow the memory note's conventions, and its pitfall: a bare `{{#if name}}` is TRUE in Marinara.
- **compare.py** (`$S/mar/compare.py`):
  - Add `CHOICE_TO_CC[('logic_options','JAILBREAK')] = ['<first 8 chars of the new CC identifier>']`.
  - Make the matrix exercise JAILBREAK with every adult_mode, both in the full product and in the samples.
  - Run `python3 compare.py --full` and get `0 unique section diffs`. Run `verify.py` and get `0 mismatches`.

## Budget (hard limits)

- CC everything ON ≤ 7,000 (the checker).
- TC everything ON ≤ 7,000; also measure TC with every module on and the GLM patch, the largest gate patch.
- Marinara fully kitted-out ≤ 7,000 for every model patch with `state_mode` AGENTS and NONE (the `after` line from verify.py).

## Checker change

In `tools/aria_budget.py`:
- Set `BUDGET` to 7000.
- Add a per-file budget: any preset whose filename contains `Chibi Edition` gets 3000; every other preset keeps `BUDGET`. Error messages name the budget that applies.
- Leave `DEFAULT_PRESETS` unchanged for now.

## Guide and README

Aria's voice; facts exact; every figure re-measured with the checker.
- **New entry** for 🔓 Jailbreak in the list of band members, next to 🔞 Adult Context and 😈 Freaky Override. Cover:
  - what it does;
  - that it needs Adult Context, ships OFF and works only with a Logic Core;
  - its sources: Realistic Frankenstein's BOLT and Micro CoTs and their Jean-Claude Van Damme editions, plus the Realism and Freaky modes;
  - one plain sentence saying the parts of those jailbreaks that work by telling the model it has no rules, or by asking it to drop its protectiveness, stayed out.
- **Tables:** a TC switch-table row for `aria-jailbreak`, and wiring-table rows for `ariaJb` and `ariaJbLines`.
- **Token budget section:** the cap is now 7,000. Update every 6,000 mention and the measured figures.
- **Test notes:** mark beta 8's GLM, MiMo Flash and DeepSeek fixes as confirmed live (see COMMON.md, "Latest live results"). Add a short live-test item for the JB.
