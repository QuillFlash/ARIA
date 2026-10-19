# ARIA 1.0 Chibi Edition (decided with the user)

## What it is

A lighter edition of ARIA 1.0 in three files, saved in the repository root next to the ARIA 1.0 files:
- `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json`
- `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json`
- `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition — Agent Gating.json` (Marinara)

Every ARIA module and toggle stays, each one compressed. That includes the new 🔓 Jailbreak toggle (see JB.md), which ships OFF and needs 🔞 Adult Context.

## Size

- **Fully kitted-out ≤ 3,000 tokens:** everything ON, with the largest patch, the JB, Adult, Freaky, Logic Core Tags, Reduce Reasoning, Flash Gate, Hold, Fate, Bonds and Time & Place. Aim for 2,850 or less.
- **Shipped default ≈ 1,500 tokens** (1,350 to 1,650). To get there, Chibi CC ships 🎲 Fate & Chekhov Ledger and ⏰ Time & Place OFF, unlike ARIA CC. Everything else ships as in ARIA CC.
- **Chibi TC** uses ARIA TC's switch defaults, but `aria-logic-core` ships on if the lean start would otherwise fall below 1,350.

## Style

Use the concise wording of Realistic Frankenstein's Douyin Edition. Source: `/home/theaestheticfur/SillyTavern Presets/Realistic Frankenstein 2.2.1.3 — Limitless Realism/Douyin/Realistic Frankenstein 2.2.1.3 Douyin Edition.json`. Study its Main Prompt, World & NPC Concepts, Prose Concepts, the four killswitches, Douyin CoT, pico CoT and Hardening.
- Short declarative do-this sentences, one rule per clause.
- Inside plan and gate lines, fragments joined by semicolons.
- No hedges, no rationale, no restating, plain nouns.

ARIA's house rules still apply (COMMON.md):
- no quoted examples, except the 🩹 Claude 5 patch's repairs, which may stay in shortened form;
- no lists of three;
- mechanical, checkable wording.

Comments (`{{// … }}`) cost nothing. Keep them short, accurate and adapted to Chibi (mention the Chibi sizes where useful).

## Wiring is unchanged; compress only the wording

- **Keep exactly as ARIA 1.0 has them:** identifiers, names, roles, positions, triggers, variables, every `setvar`/`getvar`/`addvar`/`#if` structure, plan labels, line counts and gate line labels. The regex scripts then keep working as they are.
- **The Logic Core** keeps its 7 base lines (OOC, Scene, Knows, Voice, Move, Fresh, Check) and its whole macro logic, plus the JB counter and print from JB.md. Both Logic Cores are identical after their comments.
- **Dropping or merging a wired line** (a line some variable supplies, or a gate line) is allowed only when every counter and reader is updated to match and the judge approves. Compressing is the strong preference.
- **Keep every mechanic and every tester fix,** down to the checkable core of each rule, for example:
  - numbers and thresholds;
  - exceptions such as nervous cards keeping their stammers and a refusal staying a plain no;
  - Fate's dice tiers, ladders and ledger fields;
  - Bonds' gates, Sparks, Grudge and conversions;
  - DeepSeek's Tally;
  - each patch's specific lines.
- **What goes:** restatements, rationale, and overlaps between modules. A rule stated in two system-block modules keeps one copy; the gate's short echo of a Codex rule stays.

## Token targets

Rendered with everything ON, comments excluded. Measure with `python3 $S/spec/tok.py <your json>` (add `--state '{"ariaModeLine":"x"}'` to render blocks that test a variable). These targets add up to about 2,770 fully kitted-out and about 1,460 as shipped, so every row matters: if you go over in one row, save the same amount elsewhere in your group.

