// Apply ARIA's regex scripts (as SillyTavern would, in order, by placement) to sample replies and report the results.
import { readFileSync } from 'node:fs';
const [ccPath] = process.argv.slice(2);
const scripts = JSON.parse(readFileSync(ccPath, 'utf8')).extensions.regex_scripts;
const toRe = (s) => { const m = s.match(/^\/([\s\S]*)\/([a-z]*)$/); return new RegExp(m[1], m[2]); };
function run(text, { placement, prompt }) {
  let out = text;
  for (const s of scripts) {
    if (s.disabled || !s.placement.includes(placement)) continue;
    if (prompt ? s.markdownOnly : s.promptOnly) continue;
    out = out.replace(toRe(s.findRegex), s.replaceString.replace(/\{\{match\}\}/g, '$&'));
  }
  return out;
}
const plan = '- OOC: none\n- Scene: bench\n- Knows: she saw it\n- Voice: dry\n- Move: she leaves\n- Fresh: gull\n- Check: ok\n- go';
const echo = '<thought> opens the reply, then 7 dashed lines, then go.\nI am the game master running this immersive simulation, not a helpful AI assistant: creative risk is welcome and perfection is unnecessary.\n'
  + plan + '\n</thought> closes on the line after go. The reply starts on the line after that: header if <header_instructions>; prose. Nothing above go enters the reply.\nEvery response starts with <thought>.';
const cases = {
  'tagged <thought> plan, then story': `<thought>\n${plan}\n</thought>\nShe stands up and walks off.`,
  'echoed template with <thought>': `${echo}\nShe stands up and walks off.`,
  'unclosed <thought> plan (Impersonate)': `<thought>\n${plan}\nI wave at her.`,
  'untagged plan (Impersonate)': `${plan}\nI wave at her.`,
  'plain <thinking> plan (regression)': `<thinking>\n${plan}\n</thinking>\nShe stands up and walks off.`,
};
for (const [name, text] of Object.entries(cases)) {
  const imp = name.includes('Impersonate');
  const display = imp ? run(text, { placement: 1, prompt: false }) : run(text, { placement: 2, prompt: false });
  const prompt = imp ? null : run(text, { placement: 2, prompt: true });
  const folded = /<details/.test(display);
  console.log(`--- ${name}`);
  console.log(`  ${imp ? 'impersonate result' : 'display'}: ${folded ? '[folded into <details>] ' : ''}${JSON.stringify(display.replace(/<details[\s\S]*<\/details>/, '<details…>').slice(0, 160))}`);
  if (prompt !== null) console.log(`  prompt: ${JSON.stringify(prompt.slice(0, 160))}`);
}
