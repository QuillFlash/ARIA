# ARIA work spec: common rules (read all of it before you start)

Repository: `/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA` (branch `alpha`).
- Never commit, push or stage anything. The user tests first and asks for commits separately.
- Never touch the untracked `.claude/` directory.
- Scratchpad (for your own temporary files): `/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work` (below: `$S`).

## What ARIA is

ARIA ("Aria's Realistic Intelligence Assistance") is a SillyTavern roleplay preset. Aria is its mascot: lead singer of the band AoD, an Intelligent Construct. She narrates the README and the guide in a cheerful first person. The user's persona in the repo is "Lewis" (TheAestheticFur), Aria's Manager. Never use gendered pronouns for Lewis or the user.

## Files

- **CC** `Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json`
  - `prompts[]`: identifier, name, role, content, `injection_position` (0 = relative/system block, 1 = In-Chat), `injection_depth`, `injection_trigger`.
  - `prompt_order[1].order` is the live order. `prompt_order[0]` is a short default list that only names the built-in entries.
  - `extensions.regex_scripts` holds the regex scripts.
- **TC** `Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json`
  - `sysprompt.content`, in order:
    1. a long README comment;
    2. the `{{.aria-x = on/off}}` switches, each after a `{{// … }}` comment;
    3. the Main Prompt's first line, which blanks the variables;
    4. every module inside `{{#if .aria-x}}…{{/if}}`.
  - `sysprompt.post_history`: The Logic Core inside `{{#if .aria-logic-core}}…{{/if}}`, then `<final_gate>`.
  - A `{{if .aria-flash-gate}}` without `#` is intentional; leave it.
- **Marinara** `Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json` (Marinara Engine conversion made by u/BSPiotr).
  - No variables: choice blocks, with every line inlined under choice conditions.
  - Round-trips exactly as `json.dumps(d, ensure_ascii=False, indent='\t')` with no trailing newline.
  - Read `~/.claude/projects/-home-theaestheticfur-Fejleszt-s-SillyTavern-ARIA/memory/marinara-agent-gating-port.md` before touching it.
- **Regex:** CC's `extensions.regex_scripts`, plus `regex/ARIA 1.0 Regex Scripts (Text Completions).json` (a JSON list). The script `ARIA Impersonate - strip an untagged plan` lists every plan label in one alternation (`…|Layers|Tally|Pushback|Restate|Joins`). Every new plan label goes into that alternation in both files.
- **Docs:** `docs/ARIA_Beginners_Guide.md` (Aria's voice) and `README.md`.
- **Checker:** `python3 tools/aria_budget.py` checks budget, wiring and cache safety. It must end with `OK` for every file. `simulate_cc(preset, enabled_ids, seed)` and `simulate_tc(preset, overrides, seed)` are importable from it.
- **Marinara render tools** (all in `$S/mar/`):
  - `compare.py` renders Marinara with Marinara's own macro engine and diffs it against CC rendered by `simulate_cc`. The target is `0 unique section diffs`; run `python3 compare.py --full`.
  - `verify.py` checks the plan line counts; the target is `0 mismatches`. It also prints token figures.
  - `me/mrender.mjs` and `me/macro-engine.ts` run under `node`.

## House rules for model-facing text

1. **Do-this form.** Say what to write, in mechanical wording that a model can check against its own draft (word classes, counts, positions, conditions). No vague ideals, no explanations aimed at the model.
2. **No quoted examples.** No example phrases or example sentences in model-facing text. The 🩹 Claude 5 patch's repair examples are the only exception (MiMo copies quoted examples word for word). Comments (`{{// … }}`) are stripped before sending, so they may quote.
3. **No lists of exactly three.** The rule of three is a slop pattern ARIA fights, so its own rules use one, two or four items.
4. **Keep shared lines strong.** Don't weaken the shared lines Kimi K3 and GLM 5.3 rely on (Anti-Slop Codex, Last-Mile Gate, Logic Core base lines). Model-specific fixes live in model patches.
5. **Keep CC, TC and Marinara in sync.** The model-facing text is the same in all three. In CC, The Logic Core and its system-role twin are identical after their comments.
6. **Variables:**
   - Every new `aria*` variable is blanked with `{{setvar::name::}}` in the Main Prompt's first line, in both CC and TC.
   - System-block entries (`injection_position` 0) set variables; In-Chat entries print them.
   - System-block entries must render identically on every turn, for prompt caching: no per-turn macros (`{{roll}}`, `{{random}}`, time) outside setvar bodies.
7. **Editing JSON:**
   - Edit CC and TC only by raw-text replacement. Find `json.dumps(old, ensure_ascii=False)[1:-1]` in the raw file text, assert the expected number of occurrences, and replace it with `json.dumps(new, ensure_ascii=False)[1:-1]`.
   - Never re-dump CC or TC as a whole.
   - Insert new prompt objects as raw JSON text formatted like their neighbours.
   - Marinara may be re-dumped, since it round-trips exactly; check the round trip.
8. **No personal data.** Don't ship personal test settings, and never write the user's email address anywhere.
9. **Token metric:** tokens = characters ÷ 4 of the rendered text with comments stripped. That's the checker's metric.

## Context

- **Models in play:** Claude 5 (Fable, Opus, Sonnet), Gemini 3.8 Flash and Gemini 4 Argon, GLM 5.3 and GLM 5.3 Flash, Kimi K3, Qwen, MiMo V2.6 Pro and Flash, DeepSeek V4 Pro (0813) and V4.1 Flash.
- **Testers:** u/BSPiotr (made the Marinara conversion), u/trashhaul and u/Probablynotsocool.
- **Latest live results:** Lewis confirmed beta 8 working great on GLM 5.3 Flash and MiMo V2.6 Flash. u/trashhaul confirmed it on both DeepSeeks (V4 Pro 0813 and V4.1 Flash).
- **Token caps, agreed with the user:**
  - ARIA 1.0: 7,000 on every fully kitted-out path, Marinara with the Agents state backend included (it used to be 6,000).
  - Chibi Edition: at most 3,000 fully kitted-out, about 1,500 as shipped.
- **Defaults:** ARIA ships SFW. Every new jailbreak toggle ships OFF.
