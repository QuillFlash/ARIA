import fs from 'fs';
const [ccPath] = process.argv.slice(2);
const scripts = JSON.parse(fs.readFileSync(ccPath, 'utf8')).extensions.regex_scripts;
const toRe = s => { const m = s.match(/^\/([\s\S]*)\/([a-z]*)$/); return new RegExp(m[1], m[2]); };
const apply = (s, t) => t.replace(toRe(s.findRegex), (...a) => { const g = a.slice(1, -2); return (s.replaceString || '').replace(/\$(\d+)/g, (_, n) => g[Number(n) - 1] ?? ''); });
const pipe = (t, pl, mode) => { for (const s of scripts) { if (s.disabled || !s.placement.includes(pl)) continue;
  const ok = (mode === 'display' && s.markdownOnly) || (mode === 'prompt' && s.promptOnly) || (mode === 'save' && !s.markdownOnly && !s.promptOnly); if (ok) t = apply(s, t); } return t; };
const reply = 'Mira laughs.\n\n';
const aria = '<details><summary>🎲</summary>q: 2 | hp: 1 | thread: find the key, age 3 | deferred: storm x1, age 2 | world: war, REGIONAL, age 4 | bullets: the locket [hot], weight 2, age 5 | ambitions: none | residue: none | last: MINOR TRUE, the kettle boils over loudly</details>\n<details><summary>💚</summary>Mira↔Lewis +6/3/0</details>';
const chibi = aria.replace('age 3 |', 'age 3/8 |').replace('age 2 |', 'age 2/6 |').replace('age 5 |', 'age 5/12 |');
const da = pipe(reply + aria, 2, 'display'), dc = pipe(reply + chibi, 2, 'display');
const norm = t => t.replace(/3\/8/g, '3').replace(/2\/6/g, '2').replace(/5\/12/g, '5');
console.log('display same structure:', norm(dc) === da);
if (norm(dc) !== da) { console.log(da.slice(0, 1500)); console.log('-----'); console.log(dc.slice(0, 1500)); }
const ia = pipe(reply + aria, 1, 'save').trim(), ic = pipe(reply + chibi, 1, 'save').trim();
console.log('impersonate strip:', JSON.stringify(ia), JSON.stringify(ic));
