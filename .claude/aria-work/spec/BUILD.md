# Chibi build, plus four older ARIA fixes (decided with the user on 2026-10-16)

`$W` is `/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work` and `$REPO` is the repository root above it. COMMON.md, JB.md and CHIBI.md still apply.

## Decisions

- **Every Chibi path except one stays at or under 3,000.** Chibi CC and TC are measured by the checker; Chibi Marinara by the N (no Agents) figures in verify.py.
- **The exception:** Chibi Marinara with the Agents state backend may go over 3,000, because the user chose that. Its Agents text is still compressed Douyin-style. The `<agent_context_protocol>` block in the Main section and the Agents note in both Logic Core sections come to at most 90 tokens together.
- **Fixes:** the user asked for four older bugs to be fixed in ARIA 1.0, with each fix carried into Chibi where it applies.

## Fix 1: Gemini 3.8 leak

`gemini38Patch` is never blanked. After the Gemini 3.8 Flash patch has run once, switching it off leaves its text printing through Gemini All-In-One for another turn, and the system block changes.
- Append `{{setvar::gemini38Patch::}}` to the end of the CC Main Prompt's first-line blanking run, after `{{setvar::ariaJbLines::}}`. Do the same in Chibi CC's Main Prompt.
- TC has no Gemini patch, so it needs nothing.
- **Regression check:** in `tools/aria_budget.py`, also run the stale-state cache test for every patch on its own over the shared base set, not only for everything ON. A variable a patch leaves unblanked then fails the checker.
- If the new check finds other unblanked variables, report them. Fix those only by adding blanks.

## Fix 2: TC checker blind spot

`analyse_tc`'s `patch_cost` ranks patches with every other switch off. That picks MiMo Flash (5,938), while the real TC maximum is GLM with the Logic Core on (about 6,101).
- Rank the patches with every non-patch switch on, the way `analyse_cc` does, so "everything ON" uses the true largest patch.

## Fix 3: plan-cleanup regex

Four scripts still expect the old sentence "When this turn asks for … Ledger lines." after "Nothing above go enters the reply.", in both CC's `extensions.regex_scripts` and the TC regex file:
- `ARIA - Fold an echoed Logic Core template into a Thoughts box (display only)`
- `ARIA - Hide an echoed Logic Core closing line (display only)`
- `ARIA - Keep an echoed Logic Core template out of the prompt (all depths, cache-safe)`
- `ARIA Impersonate - strip an echoed Logic Core template`

So an echoed TC plan leaves two lines behind: "For a message written as {{user}}, … line." and "Every response starts with …".

What to change:
- Make that optional group accept both the old sentence and the current one, which starts "For a message written as" and ends " line.". Do this in all eight scripts.
- The CC and TC copies of each script stay identical.
- Use raw-text replacement on the JSON-escaped string and assert the occurrence counts.

Test on real renders, with `{{user}}` rendered as a name, tags on and off:
- ARIA TC's Logic Core;
- Chibi TC's Logic Core, from `$W/chibi/final/G3.json` `tc.post_history_logic_core`;
- old-style echoes, which must still match.

## Fix 4: stale cost comments

Re-measure every token cost quoted in TC switch comments and in CC entry comments, and refresh the stale ones. For example, `aria-logic-core` says "about 325" and measures about 406; `aria-npc-voice` says "About 360" and measures 349.
- Measure the way the guide's TC switch table does: flip one switch from the shipped state.
- Change comments only.

## Chibi build

**Inputs:**
- the judged finals `$W/chibi/final/G1.json` to `G6.json` and `JB.json`;
- the ARIA files as they stand after the fixes above.

Each judge's `judge_notes` lists the build details for its group: which TC span each tc key replaces, and which Marinara sections need care. Read all six.

**Files**, saved in the repository root:
- `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json`
- `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json`
- `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition — Agent Gating.json`

### CC

