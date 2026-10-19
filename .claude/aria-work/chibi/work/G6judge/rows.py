"""Measure every G6 row of a draft-format JSON exactly (characters / 4)."""
import json, sys
from m import t
IDS = {
 'claude':'b59a2ad1-1f18-5415-a392-28d4117ced94','g38':'333dbbed-344d-4a6c-90c5-b0625291115a','gem':'ac96376e-5777-595b-8f48-359f864b0685',
 'glm':'1f2e1f97-1cde-5d46-8eb0-87e2fe55f916','kimi':'9bb6c2b0-7906-564f-852e-3d8c327b4879','mpro':'33f92483-e84c-54a6-9188-1189aff1098a',
 'mflash':'3a027832-2e4b-4706-aaed-5fc6ec5e59ad','ds':'e04b9c2b-d8a0-5346-ab66-1cf25e5d7c1b','fg':'2e3e7f63-8463-51ff-ba8f-e5b05162c193',
 'hold':'dc8b1acb-9a7e-5a43-b9aa-38e7b70662a3'}
CEIL = {'claude own':80,'g38 own (gemini38Patch)':50,'gem own':50,'gem lines':90,'glm own':50,'glm lines':120,'kimi own':50,'kimi lines':90,
        'mpro own':50,'mpro lines':90,'mflash own':50,'mflash lines':90,'ds own (Tally on)':50,'ds lines':90,'Tally (Bonds+Fate)':55,'Joins':25,
        'FG lines (with Runs)':90,'VoiceExtra':12,'Hold two lines':55}
def rows(d):
    P = d['prompts']; r = {}
    c = lambda k: P[IDS[k]]['content']
    r['claude own'] = t(c('claude'))[0]
    _, _, st = t(c('g38')); r['g38 own (gemini38Patch)'] = len(st['gemini38Patch'])/4
    n, out, st = t(c('gem')); r['gem own'] = n; r['gem lines'] = len(st['ariaPatchGate'])/4; r['gem Speech (ariaChopGate)'] = len(st['ariaChopGate'])/4
    n, out, st = t(c('gem'), {'gemini38Patch': json.dumps(0)}); 
    for k in ('glm','kimi','mpro','mflash'):
        n, out, st = t(c(k)); r[k+' own'] = n; r[k+' lines'] = len(st['ariaPatchGate'])/4
    n, out, st = t(c('ds'), {'ariaBondsLine':'x','ariaFateLine':'x'}); r['ds own (Tally on)'] = n; r['Tally (Bonds+Fate)'] = len(st['ariaPatchTally'])/4
    r['ds lines'] = len(st['ariaPatchGate'])/4; r['Joins'] = len(st['ariaPatchJoins'])/4
    n, out, st = t(c('ds')); r['ds own (no Tally)'] = n
    _, _, st = t(c('ds'), {'ariaBondsLine':'x'}); r['Tally (Bonds only)'] = len(st['ariaPatchTally'])/4
    _, _, st = t(c('ds'), {'ariaFateLine':'x'}); r['Tally (Fate only)'] = len(st['ariaPatchTally'])/4
    _, _, st = t(c('fg')); r['FG lines (with Runs)'] = len(st['ariaFlashGate'])/4; r['VoiceExtra'] = len(st['ariaVoiceExtra'])/4
    _, _, st = t(c('fg'), {'ariaPatchJoins':'x'}); r['FG lines (no Runs)'] = len(st['ariaFlashGate'])/4
    _, _, st = t(c('hold')); r['Hold two lines'] = (len(st['ariaHoldLine'])+len(st['ariaHoldGate']))/4
    r['  HoldLine'] = len(st['ariaHoldLine'])/4; r['  HoldGate'] = len(st['ariaHoldGate'])/4
    return r
def paths(r):
    p = {}
    p['GLM'] = r['glm own'] + 2*r['glm lines']
    p['MiMo Flash'] = r['mflash own'] + 2*r['mflash lines']
    p['DeepSeek (FG on: no Joins, no Runs)'] = r['ds own (Tally on)'] + 2*r['ds lines'] + r['Tally (Bonds+Fate)'] - (r['FG lines (with Runs)'] - r['FG lines (no Runs)'])
    p['DeepSeek (FG off)'] = r['ds own (Tally on)'] + 2*r['ds lines'] + r['Tally (Bonds+Fate)'] + 2*r['Joins']
    p['Gemini AIO + 3.8 (Speech swaps Chop 30.5)'] = r['gem own'] + 2*r['gem lines'] + r['g38 own (gemini38Patch)'] + r['gem Speech (ariaChopGate)'] - 30.5
    p['MiMo Pro'] = r['mpro own'] + 2*r['mpro lines']
    p['Kimi'] = r['kimi own'] + 2*r['kimi lines']
    p['Claude'] = r['claude own']
    return p
if __name__ == '__main__':
    for f in sys.argv[1:]:
        d = json.load(open(f, encoding='utf-8')); r = rows(d)
        print('====', f)
        tot = 0
        for k, v in r.items():
            ce = CEIL.get(k)
            if ce is not None: tot += v
            print(f'  {v:7.2f}' + (f' / {ce:3}  {v-ce:+7.2f}' if ce is not None else ' '*15) + f'  {k}')
        print(f'  group sum (ceiling rows): {tot:.2f} / {sum(CEIL.values())}')
        for k, v in sorted(paths(r).items(), key=lambda x: -x[1]):
            print(f'  path {v:7.2f}  {k}')
        k = paths(r)['GLM'] + r['FG lines (with Runs)'] + r['VoiceExtra'] + r['Hold two lines']
        print(f'  kitted-out G6 share (GLM + FG + VoiceExtra + Hold): {k:.2f}  (table share 447)')
