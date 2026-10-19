import sys, re
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
tot = 0
for line in t.split('\n'):
    r = line.replace('{{user}}', 'User')
    k = len(r) / 4
    tot += k
    print(f'{k:6.2f}  {line[:150]}')
print('lines total (no newlines):', tot, ' with newlines:', (len(t.replace('{{user}}', 'User'))) / 4)
