#!/usr/bin/env python3

# Re: k-term expansions of a rational fraction less than 1
# - jiw -  2020

from sys import argv, exit
import time

# Get params:
arn = 0
arn+=1; nLo = int(argv[arn]) if len(argv)>arn else 4
arn+=1; d   = int(argv[arn]) if len(argv)>arn else 17
arn+=1; kHi = int(argv[arn]) if len(argv)>arn else 3
arn+=1; nHi = int(argv[arn]) if len(argv)>arn else nLo

def gcd(a,b): # We compute gcd(a,b) if a,b are positive integers
    while a:
        a, b = b % a, a
    return b

def nextTerm(n,d,k,pd):
    g = gcd(n,d)
    n1, d1 = n//g, d//g
    if n1 == 1 and d1>pd:
        terms[-k]=d1
        sols.append(terms[:len(terms)-k+1])
        return
    t1 = max(pd+1, (d1+n-1)//n) # Find smallest feasible denominator
    #print (f'k {k}  {n1:3}/{d1:<5}  {t1:4}  {terms}')
    while k*d1 > n1*t1:         # while k/t > n/d ...
        terms[-k]=t1
        n2 = n1*t1 - d1         # n/d - 1/t = (n*t-d)/(d*t)
        if n2 > 0:
            nextTerm(n2, d1*t1, k-1, t1)
        t1 += 1

for n in range(nLo,nHi+1):
    terms, sols = [0]*kHi, []
    t0 = time.time()
    nextTerm(n,d,kHi, 0)
    tus = int((time.time()-t0)*1e6)
    print (f'{n:3}/{d}: {sols} in {tus} us')

