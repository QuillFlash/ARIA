import sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/build/chibi_tc')
import verify_chibi_tc as v

def main():
    p = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/build/chibi_tc/out/chibi_tc_finals_glue.json'
    t, nbad, pr = v.verify(p, glue='finals', jobs=4, quiet=True, stride=11)
    print(f'finals-glue file, verified as finals: {t} renders, {nbad} bad, {len(pr)} problem kinds')
    t2, nbad2, pr2 = v.verify(p, glue='capped', jobs=4, quiet=True, stride=11)
    print(f'finals-glue file, verified as capped: {t2} renders, {nbad2} bad, {len(pr2)} problem kinds (must be flagged)')
    ok = (nbad == 0 and not pr and nbad2 > 0)
    print('GLUE MODES OK' if ok else 'GLUE MODES FAILED')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
