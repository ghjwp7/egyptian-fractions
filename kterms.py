#!/usr/bin/env python3
# Re: k-term expansions of a rational fraction less than 1
# - jiw -  2020, 2023

# Usage:   ./kterms.py  minNumerator  d  kHi  maxNumerator 
# Default values are  4  17  3  4

# For n from minNumerator to maxNumerator, find Egyptian Fractions
# (sums of distinct unit fractions) for n/d, with up to kHi max number
# of terms.  For example, ./kterms.py 2 3 3 6 gives following output:
#   2/3: [[2, 6], [3, 4, 12]] in 9 us
#   3/3: [[1]] in 1 us
#   4/3: [[1, 3]] in 2 us
#   5/3: [[1, 2, 6]] in 2 us
#   6/3: [] in 1 us

# Method: kterms uses about the same method as 3terms; in essence,
# nested while loops that run trial denominators from a tight lower
# bound t upwards until the corresponding unit fraction is so small
# that remaining terms can't cover the target fraction.  For example,
# if our target is f=2/3 and we seek a 3-term expansion, we must have
# 3/t>2/3, which is 9 > 2t or 5>t.  Actually, due to the distinct unit
# fractions requirement, we must have 1/t + 1/(t+1) + 1/(t+2) > f,
# which is (3t^2 + 6t + 2)/(t^3 + 3t^2 + 2t) > f, which is 3(d-n)t^2 +
# 2(3d-n)t + 2d > n*t^3, which might or might not be worth calculating
# as a limit.  For f=2/3 this is met by t < 4, since at t=4, 3t^2 +
# 14t + 6 - 2t^3 = 48+56+6-128 = -18 < 0.
from sys import argv, exit
import time
from signal import signal, SIGINT

# Get params:
arn = 0
arn+=1; nLo = int(argv[arn]) if len(argv)>arn else 4
arn+=1; d   = int(argv[arn]) if len(argv)>arn else 17
arn+=1; kHi = int(argv[arn]) if len(argv)>arn else 3
arn+=1; nHi = int(argv[arn]) if len(argv)>arn else nLo

# Set up for clean exit on ctrl-c
def sigHandler(sig, frame):
    print(f'\nInterrupted - terms={terms}, #sols={len(sols)}: {sols[:5]}... \n')
    exit(0)
signal(SIGINT, sigHandler)

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

