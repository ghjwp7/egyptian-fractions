#!/usr/bin/env python3

# Re: Egyption-fraction expansions of a rational fraction less than 1
# - jiw - 2020

# For a given rational fraction, this program tries out various
# practical-number multipliers to see whether most or all of the
# possible k-term Egyption-fraction expansions get generated.

from sys import argv, exit
from numpy import prod
from itertools import product                                                   
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

def nextPrac(d,u,n):
    # Return small-enough divisors of a practical number m > u, where
    # 1==(m,d) and 2m>d.  Most practical numbers are multiples of 4 or 6
    m = max(2*(d//4), 2+((u-2)&(~1)), 6)
    Prac = False
    while not Prac:
        while (m%4>0 and m%6>0) or (gcd(m,d) > 1):
            m += 2
        # Compute prime factors of m (using sfn factors table)
        facs=[];  enpow=bf=0; v=m  
        while v > 1:
            pf = sfn[v]
            v = v//pf
            enpow += 1
            if pf != bf and bf>0:
                facs.append((bf,enpow-1))
                enpow = 1
            bf = pf
        facs.append((bf,enpow))
        #print (f'd {d}   u {u}   m {m} {facs}')
        pows = [[p**j for j in range(e+1)] for p,e in facs]
        divs = sorted(x for x in map(prod, product(*pows)) if x <= m*n)
        # Test if divisor-list front sums not less next divisor less 1
        # (We should test over full list instead of just x <= m*n, but hey)
        fsum = divs[0]; Prac = True
        for j in range(1,len(divs)):
            if fsum < divs[j]-1:
                Prac = False
                m += 2
                break
            fsum += divs[j]     # Add current divisor to front sum
    return m, divs

def findSols(n,d,k):
    g = gcd(n,d)
    n, d = n//g, d//g           # Reduce to lowest terms
    # Process some practical numbers m with 1==(m,d) and 2m > d
    m = 4
    sols = []
    for j in range(11):    
        m, divs = nextPrac(d,m+2,n)
        print (f'n/d {n}/{d}   j {j}   m {m}   divs {divs}')
    return sols

# For use when creating practical numbers, create prl and sfn.
# prl is a list of primes [2, 3, 5...].           (in 0.5 ms)
# sfn[j] is a prime divisor of j if fHi > j > 1.  (in 1.5 ms)
pHi, fHi = 600, 10000
prl = [2,3,5,7]+[x for x in range(11,pHi,2) if 1==pow(2,x-1,x)==pow(3,x-1,x)==pow(5,x-1,x)==pow(7,x-1,x)]
sfn = [j for j in range(fHi)]
for p in prl:
    if p*p > fHi: break         # Beyond sqrt(fHi) we don't care
    for j in range(p, fHi, p): sfn[j]=p # p is a factor of j

for n in range(nLo,nHi+1):
    t0 = time.time()
    sols = findSols(n,d,kHi)
    tus = int((time.time()-t0)*1e6)
    print (f'{n:3}/{d}: {sols} in {tus} us')

