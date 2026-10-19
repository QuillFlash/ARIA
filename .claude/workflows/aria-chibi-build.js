export const meta = {
  name: 'aria-chibi-build',
  description: 'Fix four older ARIA bugs, then build the Chibi Edition (CC, TC, Marinara) from the judged drafts, check, review and document both editions',
  phases: [
    { title: 'Fix', detail: 'Sonnet 5.5 fixes the Gemini 3.8 leak, the TC checker ranking, the plan-cleanup regex and stale cost comments', model: 'claude-sonnet-5-5' },
    { title: 'JB', detail: 'Sonnet 5.5 compresses the jailbreak lines for Chibi, Opus 5.5 judges them' },
    { title: 'Build', detail: 'Sonnet 5.5 assembles the Chibi CC, TC and Marinara files', model: 'claude-sonnet-5-5' },
    { title: 'Review', detail: 'Opus 5.5 reviews and fixes both editions', model: 'claude-opus-5-5' },
    { title: 'Docs', detail: 'Sonnet 5.5 documents Chibi and the fixes, Opus 5.5 checks the docs' },
    { title: 'Checks', detail: 'Haiku 5.5 runs the checker and the render checks', model: 'claude-haiku-5-5' },
  ],
}

// The user's CLAUDE.md: Sonnet drafts and codes, Opus checks and fixes, Haiku runs commands.
// If a model is missing, fall back to the family alias, then to the session model.
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
const CHIBI_CC = `${REPO}/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json`
const CHIBI_TC = `${REPO}/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json`
const CHIBI_MAR = `${REPO}/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition — Agent Gating.json`
const SUB = `You are a subagent inside a workflow run. Do the task yourself with Bash, Read, Edit and Write. Do not use the Skill tool and do not try to start a workflow: saved skills named aria-* describe runs like the one you are part of. Never read from or write to /tmp/claude-1000/...; your work folder is ${W} (keep scratch scripts in ${W}/build/). Never commit, stage or push. Check the current state of every file before you change it.`
const READ = `${SUB}\nRead ${W}/spec/COMMON.md, ${W}/spec/JB.md, ${W}/spec/CHIBI.md and ${W}/spec/BUILD.md in full before anything else; they are binding ($S and $W both mean ${W}; $REPO means ${REPO}).`
const MEM = `Also read ~/.claude/projects/-home-theaestheticfur-Fejleszt-s-SillyTavern-ARIA/memory/marinara-agent-gating-port.md.`
const STR = { type: 'string' }
const STRS = { type: 'array', items: { type: 'string' } }
const NUM = { type: 'number' }
const RUN = { type: 'object', properties: { ok: { type: 'boolean' }, output: STR }, required: ['ok', 'output'] }

