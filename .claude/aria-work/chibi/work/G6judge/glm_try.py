from m import *
src = open('glm_src.txt',encoding='utf-8').read() if False else None
cands = {
'draft': """- Person: help, praise, advise or comfort {{user}} only as far as card and bond allow.
- Replies: answer {{user}}'s whole move; a true line keeps its size; then something new.
- Filler: steadying or self-talk filler becomes the held thought or an act; one stays when answering.
- Pushback: say what they hold plainly, never what {{user}}'s view or their last line is not; a refusal stays a plain no; cut a not/n't/never half beside one on its subject, denials and claim fixes too.
- Restate: cut repeats or bare labels of the line before, intensified or not, and a phrase anywhere marking speech as on record, honest, clear or said first; stammers stay.""",
'c1': """- Person: agree or push back per card; help, praise, advise or comfort {{user}} only as far as card and bond allow.
- Replies: answer {{user}}'s whole move, main concern first; a true line keeps its size, then the answer moves on.
- Filler: steadying or self-talk filler becomes the held thought or an act; one stays when answering.
- Pushback: disagreeing or reassuring, state your view as plain fact, never what {{user}}'s view or your last line is not, a refusal a plain no; cut a not/n't/never half beside one on its subject, denials and claim fixes too.
- Restate: cut a repeat or bare label of what was just said, intensified or not, and any phrase marking speech as on record, honest, clear or said first; stammers stay, and an act carries the weight.""",
}
for k,v in cands.items():
    tot = show(k, v)
    for line in v.split('\n'):
        n,_,_ = t(line)
        print(f'      {n:6.2f}  frags={len(line.split(";"))}  {line[:70]}')
