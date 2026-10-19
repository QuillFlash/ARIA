export const meta = {
  name: 'aria-jb-7k',
  description: 'ARIA 1.0: add the 🔓 Jailbreak toggle (CC, TC, Marinara), raise the cap to 7,000, update the docs',
  phases: [
    { title: 'Draft', detail: 'Sonnet distills the JB plan lines from Realistic Frankenstein', model: 'sonnet' },
    { title: 'Judge', detail: 'Opus checks the boundary, house rules and size, and fixes', model: 'opus' },
    { title: 'Integrate', detail: 'Sonnet wires the JB into CC, TC, regex and the checker', model: 'sonnet' },
    { title: 'Marinara', detail: 'Sonnet ports the JB into the Marinara preset', model: 'sonnet' },
    { title: 'Review', detail: 'Opus reviews and fixes the whole diff', model: 'opus' },
    { title: 'Docs', detail: 'Sonnet updates the guide and README, Opus checks them' },
    { title: 'Checks', detail: 'Haiku runs the checker and the render checks', model: 'haiku' },
  ],
}

const S = '/tmp/claude-1000/-home-theaestheticfur-Fejleszt-s-SillyTavern-ARIA/df35259a-9218-4ff7-923f-01988f563265/scratchpad'
const REPO = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA'
const CC = `${REPO}/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json`
const READ = `Read ${S}/spec/COMMON.md and ${S}/spec/JB.md in full before anything else; they are binding. In those files, $S means ${S}.`
const MEM = `Also read ~/.claude/projects/-home-theaestheticfur-Fejleszt-s-SillyTavern-ARIA/memory/marinara-agent-gating-port.md.`
const STR = { type: 'string' }
const STRS = { type: 'array', items: { type: 'string' } }
const RUN = { type: 'object', properties: { ok: { type: 'boolean' }, output: STR }, required: ['ok', 'output'] }

phase('Draft')
const draft = await agent(`${READ}

Task: draft the 🔓 Jailbreak plan lines (JB.md, sections "Decisions" to "Form").
1. Load the Realistic Frankenstein source file named in JB.md with python3 (json) and print every prompt JB.md lists, in full. Read them closely, the Jean-Claude Van Damme editions included.
2. Print ARIA's 🔞 Adult Context (prompt identifier "nsfw"), 😈 Freaky Override (identifier starting 4537b57d) and The Logic Core (identifier starting 15b770cf) from "${CC}", so the JB adds to them instead of repeating them.
3. Write 2 or 4 plan lines carrying only the mature-theme parts listed under "What to distill", in ARIA's do-this style, inside the hard boundary. Also write the entry's {{// … }} comment (user-facing; factual and short) and the TC switch comment.
4. Measure: tokens = len('\\n'.join(lines)) / 4, at most 130.
5. Write ${S}/jb/draft.json: {"labels": [...], "lines": [...], "tokens": n, "cc_comment": "...", "tc_switch_comment": "...", "sources": {"<label>": "which RF prompts and sentences it distills"}, "left_out": "what you deliberately left out and why"}.
Do not edit any repository file. Return the labels, the lines and the token count.`,
  { label: 'draft-jb', phase: 'Draft', model: 'sonnet', schema: { type: 'object', properties: { labels: STRS, lines: STRS, tokens: { type: 'number' } }, required: ['labels', 'lines', 'tokens'] } })

phase('Judge')
const jb = await agent(`${READ}

You are the quality judge and fixer for the 🔓 Jailbreak plan lines a drafter wrote to ${S}/jb/draft.json (drafter's return: ${JSON.stringify(draft)}). Read the draft, the Realistic Frankenstein sources JB.md names, and ARIA's 🔞 Adult Context (CC prompt "nsfw") and The Logic Core (15b770cf…) in "${CC}".
Check every point and fix what fails:
1. Hard boundary (JB.md): nothing from the four excluded techniques in any rewording; no never-refuse or comply-with-everything orders; no claim about the model's deployment, rules or legal status; sexual content stated as between adults.
2. Scope: only mature-theme parts; no anti-slop checks (contrast, chop, register, quant hardening, leash); nothing that repeats Adult Context's own sentences or its Mode line.
3. House rules: do-this, mechanically checkable wording; no quoted examples; no list of exactly three anywhere (count the items of every comma/or/and list inside each line); 2 or 4 lines; labels new and outside JB.md's forbidden list.
4. Usefulness: each line makes the model plan something concrete about this beat, as fragments joined by semicolons like ARIA's other plan lines, and it reads well where The Logic Core prints it (after the Ledger line, before "- Fresh:").
5. Size: at most 130 tokens (characters / 4 of the lines joined by newlines).
6. Comments: factual, short, no promises the text can't keep.
Write the approved version to ${S}/jb/final.json with the draft's keys plus "judge_notes". Do not edit repository files. Return the final labels, lines, token count and a one-paragraph verdict.`,
  { label: 'judge-jb', phase: 'Judge', model: 'opus', schema: { type: 'object', properties: { labels: STRS, lines: STRS, tokens: { type: 'number' }, verdict: STR }, required: ['labels', 'lines', 'tokens', 'verdict'] } })
