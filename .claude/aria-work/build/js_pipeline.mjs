// Runs the ARIA regex scripts the way SillyTavern does, in real JavaScript, over the texts in a payload file.
// usage: node js_pipeline.mjs payload.json  ->  {"<id>": {"display": ..., "prompt": ..., "impersonate": ...}}
import fs from 'fs';

const { scripts, cases } = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

function subJs(script, text) {
    const m = script.findRegex.match(/^\/(.*)\/([a-z]*)$/s);
    const rx = new RegExp(m[1], m[2]);
    const repl = script.replaceString || '';
    return text.replace(rx, (...args) => {
        const ngroups = args.length - 3; // match, p1..pn, offset, string
        return repl.replaceAll(/\$(\d+)/g, (_, n) => {
            n = Number(n);
            return n <= ngroups ? (args[n] ?? '') : '';
        });
    });
}

function pipeline(text, placement, mode) {
    for (const s of scripts) {
        if (s.disabled || !s.placement.includes(placement)) continue;
        const applies = (mode === 'display' && s.markdownOnly) || (mode === 'prompt' && s.promptOnly) ||
            (mode === 'save' && !s.markdownOnly && !s.promptOnly);
        if (applies) text = subJs(s, text);
    }
    return text;
}

const out = {};
for (const c of cases) {
    out[c.id] = {
        display: pipeline(c.text, 2, 'display'),
        prompt: pipeline(c.text, 2, 'prompt'),
        impersonate: pipeline(c.text, 1, 'save'),
    };
}
process.stdout.write(JSON.stringify(out));
