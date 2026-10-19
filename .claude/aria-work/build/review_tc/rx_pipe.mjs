// usage: node rx_pipe.mjs scripts.json cases.json out.json
// Runs SillyTavern-style regex pipelines: display (placement 2, not promptOnly), prompt (placement 2, not markdownOnly),
// impersonate (placement 1). $N groups, undefined -> '', {{match}} -> $0.
import fs from 'fs';
const [,, scriptsPath, casesPath, outPath] = process.argv;
const scripts = JSON.parse(fs.readFileSync(scriptsPath, 'utf8'));
const cases = JSON.parse(fs.readFileSync(casesPath, 'utf8'));
function toRe(s) { const m = s.match(/^\/([\s\S]*)\/([a-z]*)$/); return m ? new RegExp(m[1], m[2]) : new RegExp(s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'); }
function run(script, text) {
  const re = toRe(script.findRegex);
  return text.replace(re, function () {
    const args = [...arguments];
    const rs = (script.replaceString || '').replace(/{{match}}/gi, '$0');
    return rs.replaceAll(/\$(\d+)|\$<([^>]+)>/g, (_, num, name) => {
      let v = num !== undefined ? args[Number(num)] : (typeof args[args.length - 1] === 'object' ? args[args.length - 1][name] : undefined);
      if (typeof v !== 'string') return '';
      for (const t of (script.trimStrings || [])) v = v.split(t).join('');
      return v;
    });
  });
}
function pipe(kind, text) {
  for (const s of scripts) {
    if (s.disabled) continue;
    const pl = s.placement || [];
    if (kind === 'display' && (!pl.includes(2) || s.promptOnly)) continue;
    if (kind === 'prompt' && (!pl.includes(2) || s.markdownOnly)) continue;
    if (kind === 'impersonate' && (!pl.includes(1))) continue;
    text = run(s, text);
  }
  return text;
}
const out = {};
for (const [k, text] of Object.entries(cases)) out[k] = { display: pipe('display', text), prompt: pipe('prompt', text), impersonate: pipe('impersonate', text) };
fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