log(jb ? `JB lines: ${jb.labels.join(', ')} (${jb.tokens} tokens)` : 'JB judge returned nothing')

phase('Integrate')
const integ = await agent(`${READ}

Task: implement JB.md's "Wiring in CC", "Wiring in TC" and "Checker change" in ${REPO}, using the lines, labels and comments in ${S}/jb/final.json exactly (comments may be lightly edited to fit the entry style).
COMMON.md's JSON editing rules are strict: write your edit script to ${S}/jb/integrate.py and run it; every replacement asserts its occurrence count; the new CC prompt object goes in as raw JSON text formatted like its neighbours (check the file's indentation and separators); the prompt_order row likewise. The regex label alternation sits inside a JSON string in both regex locations: escape correctly and assert counts.
Then verify with your own python, importing simulate_cc and simulate_tc from ${REPO}/tools/aria_budget.py:
- python3 tools/aria_budget.py ends with OK for both files;
- CC, each Logic Core in turn, Logic Core Tags on and off: with 🔞 Adult Context on (also with Freaky on) plus the JB on, the JB lines print after the Ledger line and before "- Fresh:", and the "N dashed lines" number equals the lines starting "- " before "- go"; with Adult and Freaky off, or the JB off, no JB line and the count still matches; on an Impersonate turn (impersonate=True) no JB line;
- the two CC Logic Cores are identical after their comments;
- TC: the same checks with simulate_tc (aria-logic-core on; aria-adult, aria-jailbreak and aria-thinking-tags each on and off);
- measure CC everything ON (checker), TC everything ON (checker) and TC with every non-patch switch on plus aria-patch-glm.
Do not touch the Marinara file, the docs or git. Return what you changed, the new CC identifier and the measured figures.`,
  { label: 'integrate-cc-tc', phase: 'Integrate', model: 'sonnet', schema: { type: 'object', properties: { ok: { type: 'boolean' }, new_identifier: STR, cc_everything_on: { type: 'number' }, tc_everything_on: { type: 'number' }, tc_glm_all_on: { type: 'number' }, problems: STRS, summary: STR }, required: ['ok', 'new_identifier', 'summary'] } })

const chk1 = await agent(`Run these commands and report their output faithfully. Do not change any file.
cd "${REPO}" && python3 tools/aria_budget.py 2>&1 | grep -v "^ \\+[0-9]\\+  "
cd "${REPO}" && git status --short && git diff --stat
Return whether the checker ended with "OK: budget, wiring and cache checks all pass." for both presets, plus the printed totals and the diff stat.`,
  { label: 'checker-1', phase: 'Checks', model: 'haiku', schema: RUN })

phase('Marinara')
const mar = await agent(`${READ}
${MEM}

Task: implement JB.md's "Wiring in Marinara" in "${REPO}/Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json". CC (already updated; the new JB prompt identifier is ${integ && integ.new_identifier ? integ.new_identifier : 'the one on the prompt named 🔓 Jailbreak (needs Adult Context)'}) is the source of truth for the rendered text.
- Study how the existing Logic Core sections inline 🧷 Character Hold (core_modules contains "HOLD") and the patch lines, and how logicCoreLines is computed additively; add the JB the same way in both Logic Core sections, under logic_options containing JAILBREAK and adult_mode not NONE.
- Add the logic_options option, the question sentence and a description note; set the preset's updatedAt and the export's exportedAt to 2026-10-16T12:00:00.000Z.
- Keep the exact round-trip format (json.dumps(d, ensure_ascii=False, indent='\\t'), no trailing newline); write your script to ${S}/jb/marinara.py.
- Update ${S}/mar/compare.py (CHOICE_TO_CC and the matrix, per JB.md), and in ${S}/mar/verify.py add JAILBREAK to the fully kitted-out config's logic_options so its token figures include the JB. From ${S}/mar run python3 compare.py --full (must report 0 unique section diffs) and python3 verify.py (0 mismatches; its "after" line gives the fully kitted-out tokens for every patch with state N and A, and all must be at most 7000; ignore its "before" line, which is an old backup).
Do not touch CC, TC, docs or git. Return the compare and verify results and the largest Marinara figure.`,
  { label: 'marinara-port', phase: 'Marinara', model: 'sonnet', schema: { type: 'object', properties: { ok: { type: 'boolean' }, compare: STR, verify: STR, max_tokens: { type: 'number' }, summary: STR }, required: ['ok', 'compare', 'verify', 'summary'] } })

