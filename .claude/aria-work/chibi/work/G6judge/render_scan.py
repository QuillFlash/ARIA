"""Render every G6 shape (CC with the G1-G3 finals + JB, and TC) and scan the rendered text for doubled spaces,
space before punctuation, a separator at a line end, blank lines inside the plan or gate, and leftover macros."""
import json, re, sys
sys.path.insert(0, '.')
import g6check as g
import aria_budget as ab
G6PATH = sys.argv[1]
g.G6 = json.load(open(G6PATH, encoding='utf-8'))
cc = g.cc_build(True)
order = cc['prompt_order'][1]['order']; P = {p['identifier']: p for p in cc['prompts']}
names = {k: P[k]['name'] for k in P}
allids = {r['identifier'] for r in order} - {'enhanceDefinitions'}
patches = sorted(k for k in allids if names[k].startswith('🩹'))
fg, hold, tags = '2e3e7f63-8463-51ff-ba8f-e5b05162c193', 'dc8b1acb-9a7e-5a43-b9aa-38e7b70662a3', '303f26f5-bc2f-5dde-a9e9-aaaacd3eff4b'
fate, bonds, nsfw = 'acc2177a-34e4-4941-93a2-b80bc18b8c91', '5506d699-fb00-49ce-a631-73b3f0036eae', 'nsfw'
G6IDS = set(g.G6['prompts'])
base = {k for k in allids if not names[k].startswith(('🌳', '🌿', '🩹'))} - {g.LC_IDS[1], fg, hold, tags, fate, bonds}
PATS = [(r'  +', 'double space'), (r' [,.;:]', 'space before punctuation'), (r'[;,]\s*$', 'separator at line end'),
        (r'\{\{|\}\}', 'leftover macro'), (r'\.\.(?!\.)', 'double period'), (r';;|,,', 'doubled separator')]
issues = {}
def scan(label, text, blank_ok):
    for ln in text.split('\n'):
        for pat, what in PATS:
            if re.search(pat, ln):
                issues.setdefault((what, ln[:140]), label)
    if not blank_ok and '\n\n' in text.strip('\n'):
        issues.setdefault(('blank line', label), label)
n = 0
for p in patches + [None]:
    extras = [[], ['333dbbed-344d-4a6c-90c5-b0625291115a']] if p and p.startswith('ac96') else [[]]
    for extra in extras:
        for f in (0, 1):
            for h in (0, 1):
                for t in (0, 1):
                    for fb in ((0, 0), (1, 0), (0, 1), (1, 1)):
                        for imp in (False, True):
                            en = base | ({p} if p else set()) | set(extra) | ({fg} if f else set()) | ({hold} if h else set()) | ({tags} if t else set()) | ({fate} if fb[0] else set()) | ({bonds} if fb[1] else set())
                            r, st = ab.simulate_cc(cc, en, seed=1, impersonate=imp); n += 1
                            lab = f'{names.get(p)} fg={f} hold={h} tags={t} fate/bonds={fb} imp={imp}'
                            scan('LC ' + lab, r[g.LC_IDS[0]], False)
                            scan('GATE ' + lab, r['jailbreak'].split('</final_gate>')[0], False)
                            for k in G6IDS & set(r):
                                scan(names[k] + ' ' + lab, r[k].strip('\n'), True)
tc = g.tc_build(True)
sw = dict(ab.SWITCH.findall(tc['sysprompt']['content']))
for p in [s for s in sw if s.startswith('aria-patch')] + [None]:
    for f in ('on', 'off'):
        for h in ('on', 'off'):
            for t in ('on', 'off'):
                ov = {s: 'on' for s in sw if not s.startswith('aria-patch')} | {s: 'off' for s in sw if s.startswith('aria-patch')}
                ov.update({'aria-flash-gate': f, 'aria-character-hold': h, 'aria-thinking-tags': t})
                if p: ov[p] = 'on'
                r, st = ab.simulate_tc(tc, ov, seed=1); n += 1
                post = r['Post-History']; i = post.index('<final_gate>')
                lab = f'TC {p} fg={f} hold={h} tags={t}'
                scan('TC-LC ' + lab, post[:i], False); scan('TC-GATE ' + lab, post[i:].split('</final_gate>')[0], False)
print(f'{n} renders scanned; {len(issues)} distinct issues')
for (what, ln), lab in sorted(issues.items()):
    print(f'  {what}: {ln!r}\n      first seen in {lab}')
