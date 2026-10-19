import json, re, subprocess, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab
ROOT = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/'
CCN = "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
TCN = "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
def load(rev, name):
    if rev == 'WORK':
        return json.load(open(ROOT + name, encoding='utf-8'))
    return json.loads(subprocess.run(['git', '-C', ROOT, 'show', f'HEAD:{name}'], capture_output=True).stdout.decode())
tok = lambda r: sum(ab.tokens(t) for t in r.values())
for rev in ('HEAD', 'WORK'):
    cc = load(rev, CCN)
    P = {p['identifier']: p for p in cc['prompts']}
    nm = {i: p['name'] for i, p in P.items()}
    order = [r['identifier'] for r in cc['prompt_order'][1]['order']]
    patches = [i for i in P if nm[i].startswith('🩹')]
    skip = {i for i in P if nm[i].startswith(('🌳', '🌿')) or 'twin' in nm[i]} | {'enhanceDefinitions'} | set(patches)
    no_patch = set(order) - skip
    figs = {}
    for p in patches:
        figs[nm[p][14:]] = tok(ab.simulate_cc(cc, no_patch | {p}, 1)[0])
    g38 = [i for i in patches if 'Gemini 3.8' in nm[i]][0]; gaio = [i for i in patches if 'All-In-One' in nm[i]][0]
    figs['Gemini 3.8 + All-In-One'] = tok(ab.simulate_cc(cc, no_patch | {g38, gaio}, 1)[0])
    twin = [i for i in P if 'twin' in nm[i]][0]; lc = '15b770cf-6049-5f3b-b25d-be09728a65d5'
    figs['GLM, twin instead of LC'] = tok(ab.simulate_cc(cc, (no_patch - {lc}) | {twin} | {[i for i in patches if nm[i].endswith('GLM')][0]}, 1)[0])
    print(f'CC {rev}: everything ON per patch:', ', '.join(f'{k}={v}' for k, v in figs.items()), '| max', max(figs.values()))
    tc = load(rev, TCN)
    sw = dict(ab.SWITCH.findall(tc['sysprompt']['content']))
    tpatches = [s for s in sw if s.startswith('aria-patch')]
    base = {s: 'on' for s in sw if not s.startswith('aria-patch')} | {p: 'off' for p in tpatches}
    tf = {}
    for p in tpatches:
        r, _ = ab.simulate_tc(tc, base | {p: 'on'}, 1)
        tf[p[11:]] = tok(r)
    tf['no patch'] = tok(ab.simulate_tc(tc, base, 1)[0])
    print(f'TC {rev}: everything ON per patch:', ', '.join(f'{k}={v}' for k, v in tf.items()), '| max', max(tf.values()))
