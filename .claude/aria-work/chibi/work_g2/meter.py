#!/usr/bin/env python3
"""Scratch meter for G2: prints per-line sizes (chars/4) of a text block file, one rule per line."""
import sys

def main():
    path = sys.argv[1]
    total = 0
    for i, line in enumerate(open(path, encoding='utf-8').read().split('\n')):
        n = len(line)
        total += n + 1
        print(f'{i:2} {n:5} {n/4:6.1f}  {line[:100]}')
    print('TOTAL chars', total - 1, 'tokens', round((total - 1) / 4))

if __name__ == '__main__':
    main()
