import json, sys, re
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
from paths import *
d = json.load(open(TC, encoding='utf-8'))
print('TOP KEYS', list(d.keys()))
sp = d['sysprompt']
print('SYSPROMPT KEYS', list(sp.keys()))
c = sp['content']
i = c.find('<anti_slop>')
# find the enclosing #if
j = c.rfind('{{#if', 0, i)
k = c.find('{{/if}}', c.find('</anti_slop>'))
print('==== TC codex block (from preceding #if to closing /if) ====')
print(repr(c[j-400:j]))
print(c[j:k+7])
print('==== count of anti_slop', c.count('<anti_slop>'))
ph = sp['post_history']
print('==== post_history ====')
print(ph)
