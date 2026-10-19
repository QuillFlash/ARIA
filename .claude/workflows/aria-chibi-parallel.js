export const meta = {
  name: 'aria-chibi-parallel',
  description: 'Alongside the Chibi TC build: build Chibi Marinara (Sonnet 5.5), check Chibi CC (Haiku 5.5), review and fix Chibi CC (Opus 5.5)',
  phases: [
    { title: 'Parallel', detail: 'Marinara builder, CC checker and CC reviewer at once' },
    { title: 'Resync', detail: 'Haiku 5.5 re-runs the Marinara render check; Sonnet 5.5 resyncs if the CC review changed text' },
  ],
}

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
const SUB = `You are a subagent inside a workflow run. Do the task yourself with Bash, Read, Edit and Write. Do not use the Skill tool and do not try to start a workflow. Never read from or write to /tmp/claude-1000/...; your work folder is ${W} (scratch scripts in ${W}/build/). Never commit, stage or push. Another agent is building Chibi TC ("${CHIBI_TC}") and editing tools/aria_budget.py right now: never touch either, and don't run tools/aria_budget.py without a file argument.`
const READ = `${SUB}\nRead ${W}/spec/COMMON.md, ${W}/spec/JB.md, ${W}/spec/CHIBI.md and ${W}/spec/BUILD.md in full before anything else; they are binding ($S and $W mean ${W}; $REPO means ${REPO}).`
const MEM = `Also read ~/.claude/projects/-home-theaestheticfur-Fejleszt-s-SillyTavern-ARIA/memory/marinara-agent-gating-port.md.`
const STR = { type: 'string' }
const STRS = { type: 'array', items: { type: 'string' } }
const NUM = { type: 'number' }
const RUN = { type: 'object', properties: { ok: { type: 'boolean' }, output: STR }, required: ['ok', 'output'] }

