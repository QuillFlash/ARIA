import sys
from m import t
def L(*lines):
    for s in lines:
        n = t(s)[0]
        print(f'{n:6.2f}  f{len(s.split(";"))}  {s}')
    print()
L("- Person: help, praise, advise or comfort {{user}} only as far as card and bond allow.",
  "- Person: agree or push back per card; help, praise, advise or comfort {{user}} only as card and bond allow.",
  "- Person: agree or push back per card; help, praise, advise or comfort {{user}} only as far as card and bond allow.")
L("- Replies: answer {{user}}'s whole move; a true line keeps its size; then something new.",
  "- Replies: answer {{user}}'s whole move, main concern first; a true line keeps its size, then something new.",
  "- Replies: answer {{user}}'s whole move, the character's main concern first; a true line keeps its size, then something new.",
  "- Replies: answer {{user}}'s whole move, what they care about most first; a true line keeps its size, then something new.",
  "- Replies: answer {{user}}'s whole move; their main concern first; a true line keeps its size; then something new.")
L("- Filler: steadying or self-talk filler becomes the held thought or an act; one stays when answering.",
  "- Filler: steadying or self-talk filler becomes its thought or an act; one stays as an answer.",
  "- Filler: steadying or self-talk filler becomes its thought or an act; one stays when answering.")
L("- Pushback: say what they hold plainly, never what {{user}}'s view or their last line is not; a refusal stays a plain no; cut a not/n't/never half beside one on its subject, denials and claim fixes too.",
  "- Pushback: say what they hold plainly, never what {{user}}'s view or their last line is not, and a refusal stays a plain no; cut a not/n't/never half beside one on its subject, denials and claim fixes too.",
  "- Pushback: say plainly what they hold, a refusal a plain no, never what {{user}}'s view or their last line is not; cut a not/n't/never half beside one on its subject, denials and claim fixes too.")
L("- Restate: cut repeats or bare labels of the line before, intensified or not, and a phrase anywhere marking speech as on record, honest, clear or said first; stammers stay.",
  "- Restate: cut repeats or bare labels of the line before, intensified or not, and phrases anywhere marking speech as on record, honest, clear or said first; stammers stay.",
  "- Restate: cut a repeat or bare label of the last line, intensified or not, and a phrase anywhere marking speech as on record, honest, clear or said first; stammers stay.")
L("- Mood: card mood and energy, shaded by ties to {{user}}, back after events.",
  "- Mood: card mood and energy, shaded by ties to {{user}}, return after events.",
  "- Lulls: in pauses, raise what the card cares about or wants.",
  "- Lulls: characters raise card interests and wants.",
  "- Lulls: raise card interests and wants.")
L("- Work words, narration too: only for work underway, raised, due or dodged; feelings, memories, promises, decisions show as acts or choices.",
  "- Work words, narration too: only for work underway, raised by others, due now or dodged; feelings, memories, promises, decisions show as acts or choices.",
  "- Work words, narration too: only for work underway, raised by someone else, due now or dodged; feelings, memories, promises, decisions show as acts or choices.")
L("- Demands: press once; refused or sidestepped, act or trade, else drop it; own lines and pet phrases rest four replies.",
  "- Demands: press a demand or offer once; refused or sidestepped, act or trade, else drop it; the scene moves on; own lines and pet phrases rest four replies.",
  "- Demands: press once; refused or sidestepped, act or trade, else drop it; the scene moves on; own lines and pet phrases rest four replies.",
  "- Demands: press once, then, refused or sidestepped, act or trade, else drop it and move on; own lines and pet phrases rest four replies.")
L("- Runs: a sentence under five words stands once a reply; extras join a neighbour; stalls and cut-offs, one-word answers, long paragraphs, jokes stay.",
  "- Runs: one sentence under five words a reply at most, extras joining a neighbour; stalls, cut-off lines, one-word answers, long paragraphs and jokes stay.",
  "- Runs: a sentence under five words stands once a reply at most, extras join a neighbour; stalls, cut-offs, one-word answers, long paragraphs and jokes stay.",
  "- Runs: one sentence under five words a reply at most, the rest joining a neighbour; stalls, cut-off lines, one-word answers, long paragraphs and jokes stay.")
L("; a raw in-voice thought each, steering the move", "; a raw in-voice thought each, steering their move", "; a raw in-voice thought each, behind their move", "; one raw in-voice thought each, steering it")
L("- Layers: per card character, one trait the mood fits, one it buries, in card words; both show this reply.",
  "- Layers: per card character, one trait the mood fits, one it buries, in card words; both show this reply in an act or line.",
  "- Layers: card characters keep every trait and want the whole chat; strong moods tint, buried traits still show.")
