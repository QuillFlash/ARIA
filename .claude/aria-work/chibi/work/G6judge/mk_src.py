import json
S='/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
p=S+"/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
d=json.load(open(p,encoding='utf-8'))
ids=json.load(open(S+'/chibi/drafts/G6.json',encoding='utf-8'))['prompts'].keys()
by={x['identifier']:x for x in d['prompts']}
out={'prompts':{i:{'name':by[i]['name'],'content':by[i]['content']} for i in ids}}
json.dump(out,open('src_g6.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