phase('Fix')
const [fix, jbDraft] = await parallel([
  () => run('sonnet', `${READ}

Task: BUILD.md's Fix 1 to Fix 4, in ARIA 1.0's files in ${REPO} (CC, TC, the TC regex file, tools/aria_budget.py). Chibi files don't exist yet; the build stage carries the fixes into them.
- Fix 1: the gemini38Patch blank at the end of the CC Main Prompt's blanking run, plus the per-patch stale-state check in the checker. Confirm the new check fails on the unfixed file (test on an in-memory copy) and passes after the fix. If it finds other unblanked variables, report them and fix only by adding blanks.
- Fix 2: rank TC patches with every non-patch switch on. Report the new TC everything-ON figure and which patch it picks.
- Fix 3: the optional closing-sentence group in the four named scripts, in CC's regex_scripts and in the TC regex file, by raw-text replacement with asserted counts. Keep each CC and TC copy identical, keep four-space indentation and every other byte of the regex file, and check that both files still parse and every regex compiles in python (strip the JS slashes and flags). Test with your own python on real renders: ARIA TC's Logic Core and ${W}/chibi/final/G3.json tc.post_history_logic_core, tags on and off, {{user}} rendered as a name, as an echoed template followed by a reply. The fold, hide, keep-out and strip scripts must now remove the "For a message written as … line." sentence and the "Every response starts with" line, and old-style echoes must still match.
- Fix 4: re-measure and refresh the token costs quoted in TC switch comments and CC entry comments. Change comments only.
Finally run python3 tools/aria_budget.py (OK for both files) and, from ${W}/mar, python3 compare.py --full (0 unique section diffs (JB exercised)). Return what you changed, the test results and the new figures.`,
    { label: 'fix-aria', phase: 'Fix', schema: { type: 'object', properties: { ok: { type: 'boolean' }, changed: STRS, tests: STR, tc_everything_on: NUM, other_unblanked: STRS, summary: STR }, required: ['ok', 'changed', 'tests', 'summary'] } }),
  () => run('sonnet', `${READ}

Task: compress the 🔓 Jailbreak's two plan lines for the Chibi Edition. Source: ${W}/jb/final.json (ARIA's approved Role and Frank lines and comments).
- Keep the labels Role and Frank (the regex depends on them) and 2 lines, at most 55 tokens together (characters / 4 of the lines joined by a newline).
- Keep each line's checkable core: game master of an adult fiction, not an assistant; {{user}} and NPCs succeed or fail alike by skill and circumstance; NPCs finish what they start, nervous cards stay nervous; sex stays between adults; for a sexual, violent, cruel or dark beat, name its act, anatomy, card trait and tone and write it explicitly in those terms. If something must go, drop the least checkable part first and say what.
- JB.md's hard boundary, the house rules (do-this, no quoted examples, no list of exactly three) and the Douyin style of CHIBI.md apply.
- Also write a short Chibi CC entry comment and a TC switch comment (needs aria-adult and aria-logic-core; its measured cost).
Write ${W}/chibi/drafts/JB.json: {"labels": [...], "lines": [...], "tokens": n, "cc_comment": "...", "tc_switch_comment": "...", "dropped": "..."}. Don't edit repository files. Return the lines and the token count.`,
    { label: 'draft-jb-chibi', phase: 'JB', schema: { type: 'object', properties: { lines: STRS, tokens: NUM, dropped: STR }, required: ['lines', 'tokens'] } }),
])

const jb = await run('opus', `${READ}

You are the quality judge and fixer for the Chibi Jailbreak lines in ${W}/chibi/drafts/JB.json (drafter's return: ${JSON.stringify(jbDraft)}), compressed from ARIA's ${W}/jb/final.json.
Check and fix: JB.md's hard boundary (no writer pretext, no no-guidelines claim, no protectiveness check, no never-refuse or comply order, sex stays between adults); labels exactly Role and Frank; 2 lines; at most 55 tokens; every line's checkable core from ARIA's final present, or a justified drop; house rules (do-this, no quoted examples, no list of exactly three, counting semicolon fragments as list items the way the earlier judges did); the lines read well where The Logic Core prints them (after the Ledger line, before "- Fresh:"); the comments are factual and the costs right.
Write the approved version to ${W}/chibi/final/JB.json (same keys plus "judge_notes"). Don't edit repository files. Return the final lines, token count and a short verdict.`,
  { label: 'judge-jb-chibi', phase: 'JB', schema: { type: 'object', properties: { lines: STRS, tokens: NUM, verdict: STR }, required: ['lines', 'tokens', 'verdict'] } })

const chk1 = await run('haiku', `${SUB}
Run these and report their output faithfully. Change nothing.
cd "${REPO}" && python3 tools/aria_budget.py 2>&1 | grep -v "^ \\+[0-9]\\+  "
cd "${W}/mar" && python3 compare.py --full 2>&1 | tail -3 && python3 verify.py 2>&1 | tail -3
cd "${REPO}" && git status --short && git diff --stat
Return whether every checker run ended with "OK: budget, wiring and cache checks all pass.", the totals, the compare and verify lines and the diff stat.`,
  { label: 'checks-after-fixes', phase: 'Checks', schema: RUN })

