import fs from 'fs';
const p = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
let n = 0;
for (const [label, list] of Object.entries(p)) {
    for (const s of list) {
        const m = s.findRegex.match(/^\/(.*)\/([a-z]*)$/s);
        new RegExp(m[1], m[2]);
        n++;
    }
    console.log(label, list.length, 'scripts compile in node', process.version);
}
console.log('total compiled in JS:', n);
