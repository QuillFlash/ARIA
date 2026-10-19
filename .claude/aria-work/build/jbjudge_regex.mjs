// Run the live 'ARIA Impersonate - strip an untagged plan' script (CC and TC copies) on a plan holding the candidate JB lines,
// the way SillyTavern does: the findRegex string is turned into a JS RegExp and replaced with ''.
import fs from 'fs';
const [ccPath, tcPath, linesJson] = process.argv.slice(2);
const cc = JSON.parse(fs.readFileSync(ccPath, 'utf8')).extensions.regex_scripts;
const tc = JSON.parse(fs.readFileSync(tcPath, 'utf8'));
const lines = JSON.parse(linesJson).map(l => l.replaceAll('{{user}}', 'Lewis'));
const toRe = s => { const m = s.match(/^\/([\s\S]*)\/([a-z]*)$/); return new RegExp(m[1], m[2]); };
for (const [name, list] of [['CC', cc], ['TC', tc]]) {
  const re = toRe(list.find(x => x.scriptName.includes('strip an untagged plan')).findRegex);
  const plan = '- OOC: none.\n- Scene: a room.\n- Knows: x.\n- Mode: realism, persona-true.\n- Voice: a.\n- Move: b.\n'
    + lines.join('\n') + '\n- Fresh: c.\n- Check: d.\n- go\nReply text follows here.';
  const out = plan.replace(re, '');
  console.log(name, JSON.stringify(out), out === 'Reply text follows here.' ? 'OK' : 'FAIL');
}
