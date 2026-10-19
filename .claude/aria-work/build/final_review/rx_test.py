"""Fix 3 check, independent of the earlier test scripts: echoed Logic Core templates from live renders, run in node."""
import json, random, re, subprocess, sys, itertools
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
W = R + "/.claude/aria-work"
sys.path.insert(0, R + '/tools')
import aria_budget as ab
F = {
 'ariaCC': R + "/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json",
 'ariaTC': R + "/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",
 'chibiCC': R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json",
 'chibiTC': R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json",
 'oldTC': W + "/build/tc_before_ece78b2.json",
}
P = {k: json.load(open(v)) for k, v in F.items()}
RX = json.load(open(R + "/regex/ARIA 1.0 Regex Scripts (Text Completions).json"))
OLDRX = json.load(open(W + "/build/orig/TCregex.json"))
sets = {'new_tcfile': RX, 'new_cc': P['ariaCC']['extensions']['regex_scripts'], 'new_chibicc': P['chibiCC']['extensions']['regex_scripts'], 'old': OLDRX}
NAMES = ['Lewis', "D'Arcy", 'Ana María', '🦊 Fox', 'Sir Reginald Bartholomew the Third of Somewhere Far']

def tc_lc(key, name, tags, full):
    pre = P[key]
    sh = dict(ab.SWITCH.findall(pre['sysprompt']['content']))
    ov = dict(sh) | {'aria-logic-core': 'on', 'aria-thinking-tags': tags}
    if full:
        ov |= {s: 'on' for s in sh if not s.startswith('aria-patch')} | {'aria-thinking-tags': tags, 'aria-patch-deepseek': 'on', 'aria-adult': 'on', 'aria-jailbreak': 'on'}
    r, _ = ab.simulate_tc(pre, ov, 1)
    post = r['Post-History']
    lc = post.split('<final_gate>')[0].rstrip('\n')
    return lc.replace('User', name)

def cc_lc(key, name, tags, full):
    pre = P[key]
    prompts = {p['identifier']: p for p in pre['prompts']}
    order = pre['prompt_order'][1]['order']
    shipped = {r['identifier'] for r in order if r['enabled']}
    nm = {pid: prompts[pid].get('name', '') for pid in prompts}
    lc = [pid for pid in prompts if nm[pid].startswith('🧠 The Logic Core') and 'twin' not in nm[pid]][0]
    tagid = [pid for pid in prompts if nm[pid].startswith('🏷️')][0]
    en = set(shipped) | {lc}
    if full:
        en |= {r['identifier'] for r in order if not nm[r['identifier']].startswith(('🩹', '🌳', '🌿')) and 'twin' not in nm[r['identifier']]}
    en = (en | {tagid}) if tags == 'on' else (en - {tagid})
    r, _ = ab.simulate_cc(pre, en, 1)
    return r[lc].replace('User', name)

REPLY = 'Mira sets the kettle down and looks at {n} for a long moment. "You came back," she says, and pulls out the second chair.'
PLAN = '<thinking>\n- OOC: none\n- Scene: kitchen; kettle; {n} at the door.\n- Knows: Mira saw {n} arrive.\n- Voice: Mira wary, warm underneath.\n- Move: Mira offers a chair.\n- Fresh: chipped blue mug.\n- Check: plain.\n- go\n</thinking>'

def split_template(lc):
    """For a tags-on Logic Core: the template part (through '- go\\n</thinking>') and the closing part."""
    i = lc.index('</thinking> closes')
    return lc[:i], lc[i:]

cases = []
def add(cid, text, reply, kind):
    cases.append({'id': cid, 'text': text, 'reply': reply, 'kind': kind})

for src in ('ariaTC', 'chibiTC', 'oldTC', 'ariaCC', 'chibiCC'):
    for name, tags, full in itertools.product(NAMES, ('on', 'off'), (False, True)):
        lc = (tc_lc if 'TC' in src else cc_lc)(src, name, tags, full)
        reply = REPLY.format(n=name)
        plan = PLAN.format(n=name)
        base = f'{src}|{name}|{tags}|{"full" if full else "lean"}'
        if tags == 'on':
            tmpl, closing = split_template(lc)
            add(base + '|echo+reply', lc + '\n\n' + reply, reply, 'echo')
            add(base + '|echo+plan+reply', lc + '\n' + plan + '\n' + reply, reply, 'echo')
            # a real plan whose closing tag carries the template's closing lines, then the reply
            add(base + '|plan+closing+reply', plan[:-len('</thinking>')] + closing + '\n\n' + reply, reply, 'echo')
            add(base + '|closing-only+reply', closing[len('</thinking> '):] + '\n\n' + reply, reply, 'closing_only')
            add(base + '|echo-no-reply', lc, '', 'echo')
        else:
            add(base + '|echo+reply', lc + '\n\n' + reply, reply, 'echo_off')
            add(base + '|plan+reply', plan + '\n' + reply, reply, 'echo')
        add(base + '|plain', reply, reply, 'plain')
        add(base + '|mentions', reply + ' She says: For a message written as a letter, keep one line.', reply + ' She says: For a message written as a letter, keep one line.', 'plain')

json.dump({'sets': sets, 'cases': cases}, open(W + '/build/final_review/rx_payload.json', 'w'), ensure_ascii=False)
subprocess.run(['node', W + '/build/final_review/rx_run.mjs', W + '/build/final_review/rx_payload.json', W + '/build/final_review/rx_out.json'], check=True)
out = json.load(open(W + '/build/final_review/rx_out.json'))

LEFT = ['For a message written as', 'Every response starts with', 'closes on the line after go', 'Nothing above go', 'When this turn asks for', 'opens the reply, then', '- go', '</thinking>', '<thinking>']
def outside_details(t):
    return re.sub(r'<details[\s\S]*?</details>', '', t)
def clean(t, reply):
    leftovers = [w for w in LEFT if w in t]
    return (not leftovers) and t.strip() == reply.strip(), leftovers

from collections import Counter
stats = Counter(); fails = []
for sid in sets:
    for c in cases:
        o = out[sid][c['id']]
        src = c['id'].split('|')[0]
        for mode in ('display', 'prompt', 'imp'):
            t = o[mode]
            if mode == 'display':
                t = outside_details(t)
            ok, left = clean(t, c['reply'])
            if c['kind'] == 'plain':
                ok = o[mode] == c['text'] if mode != 'imp' else o[mode].strip() == c['text'].strip()
            key = (sid, src, c['kind'], mode, ok)
            stats[key] += 1
            if not ok and sid != 'old' and not (c['kind'] == 'closing_only' and mode == 'imp') and c['kind'] != 'echo_off':
                fails.append((sid, c['id'], mode, left, t[:200]))
for k in sorted(stats):
    print(k, stats[k])
print('UNEXPECTED FAILS (new scripts):', len(fails))
for f in fails[:20]:
    print(f)
