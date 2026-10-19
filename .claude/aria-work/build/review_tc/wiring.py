import difflib
from common import *
c, a = load(CHIBI_TC), load(ARIA_TC)
cs, as_ = SW.findall(c['sysprompt']['content']), SW.findall(a['sysprompt']['content'])
print('switches chibi:', cs)
print('switches aria :', as_)
print('names/order equal:', [x for x, _ in cs] == [x for x, _ in as_])
print('default diffs:', [(x, y, z) for (x, y), (_, z) in zip(cs, as_) if y != z])
for part in ('content', 'post_history'):
    sa, sc = skeleton(a['sysprompt'][part]), skeleton(c['sysprompt'][part])
    print(f'--- skeleton {part}: aria {len(sa)} items, chibi {len(sc)}')
    for line in difflib.unified_diff(sa, sc, 'aria', 'chibi', lineterm='', n=2):
        print('   ', line)
# keys beyond sysprompt
for k in a:
    if k == 'sysprompt':
        continue
    diffs = {kk for kk in set(a[k]) | set(c[k]) if a[k].get(kk) != c[k].get(kk)}
    print('top-level', k, 'differs in', diffs)
print('sysprompt keys', list(a['sysprompt']), list(c['sysprompt']))
