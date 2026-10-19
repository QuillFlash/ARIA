import json, re
S='/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
cc=json.load(open(S+"/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json",encoding='utf-8'))
tc=json.load(open(S+"/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",encoding='utf-8'))
s=tc['sysprompt']['content']
by={p['identifier'][:8]:p for p in cc['prompts']}
MAP={'aria-patch-glm':'1f2e1f97','aria-patch-kimi-qwen':'9bb6c2b0','aria-patch-mimo-pro':'33f92483','aria-patch-mimo-flash':'3a027832','aria-patch-deepseek':'e04b9c2b','aria-flash-gate':'2e3e7f63','aria-character-hold':'dc8b1acb'}
def body(c):
    # model-facing body after the leading comment and {{trim}}
    i=c.index('}}{{trim}}')+len('}}{{trim}}')
    return c[i:]
def wrap(sw, b):
    b2 = b[1:] if b.startswith('\n') else b
    if sw=='aria-flash-gate':
        return '{{if .aria-flash-gate}}'+b2+'{{/if}}'
    if sw=='aria-character-hold':
        return '{{#if .aria-character-hold}}'+b2+'{{/if}}'
    return '{{#if .'+sw+'}}'+b2+'\n{{/if}}'
if __name__=='__main__':
    for sw,pid in MAP.items():
        w=wrap(sw, body(by[pid]['content']))
        n=s.count(w)
        i=s.find(w)
        print(sw, 'occurrences', n, 'before', repr(s[i-3:i]), 'after', repr(s[i+len(w):i+len(w)+30]))
