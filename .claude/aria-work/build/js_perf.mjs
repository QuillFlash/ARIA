// Adversarial inputs for the four changed scripts: old vs new findRegex timing in node
import fs from 'fs';
const oldS = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const newS = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const idx = [0, 1, 2, 24];
const head = '<thinking> opens the reply, then 7 dashed lines, then go.\n- OOC: a\n- Scene: b\n- go\n</thinking> closes on the line after go. The reply starts on the line after that: ';
const inputs = {
  'no closing period, 100k chars': head + 'header if x; ' + 'a'.repeat(100000),
  'sentence start repeated 5000x': head + 'Nothing above go enters the reply. ' + 'For a message written as '.repeat(5000),
  'long line without " line."': head + 'Nothing above go enters the reply. For a message written as ' + 'N'.repeat(100000),
  'many near-complete echoes': (head + 'Nothing above go enters the reply. For a message written as X, plan only X\'s move, with no Fate lin\n').repeat(800),
  'ten thousand dashes': '<thinking> opens the reply, then ' + '- go\n'.repeat(10000),
  'closes... repeated': 'closes on the line after go. The reply starts on the line after that: '.repeat(3000),
};
function rx(s) { const m = s.findRegex.match(/^\/(.*)\/([a-z]*)$/s); return new RegExp(m[1], m[2]); }
let worst = 0;
for (const [name, text] of Object.entries(inputs)) {
  const row = [];
  for (const i of idx) {
    const t = [];
    for (const list of [oldS, newS]) {
      const r = rx(list[i]);
      const t0 = performance.now();
      text.replace(r, '');
      t.push(performance.now() - t0);
    }
    row.push(`#${i} ${t[0].toFixed(1)}->${t[1].toFixed(1)}ms`);
    worst = Math.max(worst, t[1]);
  }
  console.log(name.padEnd(34), row.join('  '));
}
console.log('worst new-regex time:', worst.toFixed(1), 'ms');
