.. -*- mode: rst -*-
..  To view this as a local file in browser, use `restview README.rst`
..  Browser page will update whenever a changed version is stored.

===================
Egyptian Fractions
===================

My egyptian-fractions repository contains programs and data files
listed below and at https://github.com/ghjwp7/egyptian-fractions
~ by James Waldby ~ Feb 2020, Nov 2023

These programs generate expansions of rational fractions into Egyptian
fraction representations, that is, as sums of unit fractions.  For
example, 5/9 = 1/2 + 1/18 = 1/3 + 1/6 + 1/18.

Useful references may include:
 https://en.wikipedia.org/wiki/Egyptian_fraction
 https://en.wikipedia.org/wiki/Greedy_algorithm_for_Egyptian_fractions
 https://en.wikipedia.org/wiki/Engel_expansion
 https://en.wikipedia.org/wiki/Practical_number#Practical_numbers_and_Egyptian_fractions

Project Contents:
------------------

Programs in this repository include `3terms.py, gterms.py, kterms.py,`
and `pracfracs.py`, as described below.  Data files with `n#d#k#` names
represent output from when kterms was run with specified integers as
parameters.  For example file `n13d79k4` contains output from
`./kterms.py 13 79 4`

--------------------------------------------------------------------
  
Program **pracfracs.py** uses "practical numbers" to find Egyptian
fraction representations.  More specifically, when given n, d, and
other parameters [described below, at end], it generates a series of
numbers that it uses as multipliers that let it readily form Egyptian
fraction representations of n/d.  Number m is practical if for any
j<m, some distinct divisors of m add up to j.  Thus, suppose u = m*d
is practical and that distinct divisors (d1, d2, d3, ...) of u add up
to m*n.  Then n/d = m*n/(m*d) = m*n/u = (d1+d2+d3+...)/u, hence d1/u +
d2/u + d3/u + ... is an Egyptian fraction for n/d, because the di are
distinct and each di/u reduces to a fraction with numerator 1.
pracfracs.py isn't exhaustive in its coverage, nor is it clear what it
would take to make it exhaustive.  (Note, for a lucid explanation of
important E-F methods, some using practical numbers, see PDF file
http://kevingong.com/Math/EgyptianFractions.pdf )

--------------------------------------------------------------------

Program **kterms.py** exhaustively computes expansions with up to kHi
terms.  The first three command-line parameters for this program are
n, d, and kHi.  Example: ./kterms.py 5 19 2 finds all the two-term
expansions of 5/19, outputting a line like "5/19: [[4, 76]] in 8 us".
Example: ./kterms.py 5 19 3 finds all the two- or three-term
expansions of 5/19, outputting a line like "5/19: [[4, 76], [5, 16,
1520], [5, 19, 95], [5, 20, 76], [6, 12, 76]] in 64 us".  Example:
./kterms.py 5 19 4 in about 44 ms finds 65 two-to-four term expansions
of 5/19.

kterms.py rapidly bogs down as d or kHi increase.  Some example
outputs illustrating this appear in files with names like n4d17k3,
n6d19k4, etc, that encode the n, d, and k values used as parameters.
For example, n13d1179 shows that kterms.py took 561815897 us (about
9.4 minutes) to find 76 3-term expansions of 13/1179.  In contrast,
pracfracs.py takes about 1 second to find 21 solutions, 4 seconds to
find 34 solutions, 16 seconds to find 40 solutions, 40 seconds to find
50 solutions, etc.

--------------------------------------------------------------------

Program **gterms.py** is like kterms, with differences as follows: (1)
uses gmpy mpz integers for calcs, (2) displays Engel series and
Fibonacci / greedy algorithm results, (3) if interrupted early,
displays up to ~10 solutions [vs ~6], and (4) displays solutions in
ascending order of sum of denominators.  See example outputs included
in comments at front of gterms.

--------------------------------------------------------------------

Program **3terms.py** exhaustively computes 1, 2, or 3-term expansions of
its input, printing denominator lists one set per line; eg, "2 18" and
"3 6 18".  Its execution time probably is quadratic, O(d*d) for input
n/d, as in essence it has one O(d) while loop nested within another.

--------------------------------------------------------------------

Parameters for pracfracs.py, as described in program comments:

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

--------------------------------------------------------------------

-30-
