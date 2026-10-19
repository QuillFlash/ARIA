// Render a Marinara preset's sections with Marinara's own macro engine.
// usage: node mrender.mjs <preset.json> <configs.json> [--force]
// configs.json: [{adult_mode, pov_style, core_modules:[..], world_engine:[..], model_patch, logic_core, logic_options:[..], state_mode}, ...]
// Prints a JSON array: one {sectionName: renderedText} map per config, in sectionOrder, for the sections the assembler would include.
// --force also renders the choice-gated content sections that ship disabled (Freaky, Anthro, Claude, Gemini, MiMo Pro).
import { readFileSync } from 'node:fs';
import { resolveMacros } from '../vendor/macro-engine.ts';

const [presetPath, configsPath, ...flags] = process.argv.slice(2);
const force = flags.includes('--force');
const exp = JSON.parse(readFileSync(presetPath, 'utf8'));
const data = exp.data;
const sections = new Map(data.sections.map((s) => [s.id, s]));
const groups = new Map(data.groups.map((g) => [g.id, g]));
const order = JSON.parse(data.preset.sectionOrder);
const blocks = data.choiceBlocks;
const USER_CONTROLLED = /Custom Instructions|Custom Post-History|Impersonation Turn|\(Agent\)/;

const out = [];
for (const cfg of JSON.parse(readFileSync(configsPath, 'utf8'))) {
  const variables = {};
  for (const cb of blocks) {
    const sel = cfg[cb.variableName];
    const multi = cb.multiSelect === 'true' || cb.multiSelect === true;
    if (sel === undefined) throw new Error(`config lacks ${cb.variableName}`);
    variables[cb.variableName] = multi ? (sel.length ? sel.join(cb.separator ?? ', ') : '') : sel;
  }
  const ctx = { char: 'Char', user: 'User', characters: ['Char'], variables, localVariables: {} };
  const rendered = {};
  for (const id of order) {
    const s = sections.get(id);
    if (!s || s.isMarker === 'true') continue;
    const on = s.enabled === 'true' || (force && !USER_CONTROLLED.test(s.name));
    if (!on) continue;
    if (s.groupId && groups.get(s.groupId)?.enabled !== 'true') continue;
    rendered[s.name] = resolveMacros(s.content, ctx);
  }
  out.push(rendered);
}
process.stdout.write(JSON.stringify(out));
