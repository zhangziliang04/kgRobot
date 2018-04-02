#!/usr/bin/python


from refo import Literal, Question, match
import re
import time

# This regular expression is known to kill the python re module
# because it exploits the fact that the implementation has exponential
# worst case complexity.
# Instead, this implementation has polinomial worst case complexity,
# and therefore this test should finish in a reasonable time.

# You might want to try with N = 20, 30, 40, 100 to see what happens
N = 30

a = Literal("a")
string = "a" * N
regex = Question(a) * N + a * N
start = time.time()
m = match(regex, string)
end = time.time()
print "Refo finished in {0:.2} seconds".format(end - start)

regex = "(:?a?){{{0}}}a{{{0}}}".format(N)
print "Trying", regex
regex = re.compile(regex)
start = time.time()
regex.match(string)
end = time.time()
print "Python re finished in {0:.2} seconds".format(end - start)
