import sys
sys.path.insert(0,'/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab, random
def T(s):
    st={}
    out=ab.render(s,st,random.Random(1))
    return len(out), ab.tokens(out), out
if __name__=='__main__':
    s=sys.stdin.read()
    n,t,out=T(s)
    print(n,'chars',t,'tokens (ceil: chars<=%d for round)'%0)
