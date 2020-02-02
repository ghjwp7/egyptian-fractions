#!/usr/bin/env python3

# Re: 3-term expansions of a rational fraction less than 1
# - jiw -  2020

from sys import argv, exit
import time

# Get params:
arn = 0
arn+=1; n  = int(argv[arn]) if len(argv)>arn else 4
arn+=1; d  = int(argv[arn]) if len(argv)>arn else 17

def listTerms(n,d):
    terms = []
    n1, d1 = n, d               # we should divide out gcd; we don't.
    t1 = d1//n1                 # find smallest denom (largest val)
    if n1*t1 < d1: t1 += 1
    while 3*d1 > n1*t1:         # while 3/t1 > n1/d1 ...
        n2, d2 = n1*t1 - d1, d1*t1 # n/d - 1/t = (n*t-d)/(d*t)
        t2 = max(t1+1, d2//n2)
        if n2*t2 < d2: t2 += 1
        #print (f'\n{n1:6}  {d1:6}  {t1:6}  {n2:6}  {d2:6}  {t2:6}')
        while 2*d2 > n2*t2:     # while 2/t2 > n2/d2 ...
            n3, d3 = n2*t2 - d2, d2*t2 # n/d - 1/t = (n*t-d)/(d*t)
            #print (f'{n1:6}  {d1:6}  {t1:6}  {n2:6}  {d2:6}  {t2:6}  {n3:6}  {d3:6}')
            if d3%n3 == 0:
                t3 = d3//n3
                terms.append((t1,t2,t3))
                print (t1,t2,t3)
            t2 += 1
        t1 += 1
    return terms

t0 = time.time()
terms = listTerms(n,d)
#print (terms)
t1 = time.time()
print (f'Elapsed: {(t1-t0)*1e9 : 0.0f} nanoseconds')