phase('Build')
const cc = await run('sonnet', `${READ}

Task: build Chibi CC per BUILD.md "Chibi build" → "CC" and "Checker", at "${CHIBI_CC}". Inputs: ${W}/chibi/final/G1.json … G6.json and JB.json (read every judge_notes for build details) and ARIA CC as it stands now (the fixes are in). Fix results so far: ${JSON.stringify(fix)}. Chibi JB: ${JSON.stringify(jb)}.
- Copy ARIA CC's raw text, then replace contents by raw-text replacement keyed by identifier, asserting one occurrence each. Every prompt in the finals must land; every other prompt (markers, Custom Instructions wiring and the like) stays as ARIA's.
- The JB entry: JB.json's cc_comment, then the conditional setvars with the two lines joined by a real newline.
- The Main Prompt: G1's text plus the gemini38Patch blank at the end of the blanking run.
- prompt_order[1]: Fate and Time & Place off; the rest as ARIA.
- Add Chibi CC to DEFAULT_PRESETS in tools/aria_budget.py (Chibi TC comes next; add only CC now).
- Verify with python3 tools/aria_budget.py: OK; Chibi CC everything ON at most 3,000 (aim 2,950), shipped default between 1,350 and 1,650; and with simulate_cc, across Logic Core and twin, Tags on and off, Adult, Freaky and JB on and off, Fate and Bonds on and off, every patch, normal and Impersonate: "N dashed lines" equals the dashed lines before "- go", no unrendered {{…}} remains and no literal backslash-n prints. If a size target misses, apply the judges' non-core cut menus in order and record each cut.
Don't touch ARIA's preset files or the docs. Return the figures, any cuts and the checks.`,
  { label: 'build-cc', phase: 'Build', schema: { type: 'object', properties: { ok: { type: 'boolean' }, everything_on: NUM, shipped: NUM, cuts: STRS, checks: STR, summary: STR }, required: ['ok', 'summary'] } })

const tc = await run('sonnet', `${READ}

Task: build Chibi TC per BUILD.md "Chibi build" → "TC" and "Checker", at "${CHIBI_TC}". Inputs: the finals' tc texts (each judge_notes names the span every key replaces), ${W}/chibi/final/JB.json, and ARIA TC as it stands now. Chibi CC is built: ${JSON.stringify(cc)}.
- Copy ARIA TC's raw text, then replace each segment by raw-text replacement with asserted counts.
- Rewrite every switch comment the finals don't supply, for Chibi, with Chibi costs measured the guide's way (flip one switch from the shipped state).
- sysprompt.name and context.name with "Chibi Edition"; switch defaults per BUILD.md (aria-logic-core on only if the lean start would fall below 1,350).
- Model-facing text must match Chibi CC's for every shared module (compare rendered module texts; TC's own additions excepted).
- Add Chibi TC to DEFAULT_PRESETS after Chibi CC.
- Verify: python3 tools/aria_budget.py OK for all four files; Chibi TC everything ON at most 3,000; lean start between 1,350 and 1,650; and with simulate_tc across logic core, tags, adult, freaky, jailbreak, fate, bonds and each patch: the dashed-line counts match and no unrendered {{…}} remains.
Don't touch ARIA's files or the docs. Return the figures and the checks.`,
  { label: 'build-tc', phase: 'Build', schema: { type: 'object', properties: { ok: { type: 'boolean' }, everything_on: NUM, lean: NUM, checks: STR, summary: STR }, required: ['ok', 'summary'] } })

const chk2 = await run('haiku', `${SUB}
Run this and report its output faithfully. Change nothing.
cd "${REPO}" && python3 tools/aria_budget.py 2>&1 | grep -v "^ \\+[0-9]\\+  "
Return whether all four presets ended with "OK: budget, wiring and cache checks all pass." and their totals.`,
  { label: 'checks-after-cc-tc', phase: 'Checks', schema: RUN })

