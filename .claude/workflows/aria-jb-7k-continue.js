export const meta = {
  name: 'aria-jb-7k-continue',
  description: 'Continue aria-jb-7k: finish and verify the interrupted JB wiring in CC and TC, port it to Marinara, review, docs',
  phases: [
    { title: 'Integrate', detail: 'Sonnet 5.5 finishes and verifies the interrupted CC/TC wiring', model: 'claude-sonnet-5-5' },
    { title: 'Marinara', detail: 'Sonnet 5.5 ports the JB into the Marinara preset', model: 'claude-sonnet-5-5' },
    { title: 'Review', detail: 'Opus 5.5 reviews and fixes the whole diff', model: 'claude-opus-5-5' },
    { title: 'Docs', detail: 'Sonnet 5.5 updates the guide and README, Opus 5.5 checks them' },
    { title: 'Checks', detail: 'Haiku 5.5 runs the checker and the render checks', model: 'claude-haiku-5-5' },
  ],
}

// Model choices from the user's CLAUDE.md: Sonnet drafts and codes, Opus checks and fixes, Haiku runs commands.
// If a model is missing (gateway or outage), fall back to the family alias, then inherit the session model.
const CHAINS = {
  sonnet: ['claude-sonnet-5-5', 'sonnet'],
  opus: ['claude-opus-5-5', 'opus'],
  haiku: ['claude-haiku-5-5', 'haiku', 'claude-haiku-4-5'],
}
async function run(tier, prompt, opts) {
  for (const model of CHAINS[tier]) {
    const r = await agent(prompt, { ...opts, model })
    if (r !== null && r !== undefined) return r
    log(`${opts.label}: no result on ${model}, trying the next model`)
  }
  return await agent(prompt, opts)
}

const W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
const REPO = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA'
const SUB = `You are a subagent inside a workflow run. Do the task yourself with Bash, Read, Edit and Write. Do not use the Skill tool and do not try to start a workflow: the saved skills named aria-jb-7k and aria-chibi-drafts describe the very run you are part of. Never read from or write to /tmp/claude-1000/...; your work folder is ${W}. An earlier attempt at this work was cut off by a credit error, so check the current state of every file before you change it.`
const READ = `${SUB}\nRead ${W}/spec/COMMON.md and ${W}/spec/JB.md in full before anything else; they are binding. In those files $S means ${W}.`
const MEM = `Also read ~/.claude/projects/-home-theaestheticfur-Fejleszt-s-SillyTavern-ARIA/memory/marinara-agent-gating-port.md.`
const STR = { type: 'string' }
const STRS = { type: 'array', items: { type: 'string' } }
const RUN = { type: 'object', properties: { ok: { type: 'boolean' }, output: STR }, required: ['ok', 'output'] }

phase('Integrate')
const integ = await run('sonnet', `${READ}

Context: an earlier integrator was cut off by a credit error after it edited CC, TC, the TC regex file and tools/aria_budget.py in ${REPO}; git diff shows its work. The approved JB lines are in ${W}/jb/final.json (labels Role and Frank, 2 lines). Finish and verify that work against JB.md's "Wiring in CC", "Wiring in TC" and "Checker change".
1. The TC regex file was re-dumped with tab indentation instead of its four-space indentation, which COMMON.md forbids. Restore it with: git -C "${REPO}" checkout -- "regex/ARIA 1.0 Regex Scripts (Text Completions).json". Then re-apply only the label change (Role and Frank after Joins in the alternation of the script "ARIA Impersonate - strip an untagged plan") by raw-text replacement, asserting exactly one occurrence. Afterwards git diff --stat must show a single changed line for that file, and the regex must still compile in python (strip the JS slashes and flags first).
2. Check every wiring item of JB.md in the current CC and TC, one by one: the CC prompt object's key set, key order and values (a known gap: its injection_order is 0 but Character Hold's is 100, and JB.md says to copy Hold's values), its position in prompts[] and prompt_order[1], its comment and its {{#if .ariaModeLine}} condition, the Main Prompt and Impersonation Turn blanks, both Logic Cores' counter and print, the CC regex label, the TC switch and its comment, the TC blanks, the TC block's position and condition, the TC post_history counter, print and closing sentence, and the checker's BUDGET and Chibi rule. Fix every gap with raw-text edits (COMMON.md rule 7); change nothing else.
3. Verify with your own python, importing simulate_cc and simulate_tc from ${REPO}/tools/aria_budget.py:
- python3 tools/aria_budget.py ends with OK for both files;
- CC, each Logic Core in turn, Logic Core Tags on and off: with 🔞 Adult Context on (also with Freaky on) plus the JB on, the Role and Frank lines print after the Ledger line and before "- Fresh:", and the "N dashed lines" number equals the lines starting "- " before "- go"; with Adult and Freaky off, or the JB off, no JB line and the count still matches; on an Impersonate turn (impersonate=True) no JB line;
- the two CC Logic Cores are identical after their comments;
- TC: the same checks with simulate_tc (aria-logic-core on; aria-adult, aria-jailbreak and aria-thinking-tags each on and off);
- measure CC everything ON (checker), TC everything ON (checker) and TC with every non-patch switch on plus aria-patch-glm.
Do not touch the Marinara file or the docs, and never commit or stage. Return the checklist with pass or fail per item, what you changed, the JB identifier and the measured figures.`,
  { label: 'integrate-finish', phase: 'Integrate', schema: { type: 'object', properties: { ok: { type: 'boolean' }, new_identifier: STR, checklist: STRS, changed: STRS, cc_everything_on: { type: 'number' }, tc_everything_on: { type: 'number' }, tc_glm_all_on: { type: 'number' }, summary: STR }, required: ['ok', 'new_identifier', 'checklist', 'summary'] } })

