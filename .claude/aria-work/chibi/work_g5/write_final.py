#!/usr/bin/env python3
"""write_final.py: write drafts/G5.json (primary), G5.floor.json and G5.full.json."""
import json, sys, random
sys.path.insert(0, '.')
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import importlib, final_texts as F, build_final as B, variants as V, tc_build as TB, menus as M
import aria_budget as ab
for m in (F, B, V, TB, M): importlib.reload(m)

W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
OUT = W + '/chibi/drafts/'
IDS = {'time': '5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa', 'fate': 'acc2177a-34e4-4941-93a2-b80bc18b8c91', 'bonds': '5506d699-fb00-49ce-a631-73b3f0036eae'}

def rt(text, state=None):
    st = dict(state or {})
    out = ab.render(text, st, random.Random(1))
    return out, st

def tk(text, state=None):
    return round(len(rt(text, state)[0]) / 4)

prim = {"prompts": B.assemble()}
c = {k: prim['prompts'][v]['content'] for k, v in IDS.items()}

# ---- tokens
t_time = tk(c['time']); t_fate = tk(c['fate']); t_bonds = tk(c['bonds'])
_, stf = rt(c['fate'])                       # Fate alone
_, stb = rt(c['bonds'])                      # Bonds alone
_, stfb = rt(c['bonds'], {'ariaLedgerLine': 'x'})  # Bonds after Fate
def sv(st, k): return round(len(st[k]) / 4)
_, st_fate_after = rt(c['fate'])
tokens = {
    IDS['time']: t_time,
    IDS['fate']: t_fate,
    IDS['bonds']: t_bonds,
    'ariaDice': sv(stf, 'ariaDice'),
    'ariaFateLine': sv(stf, 'ariaFateLine'),
    'ariaLedgerLine (Fate alone)': sv(stf, 'ariaLedgerLine'),
    'ariaLedgerGate (Fate alone)': sv(stf, 'ariaLedgerGate'),
    'ariaLedgerLine (Fate + Bonds)': sv(stfb, 'ariaLedgerLine'),
    'ariaLedgerGate (Fate + Bonds)': sv(stfb, 'ariaLedgerGate'),
    'Fate dice + plan + ledger + gate lines (Fate + Bonds)': sv(stf, 'ariaDice') + sv(stf, 'ariaFateLine') + sv(stfb, 'ariaLedgerLine') + sv(stfb, 'ariaLedgerGate'),
    'Fate dice + plan + ledger + gate lines (Fate alone)': sv(stf, 'ariaDice') + sv(stf, 'ariaFateLine') + sv(stf, 'ariaLedgerLine') + sv(stf, 'ariaLedgerGate'),
    'ariaBondsLine': sv(stb, 'ariaBondsLine'),
    'ariaLedgerLine (Bonds alone)': sv(stb, 'ariaLedgerLine'),
    'ariaLedgerGate (Bonds alone)': sv(stb, 'ariaLedgerGate'),
}
lines_both = tokens['Fate dice + plan + ledger + gate lines (Fate + Bonds)']
tokens['G5 total, own text + Fate lines + Bonds line (everything on)'] = t_time + t_fate + t_bonds + lines_both + tokens['ariaBondsLine']

# ---- tc text
ts, fs, bs = TB.tc_segments()
tc = {
    'time_place_block': ts,
    'fate_block': fs,
    'bonds_block': bs,
    'switch_comment_time_place': "{{// ⏰ Time & Place: a status line on top of every reply (about 50 tokens in Chibi). Turn on together with Fate.}}",
    'switch_comment_fate': "{{// 🎲 Fate & Chekhov Ledger: the world engine (about 470 tokens in Chibi). Adds a small 🎲 line to every reply. Best with 64k context and a model above 12B; pair it with Time & Place.}}",
    'switch_comment_bonds': "{{// 🥰 Bonds Lite: hidden relationship tracker (about 210 tokens in Chibi). Adds a small line to every reply.}}",
}
for k in ('time_place_block', 'fate_block', 'bonds_block'):
    tokens['tc.' + k] = tk(tc[k])

json.dump({'prompts': prim['prompts'], 'tc': tc, 'tokens': tokens, 'notes': open('notes.txt', encoding='utf-8').read() if len(sys.argv) > 1 else 'NOTES PENDING'},
          open(OUT + 'G5.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def variant(pack, note):
    d = {'prompts': pack['prompts']}
    cc = {k: d['prompts'][v]['content'] for k, v in IDS.items()}
    _, s1 = rt(cc['fate']); _, s2 = rt(cc['bonds'], {'ariaLedgerLine': 'x'})
    d['tokens'] = {IDS['time']: tk(cc['time']), IDS['fate']: tk(cc['fate']), IDS['bonds']: tk(cc['bonds']),
                   'lines (Fate + Bonds on, unchanged)': lines_both + tokens['ariaBondsLine']}
    d['notes'] = note
    return d

floor = variant(V.pack(V.FLOOR_TIME, V.FLOOR_FATE, V.FLOOR_BONDS),
    "ALTERNATIVE to G5.json, the floor: same wiring and format, with Fate, Bonds and Time cut as far as the numbers, ladders, gates, ledger fields and the biggest tester fixes allow (no World, Ambitions, Quiet, carried-state, revive, age-4, age-12 or Residue text, one-line cells, the limit shortened). Every row still sits above its ceiling. Use it if the 3,000 cap or the 2,850 aim needs the room. Comments are the primary's and need adapting.")
full = variant(V.pack(V.FULL_TIME, V.FULL_FATE, V.FULL_BONDS),
    "ALTERNATIVE to G5.json, the full set: every mechanic of the snapshot in Chibi wording (the primary plus every restore-menu item). It shows what the full edition's mechanics cost in this style. Not meant to ship; comments are the primary's.")
json.dump(floor, open(OUT + 'G5.floor.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(full, open(OUT + 'G5.full.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(json.dumps(tokens, ensure_ascii=False, indent=1))
print('floor', floor['tokens']); print('full', full['tokens'])