phase('Parallel')
const [mar, chk, rev] = await parallel([
  () => run('sonnet', `${READ}
${MEM}

Task: build Chibi Marinara per BUILD.md "Chibi build" → "Marinara", at "${CHIBI_MAR}", from ARIA's Marinara file and the Chibi texts. Chibi CC ("${CHIBI_CC}", already built: shipped 1,503, everything ON 2,978) is the source of truth for every rendered line; the finals' judge_notes in ${W}/chibi/final/ list the delicate sections. An Opus reviewer is checking Chibi CC at the same time and may fix small things in it, so re-run the compare at the very end against the CC as it then stands.
- Compress the Agents-only text (the <agent_context_protocol> block in Main and the note in both Logic Cores) Douyin-style to at most 90 tokens together, keeping its rules: the engine's <context> is an earlier snapshot; apply its facts silently, never quote or reformat it; current actions change anything in it and newer witnessed events override it; append no agent, tracker, debug or report block, while ARIA's own 🎲 and 💚 ledgers still close the reply.
- Keep the round-trip format exact; keep your script in ${W}/build/ so the text can be re-synced later.
- Verify from ${W}/mar: python3 compare.py --full --cc-file "${CHIBI_CC}" --mar "${CHIBI_MAR}" must end with "0 unique section diffs (JB exercised)"; python3 verify.py --mar "${CHIBI_MAR}" must show 0 mismatches and every N figure at most 3000 (report the A figures too). Then run compare.py --full and verify.py with no arguments, to confirm ARIA's own Marinara still passes.
Don't touch CC, TC, the checker or the docs. Return the compare and verify lines and the largest N and A figures.`,
    { label: 'build-marinara', phase: 'Parallel', schema: { type: 'object', properties: { ok: { type: 'boolean' }, compare: STR, verify: STR, max_n: NUM, max_a: NUM, summary: STR }, required: ['ok', 'compare', 'verify', 'summary'] } }),
  () => run('haiku', `${SUB}
Run these and report their output faithfully. Change nothing.
cd "${REPO}" && python3 tools/aria_budget.py "${CHIBI_CC}" 2>&1
cd "${REPO}" && python3 -c "import json; d=json.load(open(\\"${CHIBI_CC}\\",encoding='utf-8')); jb=[p for p in d['prompts'] if p['name'].startswith('🔓')][0]; print('JB literal backslash-n:', chr(92)+'n' in jb['content']); print('Fate/Time enabled:', [(o['identifier'][:8], o['enabled']) for o in d['prompt_order'][1]['order'] if o['identifier'][:8] in ('acc2177a','5dcccd11')]); m=[p for p in d['prompts'] if p['identifier']=='main'][0]['content']; print('gemini38Patch blank:', '{{setvar::gemini38Patch::}}' in m)"
cd "${REPO}" && git status --short
Return whether the checker ended with "OK: budget, wiring and cache checks all pass.", its totals and per-entry lines, and the three sanity results.`,
    { label: 'check-cc', phase: 'Parallel', schema: RUN }),
  () => run('opus', `${READ}

You are the reviewer and fixer for Chibi CC ("${CHIBI_CC}") only. Verify with your own scripts:
1. Wiring: identifiers, names, roles, positions, triggers and every setvar/getvar/addvar/#if skeleton equal ARIA CC's apart from the documented JB additions and the gemini38Patch blank (use ${W}/spec/skeleton.py logic against ARIA's current CC); both Logic Cores identical after their comments; Fate and Time off in prompt_order[1]; the JB entry with a real newline; regex scripts byte-identical to ARIA CC's.
2. Content: every prompt equals its final in ${W}/chibi/final/ (G1–G6, JB.json) or a recorded cut.
3. Budget: everything ON at most 3,000; shipped default between 1,350 and 1,650 (python3 tools/aria_budget.py "${CHIBI_CC}").
4. Behaviour: a simulate_cc render matrix (each Logic Core, Tags on and off, adult modes, JB, Fate, Bonds, every patch, normal and Impersonate): plan counts match, no leftover macros, no literal backslash-n, no doubled spaces, the system block identical across turns (stale-state test).
5. JSON hygiene: the file formats like ARIA CC (indent 4, no trailing newline) and round-trips.
6. The JB boundary and the house rules hold in the Chibi text.
Fix problems directly in Chibi CC only, by raw-text replacement. Write every change you make (prompt identifier, old text, new text) to ${W}/build/review_cc_changes.json so Chibi TC and Marinara can be re-synced. Return what you found, fixed and left.`,
    { label: 'review-cc', phase: 'Parallel', schema: { type: 'object', properties: { found: STRS, fixed: STRS, remaining: STRS, cc_changed: { type: 'boolean' }, checks: STR }, required: ['found', 'fixed', 'remaining', 'cc_changed', 'checks'] } }),
])

phase('Resync')
const chk2 = await run('haiku', `${SUB}
Run these and report their output faithfully. Change nothing.
cd "${W}/mar" && python3 compare.py --full --cc-file "${CHIBI_CC}" --mar "${CHIBI_MAR}" 2>&1 | tail -15 && python3 verify.py --mar "${CHIBI_MAR}" 2>&1 | tail -3
Return all the output, and ok=true only if compare reports "0 unique section diffs (JB exercised)" and verify reports 0 mismatches.`,
  { label: 'marinara-recheck', phase: 'Resync', schema: RUN })

let resync = null
if (!chk2 || !chk2.ok) {
  resync = await run('sonnet', `${READ}
${MEM}

Chibi Marinara ("${CHIBI_MAR}") no longer renders equal to Chibi CC, most likely because the CC reviewer changed CC text (its change list: ${W}/build/review_cc_changes.json; its report: ${JSON.stringify(rev)}). Render check output: ${JSON.stringify(chk2)}.
Apply the same text changes to the matching Marinara sections (inline lines included), keep the round-trip format exact, and re-run from ${W}/mar: compare.py --full --cc-file "${CHIBI_CC}" --mar "${CHIBI_MAR}" (0 unique section diffs (JB exercised)) and verify.py --mar "${CHIBI_MAR}" (0 mismatches, N figures at most 3000). Don't touch CC, TC or the checker. Return the final compare and verify lines.`,
    { label: 'marinara-resync', phase: 'Resync', schema: { type: 'object', properties: { ok: { type: 'boolean' }, compare: STR, verify: STR }, required: ['ok', 'compare', 'verify'] } })
}

return { marinara: mar, checkCC: chk, reviewCC: rev, recheck: chk2, resync }
