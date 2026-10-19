import json, sys
from m import t
from rows import IDS
d = json.load(open(sys.argv[1], encoding='utf-8'))
st0 = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
for k, pid in IDS.items():
    n, out, st = t(d['prompts'][pid]['content'], st0)
    print(f'##### {k}  own={n}')
    print(repr(out))
    for v in ('gemini38Patch','ariaChopGate','ariaPatchGate','ariaPatchTally','ariaPatchJoins','ariaFlashGate','ariaVoiceExtra','ariaHoldLine','ariaHoldGate'):
        if st.get(v) and st.get(v) != st0.get(v):
            print(f'  [{v}]'); print('   ' + st[v].replace('\n', '\n   '))