const mar = (typeof args !== 'undefined' && args && args.fromFile) ? { ok: true, summary: `Built and reviewed in side runs; see ${W}/build/parallel_results.json (marinara, reviewMarinara)` } : await run('sonnet', `${READ}
${MEM}

Task: build Chibi Marinara per BUILD.md "Chibi build" → "Marinara", at "${CHIBI_MAR}", from ARIA's Marinara file and the Chibi texts (Chibi CC "${CHIBI_CC}" is the source of truth for every rendered line; the finals' judge_notes list the delicate sections). Built so far: CC ${JSON.stringify(cc)}; TC ${JSON.stringify(tc)}.
- Compress the Agents-only text (the <agent_context_protocol> block in Main and the note in both Logic Cores) Douyin-style to at most 90 tokens together, keeping its rules: the engine's <context> is an earlier snapshot; apply its facts silently, never quote or reformat it; current actions change anything in it and newer witnessed events override it; append no agent, tracker, debug or report block, while ARIA's own 🎲 and 💚 ledgers still close the reply.
- Keep the round-trip format exact; keep your script in ${W}/build/.
- Verify from ${W}/mar: python3 compare.py --full --cc-file "${CHIBI_CC}" --mar "${CHIBI_MAR}" must end with "0 unique section diffs (JB exercised)"; python3 verify.py --mar "${CHIBI_MAR}" must show 0 mismatches and every N figure at most 3000 (report the A figures too). Then re-run compare.py --full and verify.py with no arguments, to confirm ARIA's own Marinara still passes.
Don't touch CC, TC or the docs. Return the compare and verify lines and the largest N and A figures.`,
  { label: 'build-marinara', phase: 'Build', schema: { type: 'object', properties: { ok: { type: 'boolean' }, compare: STR, verify: STR, max_n: NUM, max_a: NUM, summary: STR }, required: ['ok', 'compare', 'verify', 'summary'] } })

const chk3 = (typeof args !== 'undefined' && args && args.fromFile) ? { ok: true, output: `See ${W}/build/parallel_results.json (recheck, reviewMarinara.checks, checkCC, checkTC)` } : await run('haiku', `${SUB}
Run these and report their output faithfully. Change nothing.
cd "${W}/mar" && python3 compare.py --full --cc-file "${CHIBI_CC}" --mar "${CHIBI_MAR}" 2>&1 | tail -3 && python3 verify.py --mar "${CHIBI_MAR}" 2>&1 | tail -3
cd "${W}/mar" && python3 compare.py --full 2>&1 | tail -3 && python3 verify.py 2>&1 | tail -3
Return all the output lines.`,
  { label: 'render-checks', phase: 'Checks', schema: RUN })

phase('Review')
const review = await run('opus', `${READ}
${MEM}

You are the reviewer and fixer for this build. The work: four fixes in ARIA 1.0 and the new Chibi Edition files ("${CHIBI_CC}", "${CHIBI_TC}", "${CHIBI_MAR}"). Separate Opus reviews of each Chibi file already ran and fixed what they found, and Haiku checks passed on each; read their full reports in ${W}/build/parallel_results.json (keys marinara, checkCC, reviewCC, recheck, reviewTC, reviewMarinara, checkTC) (their edit logs: ${W}/build/review_cc_changes.json, review_tc_changes.json, review_mar_changes.json). Trust their per-file verdicts and only spot-check them. Spend your effort on the ARIA fixes (points 1 and 6 below) and on the cross-edition checks: the three Chibi files agree with each other after all three reviews (Chibi TC's model-facing text equals Chibi CC's, Chibi Marinara renders equal Chibi CC), and every budget in point 4 still holds. Reported so far: fixes ${JSON.stringify(fix)}; Chibi JB ${JSON.stringify(jb)}; checks ${JSON.stringify(chk1)}; CC ${JSON.stringify(cc)}; TC ${JSON.stringify(tc)}; checks ${JSON.stringify(chk2)}; Marinara ${JSON.stringify(mar)}; render checks ${JSON.stringify(chk3)}.
Verify with your own scripts:
1. The fixes: the gemini38Patch blank in both CC Main Prompts and the checker's per-patch stale test catching its absence; the TC ranking; the eight regex scripts identical between CC, Chibi CC and the TC regex file, compiling, and cleaning echoed ARIA and Chibi TC plans (tags on and off), old-style echoes too; only comments changed in Fix 4, with true figures.
2. Chibi wiring: identifiers, names, roles, positions, triggers and every setvar/getvar/addvar/#if skeleton equal to ARIA's apart from the documented JB additions and the gemini38Patch blank (use ${W}/spec/skeleton.py against ARIA's current files); both Chibi Logic Cores identical after their comments; Fate and Time off in Chibi CC's prompt_order; the JB entry with a real newline; the TC segments complete (no ARIA text left where a final replaced it, unless the finals kept it); Marinara ids, presetIds, dates and defaultChoices.
3. Content: every prompt's text equals its final (or a recorded cut), Chibi TC's model-facing text matches Chibi CC's, Chibi Marinara renders equal Chibi CC (compare.py), the Agents text keeps its rules within 90 tokens.
4. Budgets: ARIA CC and TC everything ON at most 7,000 and ARIA Marinara at most 7,000 on every path; Chibi CC and TC everything ON at most 3,000, shipped and lean starts between 1,350 and 1,650; Chibi Marinara N paths at most 3,000 (A may exceed; report it).
5. Behaviour: render matrices for Chibi CC and TC (each Logic Core, Tags, adult modes, JB, Fate, Bonds, every patch, Impersonate): plan counts match, no leftover macros, no literal backslash-n, no doubled spaces, the system block identical across turns.
6. JSON hygiene: ARIA's diffs stay minimal (git diff --stat), the Chibi files keep their source's formatting (CC and TC indent like ARIA's, Marinara round-trips exactly), the regex file keeps four-space indentation.
7. The JB boundary and the house rules hold in the Chibi text.
Fix every problem directly (you are the fixer), re-run the checker and the render checks, and return what you found, fixed and left.`,
  { label: 'review-fix', phase: 'Review', schema: { type: 'object', properties: { found: STRS, fixed: STRS, remaining: STRS, checks: STR }, required: ['found', 'fixed', 'remaining', 'checks'] } })