| Group | Entry | Target |
|---|---|---|
| G1 core | ⚡ ARIA Main Prompt (`main`) | ≤ 260 |
| | 📖 Story Context, 🏷️ Logic Core Tags (setvars only), 🍃 Custom Instructions | keep their wiring; trim only comments |
| | 🪞 Impersonation Turn | ≤ 100 |
| | Reduce Reasoning | ≤ 40 |
| | 🌳 README (disabled, 0 tokens) | a short Chibi README in Aria's voice: what Chibi is, its sizes, how it differs, that the full guide covers both editions |
| | 🌿 Sampling Advice (disabled) | keep, shortened |
| G2 style | 🖋️ Anti-Slop Codex | ≤ 330 |
| | its `ariaEchoGate` and `ariaChopGate` lines | ≤ 30 each |
| | 🚪 Last-Mile Gate's own lines | ≤ 290 |
| G3 plan | 🧠 The Logic Core's own text, excluding lines supplied by modules (ARIA's is 337 rendered without Tags) | ≤ 220 |
| G4 voice & modes | 🎬 Voice & Scene Engine | ≤ 110 |
| | 🎭 NPC Voice & Emotions | ≤ 120 |
| | 🐺 Anthro Vocals | ≤ 50 |
| | 👃 Scent Occasions, plus its gate line | ≤ 40, ≤ 25 |
| | 👀 Hybrid POV, plus its gate line | ≤ 25, ≤ 20 |
| | 🔞 Adult Context, plus its Mode line | ≤ 60, ≤ 12 |
| | 😈 Freaky Override, plus its Mode line | ≤ 30, ≤ 8 |
| G5 world | ⏰ Time & Place | ≤ 45 |
| | 🎲 Fate & Chekhov Ledger, plus its plan, ledger, gate and dice lines together | ≤ 300, ≤ 110 |
| | 🥰 Bonds Lite, plus its plan line | ≤ 120, ≤ 30 |
| G6 patches & gates | each 🩹 patch's own text | ≤ 50 (Claude 5 ≤ 80 with its repairs) |
| | GLM's five `ariaPatchGate` lines | ≤ 120 together |
| | every other patch's `ariaPatchGate` lines | ≤ 90 together |
| | `ariaPatchTally` | ≤ 55 |
| | `ariaPatchJoins` | ≤ 25 |
| | 🔦 Flash Gate lines, plus `ariaVoiceExtra` | ≤ 90, ≤ 12 |
| | 🧷 Character Hold's two lines | ≤ 55 together |
| (later) | the Chibi JB's plan lines | ≤ 55 |

These are hard ceilings, not goals: shorter is fine wherever the rule's checkable core survives.

G2 and G3 also produce the TC `post_history` version of their part (TC's Logic Core and `<final_gate>`). Compress it the same way and keep TC's own additions: the "A message written as {{user}} skips it." notes, the closing sentence about messages written as {{user}}, and the `{{#if .aria-logic-core}}` wrapper.

## Draft format

Each group writes `$S/chibi/drafts/G<n>.json`. The judge writes the approved version to `$S/chibi/final/G<n>.json`.

```json
{
  "prompts": {"<CC identifier>": {"name": "<unchanged name>", "content": "<full new content>"}},
  "tc": {"post_history_logic_core": "…", "post_history_gate": "…", "<other TC-only text>": "…"},
  "tokens": {"<identifier or line>": 123},
  "notes": "what was merged or dropped, and why"
}
```

Leave `tc` out when your group has no TC-specific text. Source texts are in the frozen snapshot `$S/chibi/src/` (CC, TC, Marinara and the TC regex file as of commit e636d9b). Work from the snapshot, never from the live repository files, because another workflow is editing those.

## Build (a later stage)

- **Copy:** copy ARIA's files (after the JB has landed) to the Chibi names and replace the contents by raw-text replacement.
- **CC:**
  - the 🌳 README entry becomes the Chibi README;
  - the regex scripts stay as they are;
  - `prompt_order[1]` turns Fate and Time & Place off.
- **TC:** `sysprompt.name` and `context.name` say Chibi Edition; the README comment becomes a short Chibi one.
- **Marinara:**
  - the preset name and description say Chibi Edition;
  - a fresh `id` (and the matching `presetId` on every child);
  - `createdAt` and `updatedAt` both 2026-10-16T12:00:00.000Z;
  - `defaultChoices` without FATE and TIME.
- **Checker:** add the Chibi CC and TC files to `DEFAULT_PRESETS`; they get the 3,000 budget through the Chibi rule.
- **Marinara checks:** run compare.py against Chibi CC (0 diffs) and verify.py (0 mismatches), using copies adapted to the Chibi paths.