const chk1 = await run('haiku', `${SUB}
Run these commands and report their output faithfully. Do not change any file.
cd "${REPO}" && python3 tools/aria_budget.py 2>&1 | grep -v "^ \\+[0-9]\\+  "
cd "${REPO}" && git status --short && git diff --stat
Return whether the checker ended with "OK: budget, wiring and cache checks all pass." for both presets, plus the printed totals and the diff stat.`,
  { label: 'checker-1', phase: 'Checks', schema: RUN })

phase('Marinara')
const mar = await run('sonnet', `${READ}
${MEM}

Task: JB.md's "Wiring in Marinara" for "${REPO}/Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json". CC (already updated; the JB prompt identifier is ${integ && integ.new_identifier ? integ.new_identifier : '05f6e90d-b30b-48d5-b2bf-26a6e45faffa'}) is the source of truth for the rendered text.
- Study how both Logic Core sections inline 🧷 Character Hold (core_modules contains "HOLD") and the patch lines, and how logicCoreLines is computed additively; add the JB the same way in both Logic Core sections, under logic_options containing JAILBREAK and adult_mode not NONE.
- Add the logic_options option, one question sentence and a description note; set the preset's updatedAt and the export's exportedAt to 2026-10-16T12:00:00.000Z.
- Keep the exact round-trip format (json.dumps(d, ensure_ascii=False, indent='\\t'), no trailing newline); keep your script at ${W}/jb/marinara.py.
- The render tools in ${W}/mar already handle the JB: compare.py maps the CC prompt whose name starts with 🔓 to the JAILBREAK option and adds JB configs to its matrix once both presets carry it (until then it prints a WARNING), and verify.py puts JAILBREAK into its fully kitted-out figures. From ${W}/mar run python3 compare.py --full (it must end with "0 unique section diffs (JB exercised)") and python3 verify.py (0 mismatches; every figure on its "tokens" line, state N and A, at most 7000).
Do not touch CC, TC or the docs, and never commit or stage. Return the compare and verify results and the largest Marinara figure.`,
  { label: 'marinara-port', phase: 'Marinara', schema: { type: 'object', properties: { ok: { type: 'boolean' }, compare: STR, verify: STR, max_tokens: { type: 'number' }, summary: STR }, required: ['ok', 'compare', 'verify', 'summary'] } })

const chk2 = await run('haiku', `${SUB}
Run these commands and report their output faithfully. Do not change any file.
cd "${W}/mar" && python3 compare.py --full 2>&1 | tail -20
cd "${W}/mar" && python3 verify.py 2>&1 | tail -6
Return the summary lines.`,
  { label: 'render-checks-1', phase: 'Checks', schema: RUN })

