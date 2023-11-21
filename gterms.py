#!/usr/bin/env python3
# Re: k-term expansions of a rational fraction less than 1
# - jiw -  2020, 2023

# Usage:   ./gterms.py  minNumerator  d  kHi  maxNumerator 
# Default values are  4  17  3  4

# For n from minNumerator to maxNumerator, find Egyptian Fractions
# (sums of distinct unit fractions) for n/d, with up to kHi max number
# of terms.  If not given, maxNumerator defaults to minNumerator.

# Example:   ./gterms.py 2 5 3 6  gives following output:
#   2/5:  [3, 15]  Engel
#   2/5:  [3, 15]  Greedy
#   2/5: [[3, 15], [4, 12, 15], [4, 10, 20], [5, 6, 30], [4, 8, 40], [4, 7, 140]] in 110 us
#   3/5:  [2, 10]  Engel
#   3/5:  [2, 10]  Greedy
#   3/5: [[2, 10], [3, 6, 10], [3, 5, 15], [3, 4, 60]] in 32 us
#   4/5:  [2, 4, 20]  Engel
#   4/5:  [2, 4, 20]  Greedy
#   4/5: [[2, 5, 10], [2, 4, 20]] in 28 us
#   5/5:  [1]  Engel
#   5/5:  [1]  Greedy
#   5/5: [[1]] in 13 us
#   6/5:  [1, 5]  Engel
#   6/5:  [1, 5]  Greedy
#   6/5: [[1, 5]] in 18 us

# Example:   ./gterms.py 5 121    gives:
#   5/121:  [25, 775, 31775, 1938275, 234531275]  Engel
#   5/121:  [25, 757, 763309, 873960180913, 1527612795642093418846225]  Greedy
#   5/121: [[33, 121, 363], [45, 55, 1089], [33, 99, 1089], [27, 297, 1089], [44, 55, 2420], [30, 132, 2420], [25, 1100, 2420], [25, 1089, 2475], [33, 93, 3751], [27, 242, 6534], [26, 363, 9438], [25, 825, 9075], [44, 54, 13068], [33, 91, 33033], [25, 770, 42350], [26, 352, 50336], [27, 234, 84942], [26, 351, 84942], [34, 84, 172788], [25, 759, 208725], [26, 350, 275275]] in 508899 us

# Example:   ./gterms.py 5 121 6    interrupted after 4 seconds gives:
#   5/121:  [25, 775, 31775, 1938275, 234531275]  Engel
#   5/121:  [25, 757, 763309, 873960180913, 1527612795642093418846225]  Greedy
#  ^C
#  Interrupted - terms=[25, 757, 763309, 873960180914, 509204265214613779736022, 12154171111535377921160733363945029185751631982], #sols=4: [[25, 757, 763309, 873960180913, 1527612795642093418846225], [25, 757, 763309, 873960180914, 509204265214613779736017, 777866951138264186954279297228503648680841336850], [25, 757, 763309, 873960180914, 509204265214613779736018, 194466737784566046738570206210324823130545136225], [25, 757, 763309, 873960180914, 509204265214613779736020, 77786695113826418695428388006689058020485896100]]... 

# Method: See kterms & 3terms
# gterms is like kterms except (1) it uses gmpy mpz integers,
# (2) before its exhaustive while loops it solves for series via
# (i) Engel series and (ii) Fibonacci / greedy algorithm, and
# (3) if interrupted early, displays up to ~10 solutions
# (4) displays solutions in ascending order of sum of denoms

from sys import argv, exit
import time
from signal import signal, SIGINT
from gmpy2 import mpz

# Get params:
arn = 0
arn+=1; nLo = mpz(argv[arn]) if len(argv)>arn else mpz(4)
arn+=1; d   = mpz(argv[arn]) if len(argv)>arn else mpz(17)
arn+=1; kHi = int(argv[arn]) if len(argv)>arn else 3
arn+=1; nHi = int(argv[arn]) if len(argv)>arn else nLo

# Set up for clean exit on ctrl-c
def sigHandler(sig, frame):
    print(f'\nInterrupted - terms={terms}, #sols={len(sols)}: {sols[:9]}... \n')
    exit(0)
signal(SIGINT, sigHandler)

def gcd(a,b): # We compute gcd(a,b) if a,b are positive integers
    while a:
        a, b = b % a, a
    return b

# Given n/d, engel returns a list of denominators, [a_1,a_2,...]  
# Ref https://en.wikipedia.org/wiki/Engel_expansion "Algorithm for
# computing Engel expansions" for explanations of u_i and a_k
# formulas: u_1 = n/d, a_k = ceil(1/u_k), u_k+1 = u_k * a_k - 1
# while u_i != 0.
def engel(n,d):          
    un, ud, dens = mpz(n), mpz(d), []
    while un > 0:               # using > not != 
        ak = (ud+un-1)//un      # ceil(1/uk)
        dens.append(ak)
        un, ud = un*ak - ud, ud
    # Convert Engel series to Engel expansion & plain integers
    for k in range(1,len(dens)):
        dens[k] *=  dens[k-1]
    return [int(g) for g in dens] # Output as integers

# Given n/d, greedy returns a list of denominators, [a_1,a_2,...]
# Ref https://en.wikipedia.org/wiki/Greedy_algorithm_for_Egyptian_fractions
# At each step, the method when given an input n/d outputs one term
# and a balance to use as the next input.
def greedy(n,d):          
    un, ud, dens = mpz(n), mpz(d), []
    while un > 0:
        den = (ud+un-1)//un     # num/den == 1/ceil(ud/un)
        dens.append(den)
        un, ud = un*den-ud, den*ud
        c = gcd(un, ud)
        un, ud = un//c, ud//c
    return [int(g) for g in dens] # Output as integers

# Run current term thru its range of possible values, using recursion
# to find deeper terms if any
def nextTerm(n,d,k,pd):
    g = gcd(n,d)
    n1, d1 = mpz(n//g), mpz(d//g)
    if n1 == 1 and d1>pd:
        terms[-k]=int(d1)
        sols.append(terms[:len(terms)-k+1])
        return
    t1 = max(pd+1, (d1+n-1)//n) # Find smallest feasible denominator
    #print (f'k {k}  {n1:3}/{d1:<5}  {t1:4}  {terms}')
    while k*d1 > n1*t1:         # while k/t > n/d ...
        terms[-k] = int(t1)
        n2 = n1*t1 - d1         # n/d - 1/t = (n*t-d)/(d*t)
        #dp=d1*t1; print(f'k{k}  n1/d1 {n1}/{d1}  n2/d2 {n2}/{dp}'); exit(0)
        if n2 > 0:
            nextTerm(n2, d1*t1, k-1, t1)
        t1 += 1

for n in range(nLo,nHi+1):
    terms, sols = [0]*kHi, []
    t0 = time.time()
    print (f'{n:3}/{d}:  {engel(n,d)}  Engel')
    print (f'{n:3}/{d}:  {greedy(n,d)}  Greedy')
    nextTerm(n,d,kHi, 0)
    tus = int((time.time()-t0)*1e6)
    ss = sorted(sols, key=sum)
    print (f'{n:3}/{d}: {ss} in {tus} us')
