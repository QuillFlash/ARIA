from common import *
for path in (ARIA_TC, CHIBI_TC):
    raw = path.read_text(encoding='utf-8')
    d = json.loads(raw)
    print(path.name[:60], '| indent4 round-trip:', json.dumps(d, ensure_ascii=False, indent=4) == raw, '| trailing newline:', raw.endswith('\n'),
          '| CRLF:', '\r' in raw, '| \\u escapes:', len(re.findall(r'\\u[0-9a-fA-F]{4}', raw)))
d = load(CHIBI_TC)
for k in ('content', 'post_history'):
    s = d['sysprompt'][k]
    print(k, '| literal backslash-n:', s.count('\\n'), '| tabs:', s.count('\t'), '| trailing spaces on lines:', len(re.findall(r'[ \t]+\n', s)), '| double spaces:', len(re.findall(r'(?<=\S)  (?=\S)', s)))
raw = CHIBI_TC.read_text(encoding='utf-8')
print('email-like strings:', re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', raw), '| icloud:', 'icloud' in raw.lower())
print('macro balance: {{', raw.count('{{'), '}}', raw.count('}}'))
# JB boundary over the model-facing render with JB on and the JB comment
r, st = ab.simulate_tc(d, {'aria-logic-core': 'on', 'aria-adult': 'on', 'aria-freaky': 'on', 'aria-jailbreak': 'on', 'aria-fate': 'on', 'aria-bonds': 'on',
                         'aria-patch-glm': 'on', 'aria-flash-gate': 'on', 'aria-character-hold': 'on', 'aria-hybrid-pov': 'on', 'aria-time-place': 'on', 'aria-anthro': 'on'}, 1)
mf = r['System Prompt'] + '\n' + r['Post-History']
BAD = r'professional|for a living|income|career|guideline|no rules|isolated|enterprise|contract|high-risk|never refuse|must not refuse|comply|minorit|protective|vulnerable|legal|permission|pre-?granted|dismiss|concerns|filter|censor|unrestricted|unfiltered|without limits|no limits|policy|polic(y|ies)|safety'
print('JB boundary hits in model-facing text:', sorted(set(m.group(0).lower() for m in re.finditer(BAD, mf, re.I))))
print('JB lines:', st.get('ariaJb'))
jbc = re.search(r'\{\{// 🔓[^\n]*?\}\}', d['sysprompt']['content']).group(0)
print('JB comment boundary hits:', re.findall(BAD, jbc, re.I))
# quotes in model-facing text
print('double quotes in model-facing text:', [mf[max(0, m.start()-40):m.end()+40] for m in re.finditer(r'["“”]', mf)][:5])
print('single-quoted spans:', [m.group(0) for m in re.finditer(r"(?<![A-Za-z])'[^'\n]{2,60}'(?![A-Za-z])", mf)][:5])
