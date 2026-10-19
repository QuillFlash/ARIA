import json, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
from paths import *
cc = json.load(open(CC, encoding='utf-8'))
rs = cc.get('extensions', {}).get('regex_scripts', [])
for r in rs:
    print('---', r.get('scriptName'))
    print('   find:', r.get('findRegex')[:600])
    print('   repl:', repr(r.get('replaceString'))[:200], 'placement', r.get('placement'), 'promptOnly', r.get('promptOnly'), 'markdownOnly', r.get('markdownOnly'))