- Copy ARIA CC's raw text to the Chibi CC name. Replace each prompt's content by raw-text replacement (COMMON.md rule 7), keyed by identifier, from the finals' `prompts`.
- The JB entry's content is JB.json's comment, then `{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::<the two lines joined by a real newline>}}{{/if}}`. Never use a literal backslash-n; an earlier build had that bug.
- The Main Prompt gets the `gemini38Patch` blank, as in Fix 1.
- In `prompt_order[1]`, set 🎲 Fate & Chekhov Ledger (`acc2177a…`) and ⏰ Time & Place (`5dcccd11…`) to enabled false. Everything else ships as in ARIA CC.
- The 🌳 README entry gets G1's Chibi README. The regex scripts stay as ARIA CC's, after Fix 3.
- **Targets:**
  - the checker prints OK;
  - everything ON ≤ 3,000, aiming for 2,950;
  - shipped default between 1,350 and 1,650.
- If a target is missed, apply the judges' cut menus from `judge_notes`, using only items marked non-core and in the stated order, and record every cut.

### TC

- Copy ARIA TC's raw text to the Chibi TC name. Replace each segment with the finals' `tc` texts:
  - G1: `main_prompt`, `readme_comment`, `custom_instructions_comment`
  - G2: `post_history_gate`, `anti_slop_block`
  - G3: `post_history_logic_core`
  - G4: `scene_engine` and the `if_aria-*` blocks
  - G5: the three blocks and their switch comments
  - G6: the module blocks and switch comments
  - the JB block and its switch comment, from JB.json
- Rewrite every other switch comment for Chibi: short and accurate, with Chibi costs measured the guide's way.
- `sysprompt.name` and `context.name` follow ARIA's naming with "Chibi Edition" added.
- Switch defaults are ARIA TC's, except that `aria-logic-core` ships on if the lean start would otherwise fall below 1,350.
- **Targets:**
  - the checker prints OK;
  - everything ON ≤ 3,000;
  - lean start between 1,350 and 1,650.

### Checker

Add both Chibi files to `DEFAULT_PRESETS`, after ARIA's two. `budget_for` already gives them 3,000.

### Marinara

- Copy ARIA's Marinara JSON. Set:
  - a fresh preset `id` in the same style as the existing one, with the matching `presetId` on every child that carries one;
  - a name and description for Chibi;
  - `createdAt`, `updatedAt` and `exportedAt` to 2026-10-16T12:00:00.000Z;
  - `defaultChoices` without FATE and TIME.
- Replace every section's content with the Chibi text, converted to Marinara conventions (read the memory note). The judges' `judge_notes` list the delicate parts:
  - Main keeps its Agents block, compressed;
  - Reduce Reasoning and the Impersonation section;
  - the Adult Mode line inlined in both Logic Cores;
  - the Scent and POV gate lines;
  - the dropped `<freaky_override>` and `<POV>` wrappers;
  - the Fate, Bonds and Time sections without their wrapper lines;
  - the patch, Flash and Hold lines inlined in the Logic Cores and the gate;
  - the JB inlined under JAILBREAK with adult_mode not NONE.
- Keep the exact round-trip format: `json.dumps(d, ensure_ascii=False, indent='\t')`, no trailing newline.
- **Verify:**
  - `python3 $W/mar/compare.py --full --cc-file "<Chibi CC>" --mar "<Chibi Marinara>"` must end with "0 unique section diffs (JB exercised)";
  - `python3 $W/mar/verify.py --mar "<Chibi Marinara>"` must report 0 mismatches, and its N figures must be ≤ 3,000. Report the A figures.

## Docs

Write in Aria's voice; figures re-measured.

**Guide** (`docs/ARIA_Beginners_Guide.md`): a new Chibi Edition section covering:
- what it is: the three files and the shared TC regex file;
- how to import each file;
- its sizes, measured;
- how it differs from the full edition:
  - every module compressed;
  - Fate and Time ship OFF;
  - a lighter Fate (no appointments, Ambitions, World news or Quiet turns) and a lighter Bonds;
  - ledger ages written as n/8, n/6 and n/12;
  - the Codex written as details of the gate's rules, so keep both ON;
  - the JB included and OFF;
  - Chibi Marinara's Agents path running over 3,000.

Also update the guide for the four fixes:
- the checker description;
- the TC "everything ON" row and figures;
- any switch-table costs that changed.

**README.md:**
- Mention the Chibi files only outside the body that is mirrored in CC's README entry and TC's README comment.
- If no such place exists, leave README.md alone and say so.
