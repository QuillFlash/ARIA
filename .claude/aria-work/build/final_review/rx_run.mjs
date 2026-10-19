// Apply SillyTavern regex scripts (JS RegExp, $n -> group or '') over cases. usage: node rx_run.mjs payload.json out.json
import fs from 'fs';
const { sets, cases } = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
function sub(s, text) {
  const m = s.findRegex.match(/^\/(.*)\/([a-z]*)$/s);
  const rx = new RegExp(m[1], m[2]);
  const repl = (s.replaceString || '').replace(/{{match}}/gi, '$0');
  return text.replace(rx, (...args) => {
    const hasGroups = typeof args[args.length - 1] === 'object';
    const n = args.length - (hasGroups ? 4 : 3);
    return repl.replaceAll(/\$(\d+)/g, (_, k) => { k = Number(k); return k <= n ? (args[k] ?? '') : ''; });
  });
}
function pipe(scripts, text, placement, mode) {
  for (const s of scripts) {
    if (s.disabled || !s.placement.includes(placement)) continue;
    const ok = (mode === 'display' && s.markdownOnly) || (mode === 'prompt' && s.promptOnly) || (mode === 'imp' && !s.markdownOnly && !s.promptOnly);
    if (ok) text = sub(s, text);
  }
  return text;
}
const out = {};
for (const [sid, scripts] of Object.entries(sets)) {
  out[sid] = {};
  for (const c of cases) out[sid][c.id] = { display: pipe(scripts, c.text, 2, 'display'), prompt: pipe(scripts, c.text, 2, 'prompt'), imp: pipe(scripts, c.text, 1, 'imp') };
}
fs.writeFileSync(process.argv[3], JSON.stringify(out));