phase('Review')
const review = await run('opus', `${READ}
${MEM}

You are the reviewer and fixer for the JB work in ${REPO}. Read git diff (CC, TC, Marinara, the TC regex file, tools/aria_budget.py) and ${W}/jb/final.json. Reported so far: integrate = ${JSON.stringify(integ)}; checker = ${JSON.stringify(chk1)}; marinara = ${JSON.stringify(mar)}; render checks = ${JSON.stringify(chk2)}.
Verify, with your own scripts where possible:
1. Wiring: the JB entry (key set, order and values like Character Hold's; right after Freaky in prompts[] and prompt_order[1], enabled false); its {{#if .ariaModeLine}} condition; the Main Prompt blanks in CC and TC; the Impersonation Turn blank; both CC Logic Cores identical after their comments; counter and print positions; the TC switch, block (after the adult and freaky blocks), post_history counter, print and closing sentence; the labels in both regex locations, with both regexes compiling in python; the Marinara option and both Logic Core sections.
2. Behaviour: render CC and TC across Adult, Freaky, JB, Tags, Logic Core and Impersonate combinations; the JB lines appear exactly when they should and the dashed-line counts match.
3. Budgets: CC and TC everything ON at most 7000; TC with every module and GLM at most 7000; every Marinara path at most 7000 (verify.py).
4. Cache: system-block entries render identically across turns (the checker covers it; also read the JB entry).
5. Minimal edits: git diff --stat shows only the expected lines; nothing untouched got reformatted (the TC regex file must show a one-line diff with four-space indentation intact).
6. The hard boundary and the house rules hold in the final text.
Fix every problem directly in the files (you are the fixer), re-run the checker, compare.py --full and verify.py from ${W}/mar, and return what you found, what you fixed and the final check results. Never commit or stage.`,
  { label: 'review-fix', phase: 'Review', schema: { type: 'object', properties: { found: STRS, fixed: STRS, remaining: STRS, checks: STR }, required: ['found', 'fixed', 'remaining', 'checks'] } })

phase('Docs')
const docs = await run('sonnet', `${READ}

Task: JB.md's "Guide and README" section, in ${REPO}/docs/ARIA_Beginners_Guide.md and ${REPO}/README.md. First read the relevant parts of both (the band-member list with 🔞 Adult Context and 😈 Freaky Override, the TC switch table, the wiring table, the token budget section, the beta 8 notes, the live test plan and the known risks) and the final JB entry in the CC file, so you describe it exactly. Re-measure every figure with python3 tools/aria_budget.py, and the TC GLM path the way JB.md says.
Write in Aria's cheerful first person, matching the surrounding style; Lewis gets no gendered pronouns; keep edits targeted. The cap is 7,000 wherever 6,000 appeared. Mark beta 8's fixes confirmed live per COMMON.md. Do not edit any preset JSON, and never commit or stage. Return the sections you changed.`,
  { label: 'docs', phase: 'Docs', schema: { type: 'object', properties: { changed: STRS, summary: STR }, required: ['changed', 'summary'] } })

const docsReview = await run('opus', `${READ}

You are the docs judge and fixer. Check the uncommitted changes to ${REPO}/docs/ARIA_Beginners_Guide.md and ${REPO}/README.md (git diff) against the actual files: every name, switch, variable, label, default and figure must match what the presets and python3 tools/aria_budget.py show; the JB description matches the final JB text, and its boundary sentence is plain and accurate; Aria's voice; no gendered pronouns for Lewis; no email address; no 6,000 cap left. Fix problems directly and return what you fixed. Never commit or stage.`,
  { label: 'docs-review', phase: 'Docs', schema: { type: 'object', properties: { fixed: STRS, ok: { type: 'boolean' } }, required: ['fixed', 'ok'] } })

phase('Checks')
const final = await run('haiku', `${SUB}
Run these commands and report their output faithfully. Do not change any file.
cd "${REPO}" && python3 tools/aria_budget.py 2>&1 | grep -v "^ \\+[0-9]\\+  "
cd "${W}/mar" && python3 compare.py --full 2>&1 | tail -3 && python3 verify.py 2>&1 | tail -4
cd "${REPO}" && git status --short && git diff --stat
Return the outputs.`,
  { label: 'final-checks', phase: 'Checks', schema: RUN })

return { integrate: integ, checker: chk1, marinara: mar, renderChecks: chk2, review, docs, docsReview, final }
