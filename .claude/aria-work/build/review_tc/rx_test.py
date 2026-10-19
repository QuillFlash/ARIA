import subprocess
from common import *
tc, atc = load(CHIBI_TC), load(ARIA_TC)
REAL_PLAN = '- OOC: none\n- Scene: kitchen; mug in hand\n- Knows: Mira heard the door\n- Voice: Mira, wry\n- Move: Mira sets the mug down\n- Fresh: chipped rim\n- Check: lists 1-2\n- go'
PROSE = 'Mira set the mug down on the counter and looked at the door.\n\n"You\'re late," she said.'
cases, meta = {}, {}
for ed, p in (('chibi', tc), ('aria', atc)):
    for tags in ('on', 'off'):
        for extra in ('plain', 'full'):
            sw = {'aria-logic-core': 'on', 'aria-thinking-tags': tags}
            if extra == 'full':
                sw |= {'aria-adult': 'on', 'aria-jailbreak': 'on', 'aria-fate': 'on', 'aria-bonds': 'on', 'aria-hybrid-pov': 'on',
                       'aria-character-hold': 'on', 'aria-patch-glm': 'on', 'aria-time-place': 'on'}
            r, st = ab.simulate_tc(p, sw, 1)
            lc = r['Post-History'].split('<final_gate>')[0].strip()
            assert 'For a message written as User' in lc
            close = re.search(r'For a message written as User[^\n]*? line\.', lc).group(0)
            # echo forms: template alone + prose; template + real plan + prose; template inside the reply after a real plan
            if tags == 'on':
                real = '<thinking>\n' + REAL_PLAN + '\n</thinking>\n'
                cases[f'{ed}|tags {tags}|{extra}|echo+prose'] = lc + '\n' + PROSE
                cases[f'{ed}|tags {tags}|{extra}|echo+plan+prose'] = lc + '\n' + REAL_PLAN + '\n</thinking>\n' + PROSE
                cases[f'{ed}|tags {tags}|{extra}|plan+closing echo+prose'] = real + lc.split('- go', 1)[1].split('\n', 2)[2] + '\n' + PROSE
            else:
                cases[f'{ed}|tags {tags}|{extra}|echo+prose'] = lc + '\n' + PROSE
                cases[f'{ed}|tags {tags}|{extra}|plan+prose'] = REAL_PLAN + '\n' + PROSE
            meta[ed, tags, extra] = close
# old-style echoes must still match
OLD = ('<thinking> opens the reply, then 9 dashed lines, then go.\nLines are fragments...\n' + REAL_PLAN + '\n</thinking> closes on the line after go. The reply starts on the line after that: header if <header_instructions>; prose in flowing paragraphs. Nothing above go enters the reply. When this turn asks for a Fate roll, write the Fate and Ledger lines.\nEvery response starts with <thinking>.\n' + PROSE)
cases['old|tags on|old sentence'] = OLD
json.dump(cases, open(OUT / 'rx_cases.json', 'w'), ensure_ascii=False, indent=1)
json.dump(load(RX_TC), open(OUT / 'rx_scripts_tc.json', 'w'), ensure_ascii=False)
subprocess.run(['node', str(W / 'build/review_tc/rx_pipe.mjs'), str(OUT / 'rx_scripts_tc.json'), str(OUT / 'rx_cases.json'), str(OUT / 'rx_out.json')], check=True)
res = load(OUT / 'rx_out.json')
def outside_details(t):
    return re.sub(r'<details[\s\S]*?</details>', '', t)
bad = 0
for k, v in res.items():
    flags = []
    for kind in ('display', 'prompt', 'impersonate'):
        t = v[kind]
        if kind == 'display':
            t = outside_details(t)
        for needle in ('For a message written as', 'Every response starts with', 'closes on the line after go', 'Nothing above go', 'opens the reply, then', '- go', 'When this turn asks for'):
            if needle in t:
                flags.append(f'{kind}: "{needle}" left')
        if PROSE.split('\n')[0] not in t:
            flags.append(f'{kind}: prose lost')
    print(('OK   ' if not flags else 'LEFT ') + k + ('' if not flags else '  ' + '; '.join(flags)))
    bad += bool(flags)
# Chibi vs ARIA remainders for the same case shape
print('--- chibi vs aria remainders (prompt and impersonate pipelines, same shape):')
for k in res:
    if not k.startswith('chibi|'):
        continue
    ka = 'aria|' + k.split('|', 1)[1]
    for kind in ('prompt', 'impersonate'):
        same = res[k][kind].strip() == res[ka][kind].strip()
        print(f'  {"same" if same else "DIFF"}  {kind:11} {k[6:]}')
        if not same:
            print('     chibi:', repr(res[k][kind][:300])); print('     aria :', repr(res[ka][kind][:300]))
print('closing sentences:'); [print('  ', k, '|', v) for k, v in meta.items()]