const chk2 = await agent(`Run these commands and report their output faithfully. Do not change any file.
cd "${S}/mar" && python3 compare.py --full 2>&1 | tail -20
cd "${S}/mar" && python3 verify.py 2>&1 | tail -6
Return the summary lines.`,
  { label: 'render-checks-1', phase: 'Checks', model: 'haiku', schema: RUN })

phase('Review')
const review = await agent(`${READ}
${MEM}

You are the reviewer and fixer for the JB work in ${REPO}. Read git diff (CC, TC, Marinara, the TC regex file, tools/aria_budget.py) and ${S}/jb/final.json. Reported so far: integrate = ${JSON.stringify(integ)}; checker = ${JSON.stringify(chk1)}; marinara = ${JSON.stringify(mar)}; render checks = ${JSON.stringify(chk2)}.
Verify, with your own scripts where possible:
1. Wiring: the JB entry (key set and order like Character Hold's; right after Freaky in prompts[] and in prompt_order[1], enabled false); its {{#if .ariaModeLine}} condition; the Main Prompt blanks in CC and TC; the Impersonation Turn blank; both CC Logic Cores identical after their comments; counter and print positions; the TC switch, block (after the adult and freaky blocks), post_history counter, print and closing sentence; the labels in both regex locations, with both regexes still compiling in python; the Marinara option and both Logic Core sections.
2. Behaviour: render CC and TC across Adult, Freaky, JB, Tags, Logic Core and Impersonate combinations; the JB lines appear exactly when they should and the dashed-line counts match.
3. Budgets: CC and TC everything ON at most 7000; TC with every module and GLM at most 7000; every Marinara path at most 7000 (verify.py).
4. Cache: system-block entries render identically across turns (the checker covers it; also read the JB entry).
5. Minimal edits: git diff --stat shows only the expected lines; nothing untouched got reformatted.
6. The boundary and the house rules hold in the final text.
Fix every problem directly in the files (you are the fixer), re-run the checker, compare.py --full and verify.py, and return what you found, what you fixed and the final check results.`,
  { label: 'review-fix', phase: 'Review', model: 'opus', schema: { type: 'object', properties: { found: STRS, fixed: STRS, remaining: STRS, checks: STR }, required: ['found', 'fixed', 'remaining', 'checks'] } })

phase('Docs')
const docs = await agent(`${READ}

Task: JB.md's "Guide and README" section, in ${REPO}/docs/ARIA_Beginners_Guide.md and ${REPO}/README.md. First read the relevant parts of both (the band-member list with 🔞 Adult Context and 😈 Freaky Override, the TC switch table, the wiring table, the token budget section, the beta 8 notes, the live test plan and the known risks) and the final JB entry in the CC file, so you describe it exactly. Re-measure every figure with python3 tools/aria_budget.py, and the TC GLM path the way JB.md says.
Write in Aria's cheerful first person, matching the surrounding style; Lewis gets no gendered pronouns; keep edits targeted. The cap is 7,000 wherever 6,000 appeared. Mark beta 8's fixes confirmed live per COMMON.md. Do not edit any preset JSON or git. Return the sections you changed.`,
  { label: 'docs', phase: 'Docs', model: 'sonnet', schema: { type: 'object', properties: { changed: STRS, summary: STR }, required: ['changed', 'summary'] } })

const docsReview = await agent(`${READ}

You are the docs judge and fixer. Check the uncommitted changes to ${REPO}/docs/ARIA_Beginners_Guide.md and ${REPO}/README.md (git diff) against the actual files: every name, switch, variable, label, default and figure must match what the presets and python3 tools/aria_budget.py show; the JB description matches the final JB text, and its boundary sentence is plain and accurate; Aria's voice; no gendered pronouns for Lewis; no email; no 6,000 cap left. Fix problems directly and return what you fixed.`,
  { label: 'docs-review', phase: 'Docs', model: 'opus', schema: { type: 'object', properties: { fixed: STRS, ok: { type: 'boolean' } }, required: ['fixed', 'ok'] } })

phase('Checks')
const final = await agent(`Run these commands and report their output faithfully. Do not change any file.
cd "${REPO}" && python3 tools/aria_budget.py 2>&1 | grep -v "^ \\+[0-9]\\+  "
cd "${S}/mar" && python3 compare.py --full 2>&1 | tail -3 && python3 verify.py 2>&1 | sed -n '1p;3p;5p'
cd "${REPO}" && git status --short && git diff --stat
Return the outputs.`,
  { label: 'final-checks', phase: 'Checks', model: 'haiku', schema: RUN })

return { jb, integrate: integ, marinara: mar, review, docs, docsReview, final }
