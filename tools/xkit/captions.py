#!/usr/bin/env python3
"""Caption helpers for the X / Threads mirrors.
  fix(text)   -> wraps every line that starts with a Latin (left-to-right) character in LRI…PDI
  xweight(t)  -> X weighted length of fix(t)   (must be <= 278)
  tbytes(t)   -> UTF-8 bytes of fix(t)         (Threads, must be <= 480)
Usage: python3 -I captions.py 'text'   (prints both numbers)"""
import sys, unicodedata
LRI, PDI = '⁦', '⁩'
def _first_strong(s):
    for c in s:
        b = unicodedata.bidirectional(c)
        if b == 'L': return 'L'
        if b in ('R', 'AL'): return 'R'
def fix(t):
    return '\n'.join((LRI + l + PDI) if (l.strip() and _first_strong(l) == 'L') else l for l in t.split('\n'))
def xweight(t):
    return sum(1 if (o <= 4351 or 8192 <= o <= 8205 or 8208 <= o <= 8223 or 8242 <= o <= 8247) else 2 for o in map(ord, fix(t)))
def tbytes(t):
    return len(fix(t).encode())
if __name__ == '__main__':
    t = sys.argv[1]
    print('X weight', xweight(t), '· Threads bytes', tbytes(t), '· has @', '@' in t)