phase('Docs')
const docs = await run('sonnet', `${READ}

Task: BUILD.md's "Docs" section. Read the guide's structure and the parts that describe the checker, the TC budget rows and the switch-table costs, plus README.md; read the built Chibi files so you describe them exactly; re-measure every figure with python3 tools/aria_budget.py and, for Marinara, python3 ${W}/mar/verify.py (with --mar for Chibi). Review notes so far: ${JSON.stringify(review)}.
Aria's cheerful first person, matching the guide's style; Lewis gets no gendered pronouns; targeted edits; no promises the Chibi text doesn't keep (Chibi's Fate has no appointments, Ambitions, World news or Quiet turns). Don't edit preset JSON. Return the sections you changed.`,
  { label: 'docs', phase: 'Docs', schema: { type: 'object', properties: { changed: STRS, summary: STR }, required: ['changed', 'summary'] } })

const docsReview = await run('opus', `${READ}

You are the docs judge and fixer. Check the uncommitted changes to ${REPO}/docs/ARIA_Beginners_Guide.md and ${REPO}/README.md (git diff) against the actual files: every file name, switch, default, label and figure must match what the presets, python3 tools/aria_budget.py and ${W}/mar/verify.py show; the Chibi section promises nothing the Chibi text lacks; the fixes are described correctly; Aria's voice; no gendered pronouns for Lewis; no email address. Fix problems directly and return what you fixed.`,
  { label: 'docs-review', phase: 'Docs', schema: { type: 'object', properties: { fixed: STRS, ok: { type: 'boolean' } }, required: ['fixed', 'ok'] } })

phase('Checks')
const final = await run('haiku', `${SUB}
Run these and report their output faithfully. Change nothing.
cd "${REPO}" && python3 tools/aria_budget.py 2>&1 | grep -v "^ \\+[0-9]\\+  "
cd "${W}/mar" && python3 compare.py --full 2>&1 | tail -2 && python3 verify.py 2>&1 | tail -2
cd "${W}/mar" && python3 compare.py --full --cc-file "${CHIBI_CC}" --mar "${CHIBI_MAR}" 2>&1 | tail -2 && python3 verify.py --mar "${CHIBI_MAR}" 2>&1 | tail -2
cd "${REPO}" && git status --short && git diff --stat
Return all the output.`,
  { label: 'final-checks', phase: 'Checks', schema: RUN })

return { fix, jbDraft, jb, chk1, cc, tc, chk2, mar, chk3, review, docs, docsReview, final }
