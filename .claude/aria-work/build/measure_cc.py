"""Fix 4: what each CC entry costs, flip one entry from the shipped state (prerequisites held on where an entry needs them)."""
import json
from rxlib import *

cc = json.load(open(CCFILE, encoding='utf-8'))
prompts = {p['identifier']: p for p in cc['prompts']}
order = cc['prompt_order'][1]['order']
name = {pid: p['name'] for pid, p in prompts.items()}
shipped = {r['identifier'] for r in order if r['enabled']}


def total(enabled, imp=False):
    r, _ = ab.simulate_cc(cc, enabled, seed=1, impersonate=imp)
    return sum(ab.tokens(t) for t in r.values()), sum(len(t) for t in r.values()) / 4, r


def pid_of(prefix):
    m = [pid for pid in prompts if name[pid] == prefix] or [pid for pid in prompts if name[pid].startswith(prefix)]
    assert len(m) == 1, (prefix, m)
    return m[0]


base_tok, base_chars, _ = total(shipped)
print('shipped default:', base_tok, 'tokens (exact', base_chars, ')')
print()
NSFW = pid_of('🔞')
rows = []
for r in order:
    pid = r['identifier']
    p = prompts[pid]
    if p.get('marker') or not (p.get('content') or '').strip():
        continue
    extra = set()
    note = ''
    if pid == pid_of('😈'):
        extra, note = {NSFW}, ' (with Adult Context on)'
    if pid == pid_of('🔓'):
        extra, note = {NSFW}, ' (with Adult Context on)'
    if pid == pid_of('🧠 The Logic Core (system-role twin)'):
        extra, note = set(), ' (twin ON with the plain Logic Core OFF)'
    base = shipped | extra
    flipped = (base - {pid}) if pid in base else (base | {pid})
    if pid == pid_of('🧠 The Logic Core (system-role twin)'):
        base = shipped - {pid_of('🧠 The Logic Core')} - {pid}
        flipped = base | {pid}
    a, ca, _ = total(base)
    b, cb, _ = total(flipped)
    rows.append((name[pid], 'ON ' if pid in shipped else 'off', abs(b - a), abs(cb - ca), note))
for n, st, t, c, note in rows:
    print(f'{n[:52]:52} ships {st} | flip {t:4} tokens (exact {c:7.2f}){note}')
