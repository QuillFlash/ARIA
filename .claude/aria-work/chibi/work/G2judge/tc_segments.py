import json, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
from paths import *
draft_path = sys.argv[1] if len(sys.argv) > 1 else DRAFT
tag = sys.argv[2] if len(sys.argv) > 2 else 'draft'
d = json.load(open(TC, encoding='utf-8'))
ph = d['sysprompt']['post_history']
i = ph.index('<final_gate>')
src_gate = ph[i:]
open(W + '/tc_gate_src.txt', 'w', encoding='utf-8').write(src_gate)
c = d['sysprompt']['content']
a = c.index('{{setvar::ariaEchoGate::- ')
b = c.index('</anti_slop>') + len('</anti_slop>')
src_codex = c[a:b]
open(W + '/tc_codex_src.txt', 'w', encoding='utf-8').write(src_codex)
# CC codex body after comment+trim+newline
cc = json.load(open(CC, encoding='utf-8'))
by = {p['identifier']: p for p in cc['prompts']}
cc_codex = by[CODEX]['content']
body = cc_codex[cc_codex.index('{{trim}}\n') + len('{{trim}}\n'):]
print('CC codex body == TC codex segment:', body == src_codex)
dr = json.load(open(draft_path, encoding='utf-8'))
dc = dr['prompts'][CODEX]['content']
dbody = dc[dc.index('{{trim}}\n') + len('{{trim}}\n'):]
open(W + f'/tc_codex_{tag}.txt', 'w', encoding='utf-8').write(dbody)
open(W + f'/tc_gate_{tag}.txt', 'w', encoding='utf-8').write(dr['tc']['post_history_gate'])
# CC gate body vs TC gate src: diff is only the 'A message written as' notes
g = by[GATE]['content']
gbody = g[g.index('{{trim}}\n') + len('{{trim}}\n'):]
print('CC gate body == TC gate src:', gbody == src_gate)
import difflib
for l in difflib.unified_diff(gbody.splitlines(), src_gate.splitlines(), 'cc', 'tc', lineterm='', n=0):
    print('   ', l)
# Same for draft
dg = dr['prompts'][GATE]['content']
dgbody = dg[dg.index('{{trim}}\n') + len('{{trim}}\n'):]
print('--- draft CC gate body vs draft TC gate:')
for l in difflib.unified_diff(dgbody.splitlines(), dr['tc']['post_history_gate'].splitlines(), 'cc', 'tc', lineterm='', n=0):
    print('   ', l)
