import fs from 'fs';
const rx = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const inputs = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
function toRe(s) { const m = s.match(/^\/([\s\S]*)\/([a-z]*)$/); return new RegExp(m[1], m[2]); }
for (const inp of inputs) {
  let t = inp;
  for (const [f, r] of rx) t = t.replace(toRe(f), r);
  // strip styles for readability
  console.log(t.replace(/ style="[^"]*"/g, '').replace(/<\/div><div>/g, '\n'));
  console.log('-----');
}
