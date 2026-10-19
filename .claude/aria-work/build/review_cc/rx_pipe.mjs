// Run every enabled regex script of a CC preset the way SillyTavern does, per mode, on each case; print the remainders.
import fs from 'fs';
const [ccPath, casesPath] = process.argv.slice(2);
const scripts = JSON.parse(fs.readFileSync(ccPath, 'utf8')).extensions.regex_scripts;
const data = JSON.parse(fs.readFileSync(casesPath, 'utf8'));
const toRe = s => { const m = s.match(/^\/([\s\S]*)\/([a-z]*)$/); return new RegExp(m[1], m[2]); };
function apply(s, text) {
  const re = toRe(s.findRegex);
  return text.replace(re, (...args) => {
    const groups = args.slice(1, -2).filter((_, i) => i < 99);
    return (s.replaceString || '').replace(/\$(\d+)/g, (_, n) => groups[Number(n) - 1] ?? '');
  });
}
function pipeline(text, placement, mode) {
  for (const s of scripts) {
    if (s.disabled || !s.placement.includes(placement)) continue;
    const ok = (mode === 'display' && s.markdownOnly) || (mode === 'prompt' && s.promptOnly) || (mode === 'save' && !s.markdownOnly && !s.promptOnly);
    if (ok) text = apply(s, text);
  }
  return text;
}
const reply = data.reply;
const res = {};
for (const [tag, cases] of Object.entries(data.cases)) {
  for (const [name, text] of Object.entries(cases)) {
    const saved = pipeline(text, 2, 'save');
    const prompt = pipeline(saved, 2, 'prompt').trim();
    const display = pipeline(saved, 2, 'display');
    const imp = pipeline(text, 1, 'save').trim();
    const dispTail = display.replace(/<details[\s\S]*<\/details>/, '').trim();
    res[`${tag}|${name}`] = {prompt_ok: prompt === reply, imp_ok: imp === reply, display_tail_ok: dispTail === reply,
      prompt: prompt === reply ? '' : prompt.slice(0, 300), imp: imp === reply ? '' : imp.slice(0, 300), disp: dispTail === reply ? '' : dispTail.slice(0, 300)};
  }
}
console.log(JSON.stringify(res, null, 1));
