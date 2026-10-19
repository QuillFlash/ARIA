import sys
from common import *
def total(p, sw):
    r, _ = ab.simulate_tc(p, sw, 1)
    return sum(ab.tokens(t) for t in r.values()), sum(len(t) for t in r.values()) / 4, r
def report(path, label):
    p = load(path)
    shipped = dict(SW.findall(p['sysprompt']['content']))
    t0, e0, r0 = total(p, shipped)
    print(f'== {label}: shipped {t0} (exact {e0:.2f})')
    flips = {}
    for sw in shipped:
        o = dict(shipped); o[sw] = 'off' if shipped[sw] == 'on' else 'on'
        if sw == 'aria-freaky': o['aria-adult'] = 'on'
        if sw == 'aria-jailbreak': o['aria-adult'] = 'on'
        t1, e1, _ = total(p, o)
        flips[sw] = (t1 - t0, e1 - e0)
    base_adult = dict(shipped) | {'aria-adult': 'on'}
    ta, ea, _ = total(p, base_adult)
    for sw in ('aria-freaky', 'aria-jailbreak'):
        o = base_adult | {sw: 'on'}; t1, e1, _ = total(p, o); flips[sw + ' (over adult)'] = (t1 - ta, e1 - ea)
    for k, (d, e) in flips.items():
        print(f'  {k:32} {d:+5}  exact {e:+8.2f}')
    return p, shipped
p, shipped = report(CHIBI_TC, 'Chibi TC')
# extra measures
def tot(sw): return total(p, sw)[0], total(p, sw)[1]
lean_off = shipped | {'aria-logic-core': 'off'}
print('lean start LC off', tot(lean_off))
for tags in ('on', 'off'):
    a = tot(shipped | {'aria-thinking-tags': tags}); b = tot(shipped | {'aria-thinking-tags': tags, 'aria-logic-core': 'off'})
    print(f'LC cost with tags {tags}: {a[0]-b[0]} exact {a[1]-b[1]:.2f}')
# Logic Core part of post-history alone (shipped, tags on/off)
for tags in ('on', 'off'):
    r, _ = ab.simulate_tc(p, shipped | {'aria-thinking-tags': tags}, 1)
    lc = r['Post-History'].split('<final_gate>')[0]
    cue = r['Post-History'].split('</final_gate>')[1]
    print(f'LC part (tags {tags}): {len(lc)/4:.2f} + cue {len(cue)/4:.2f}')
# adult with LC on and with LC off
for lc in ('on', 'off'):
    a = tot(shipped | {'aria-logic-core': lc}); b = tot(shipped | {'aria-logic-core': lc, 'aria-adult': 'on'})
    print(f'adult with LC {lc}: {b[0]-a[0]} exact {b[1]-a[1]:.2f}')
# scent, pov, fate, bonds, time with LC off as well
for sw in ('aria-hybrid-pov', 'aria-scent', 'aria-fate', 'aria-bonds', 'aria-time-place', 'aria-npc-voice', 'aria-anthro'):
    base = shipped | {'aria-logic-core': 'off'}
    o = base | {sw: 'off' if shipped[sw] == 'on' else 'on'}
    a, b = tot(base), tot(o)
    print(f'{sw} flip with LC off: {b[0]-a[0]:+} exact {b[1]-a[1]:+.2f}')
if len(sys.argv) > 1:
    report(ARIA_TC, 'ARIA TC')
    pa = load(ARIA_TC); sa = dict(SW.findall(pa['sysprompt']['content']))
    for tags in ('on', 'off'):
        a = total(pa, sa | {'aria-thinking-tags': tags, 'aria-logic-core': 'on'}); b = total(pa, sa | {'aria-thinking-tags': tags})
        print(f'ARIA LC with tags {tags}: {a[0]-b[0]}')
        r, _ = ab.simulate_tc(pa, sa | {'aria-thinking-tags': tags, 'aria-logic-core': 'on'}, 1)
        print(f'ARIA LC part (tags {tags}): {len(r["Post-History"].split("<final_gate>")[0])/4:.2f}')
