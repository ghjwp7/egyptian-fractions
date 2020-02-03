#!/usr/bin/env python3

# Re: Egyption-fraction expansions of a rational fraction less than 2
# - jiw - 2 Feb 2020

# For a given rational fraction, this program tries out various
# practical-number multipliers to see what Egyption-fraction
# expansions get generated.  It displays all the solutions it finds
# that have no more than kHi terms.

# Parameter default values are shown in this command line:
#          ./pracfracs.py  4  17   5   50000
# Parameter names:         n   d  kHi   fHi

# n and d are numerator and denominator of fraction to be expanded as
#   an Egyptian fraction.  [GCD(n,d) will be divided out.]

# fHi = highest value this routine will factor, ie largest allowed
#   denominator.  With default parameter values, setting up the tables
#   of primes and factors takes a few milliseconds.  For large fHi, it
#   takes several seconds.

# If d is large, make fHi large as well.  For example, use fHi > d*d.
#   When practical numbers being tested grow larger than fHi, the test
#   loop exits.

from sys import argv
from numpy import prod
from itertools import product                                                   
import time

# Get params:
arn = 0
arn+=1; n   = int(argv[arn]) if len(argv)>arn else 4
arn+=1; d   = int(argv[arn]) if len(argv)>arn else 17
arn+=1; kHi = int(argv[arn]) if len(argv)>arn else 5
arn+=1; fHi = int(argv[arn]) if len(argv)>arn else 50000
pHi = 200
while pHi*pHi < fHi:  pHi = (pHi*6)//5 # Make pHi big enough

def gcd(a,b): # We compute gcd(a,b) if a,b are positive integers
    while a:
        a, b = b % a, a
    return b

def nextPrac(d,u):
    # Find multiples of d (and 4 or 6), larger than u, that are
    # practical numbers. 
    minc = d if d%4==0 else (2*d if d%2==0 else 4*d)
    md = (1+u//minc)*minc;   divs = [];   Prac = False
    while not Prac and md < fHi:
        while md%4>0 and md%6>0:
            md += minc
        # Compute prime factors of md (using sfn factors table)
        facs=[];  enpow=bf=0; v=md 
        while v > 1:
            pf = sfn[v]
            v = v//pf
            enpow += 1
            if pf != bf and bf>0:
                facs.append((bf,enpow-1))
                enpow = 1
            bf = pf
        facs.append((bf,enpow))
        pows = [[p**j for j in range(e+1)] for p,e in facs]
        # Divisor test depends on all divisors x, not just x <= m*n
        divs = sorted(x for x in map(prod, product(*pows)))
        # Test if divisor-list prefix sums don't rise too fast
        fsum = divs[0]; Prac = True
        for j in range(1,len(divs)):
            if fsum < divs[j]-1:
                Prac = False
                md += minc
                break
            fsum += divs[j]     # Add current divisor to front sum
    return md, divs

def findSols(n,d,md,divs,sols):
    mn = n * (md//d)
    dix = len(divs)-1
    while divs[dix] > mn and dix>0: dix -= 1
    while 2*divs[dix] >= mn:
        nums = [md//divs[dix]]
        tn = mn - divs[dix]
        tix = dix
        while tn > 0 and tix > -1:
            tix -= 1
            if divs[tix] > tn: continue
            if len(nums) == kHi: break
            nums.append(md//divs[tix])
            tn -= divs[tix]
        if tn==0:
            sol = tuple(nums)
            if not (sol in sols):
                sols.append(sol)
        dix -= 1
        if dix < 0: break
    return sols

def listSols(n,d):
    g = gcd(n,d)
    n, d = n//g, d//g           # Reduce to lowest terms
    md = 0;  sols = [];  npr=0
    while 1:   
        md, divs = nextPrac(d,md)
        if len(divs) < 1: break
        sols = findSols(n,d,md,divs,sols)
        npr += 1
    return sols, npr

# For use when creating practical numbers, create prl and sfn.  prl is
# a list of primes [2, 3, 5...].  Its formula is good up until
# Carmichael number 29341, when a few non-primes start sneaking in.
prl = [2,3,5,7]+[x for x in range(11,pHi,2) if 1==pow(2,x-1,x)==pow(3,x-1,x)==pow(5,x-1,x)==pow(7,x-1,x)]
# sfn[j] is a prime divisor of j if fHi > j > 1.
sfn = [j for j in range(fHi)]   # Init sfn[j] to j
for p in prl:                   # Run a sieve to set divisors
    if p*p > fHi: break
    for j in range(p, fHi, p):  # Set sfn[j] to p if p|j 
        sfn[j]=p

t0 = time.time()
sols, npr = listSols(n,d)
tus = int((time.time()-t0)*1e6)
print (sorted(sols))
print (f'Generated {len(sols)} sols up to length {kHi} for {n}/{d} in {tus} us, trying {npr} practical numbers')
