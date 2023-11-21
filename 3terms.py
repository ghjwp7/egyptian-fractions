#!/usr/bin/env python3

# Re: 3-term expansions of a rational fraction less than 1, where the
# fraction is specified as two command-line parameters.  - jiw - 2020

# Example:     ./3terms.py  3 23
# will produce a list of Egyptian Fraction expansions of 3/23.
# Expansions with 1, 2, or 3 terms will be listed.  For example, the
# first line "8 184" corresponds to 1/8 + 1/184, which is equal to
# 3/23.


from sys import argv, exit
import time

# Get params:
arn = 0
arn+=1; n  = int(argv[arn]) if len(argv)>arn else 4
arn+=1; d  = int(argv[arn]) if len(argv)>arn else 17

def listTerms(n,d):
    n1, d1 = n, d               # (We should divide out gcd.  future.)

    # For fraction f = n/d, suppose t ~ 1/f and we want to use t as a
    # tight lower bound on denominators.  If 1/t > f, then t is not a
    # TLB, so we will increase it by 1, to cause 1/t <= f.
    t1 = d1//n1                 # t ~ 1/f = 1/(n/d) = d/n
    if n1*t1 < d1: t1 += 1      # Note, 1/t > n/d iff d > n*t.
    # While t1 is small enough that 3/t1 exceeds n/d = f ...
    while 3*d1 > n1*t1:
        # Subtract first term 1/t1 from f = n/d
        n2, d2 = n1*t1 - d1, d1*t1 # n2/d2 = n/d - 1/t = (n*t-d)/(d*t)
        if n2==0:                  # If n2/d2 = 0/d2 ...
            print (t1)             # Report expansion 1/t1 = f
            t1 += 1
            continue
        t2 = max(t1+1, d2//n2)  # Find lower bound on 2nd denominator
        if n2*t2 < d2: t2 += 1  # Make the bound tight
        # While t2 is small enough that 2/t2 exceeds n2/d2 = f-1/t1 ...
        while 2*d2 > n2*t2:     # while 2/t2 > n2/d2 ...
            n3, d3 = n2*t2 - d2, d2*t2 # n/d - 1/t = (n*t-d)/(d*t)
            if n3==0:           # If n3/d3 = 0/d3 ...
                print (t1, t2)  # Report expansion 1/t1 + 1/t2 = f
                t2 += 1
                continue
            # f - 1/t1 - 1/t2 = n3/d3, which is a unit fraction only
            # if n3 exactly divides d3.
            if d3%n3 == 0:       # Is remainder 0?
                t3 = d3//n3
                print (t1,t2,t3) # Report expansion 1/t1+1/t2+1/t3=f
            t2 += 1
        t1 += 1

t0 = time.time()
listTerms(n,d)
t1 = time.time()
print (f'Elapsed: {(t1-t0)*1e9 : 0.0f} nanoseconds')

