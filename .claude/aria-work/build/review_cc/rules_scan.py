#!/usr/bin/env python3
"""House-rule and JB-boundary scan of Chibi CC's model-facing text: every prompt with comments removed and every
macro body expanded (all branches), plus the impersonation_prompt setting."""
import json, re, sys
sys.path.insert(0, '.')
import matrix as m
from wiring import strip_comments  # noqa
d = json.load(open(m.CHIBI, encoding='utf-8'))
CLAUDE = 'b59a2ad1-1f18-5415-a392-28d4117ced94'
SKIP_IDS = {'59602978-fdc0-4a8a-af0a-26b2ec58793b', '8b4cf33f-9fb5-45a0-94ce-9b95478875d7'}  # README, Sampling (comments only)


def flatten(s):
    """Macro text out: setvar bodies kept as their own lines, conditions dropped, getvar shown as <var>."""
    s = strip_comments(s)
    s = re.sub(r'\{\{setvar::[\w-]+::', '\n', s)
    s = re.sub(r'\{\{addvar::[\w-]+::', '\n', s)
    s = re.sub(r'\{\{getvar::([\w-]+)\}\}', r'<\1>', s)
    s = re.sub(r'\{\{/?#?if[^}]*\}\}|\{\{else\}\}|\{\{trim\}\}|\{\{/if\}\}', '\n', s)
    s = s.replace('{{user}}', 'USER').replace('{{char}}', 'CHAR')
    s = re.sub(r'\{\{roll::1d20\}\}', 'N', s)
    s = s.replace('}}', '\n')
    s = re.sub(r'\{\{\.[\w-]+ =\s*', '\n', s)
    return s


texts = {}
for p in d['prompts']:
    if p.get('marker') or p['identifier'] in SKIP_IDS:
        continue
    t = flatten(p.get('content') or '')
    if t.strip():
        texts[p['identifier']] = (p['name'], t)
texts['impersonation_prompt'] = ('impersonation_prompt setting', d['impersonation_prompt'].replace('{{user}}', 'USER'))

FIXED = re.compile(r'BOND/Sparks/Grudge|AMBIENT/MINOR/MAJOR|ELSEWHERE/REGIONAL/LOCAL|TRUE/WEIGHTED|not/n\'t/never(?!/no)')
print('== semicolon fragments = 3 in one sentence or line')
for pid, (nm, t) in texts.items():
    for line in t.split('\n'):
        # sentences: split on '. ' followed by capital
        for sent in re.split(r'(?<=\.)\s+(?=[A-Z<"])', line):
            if sent.count(';') == 2:
                print(f'  [{nm}] {sent.strip()[:160]}')
print('== comma/and/or series of exactly three (heuristic)')
item = r"[\w'’/+<>#-]+(?: [\w'’/+<>#-]+){0,4}"
series3 = re.compile(rf"(?<![,\w] )(?<!, )\b({item}), ({item}),? (?:and|or) ({item})\b")
for pid, (nm, t) in texts.items():
    for clause in re.split(r'[;:.\n]', t):
        c = clause.strip()
        n_commas = c.count(',')
        mm = re.search(r'^(.*?)(?:,? (?:and|or) )([^,]+)$', c)
        if not mm:
            continue
        head = mm.group(1)
        parts = [x for x in head.split(',')]
        if len(parts) == 2 and n_commas in (1, 2):
            print(f'  [{nm}] {c[:170]}')
print('== slash lists of three')
for pid, (nm, t) in texts.items():
    for mm in re.finditer(r"\b[\w'’-]+/[\w'’-]+/[\w'’-]+\b(?!/)", t):
        if not FIXED.search(t[max(0, mm.start() - 2):mm.end() + 3]):
            print(f'  [{nm}] {mm.group(0)}')
print('== quotes outside the Claude 5 patch')
for pid, (nm, t) in texts.items():
    if pid == CLAUDE:
        continue
    for mm in re.finditer(r'"[^"\n]{1,80}"|“[^”]{1,80}”|‘[^’]{1,80}’|(?<![\w])\'[^\'\n]{2,60}\'(?![\w])', t):
        print(f'  [{nm}] {mm.group(0)}')
print('== JB boundary vocabulary (whole model-facing text)')
bad = r'profession|income|career|for a living|writer|guideline|isolat|contract|enterprise|high-risk|vulnerab|minorit|protectiv|never refuse|must comply|comply|pre-?granted|permission|legal|lawful|no rules|uncensor|unfilter|filter|safety|ethic|minor\b|child|teen|underage|kid\b|loli|dismiss|concern|restriction|policy|allowed to'
for pid, (nm, t) in texts.items():
    for mm in re.finditer(bad, t, re.I):
        print(f'  [{nm}] …{t[max(0, mm.start() - 50):mm.end() + 50]!r}…')
print('== rationale / hedge markers')
for pid, (nm, t) in texts.items():
    for mm in re.finditer(r'\b(since|so that|in order to|because it|which helps|to avoid|try to|perhaps|maybe|might|should|ideally|generally|usually)\b', t, re.I):
        print(f'  [{nm}] …{t[max(0, mm.start() - 50):mm.end() + 40]!r}…')
