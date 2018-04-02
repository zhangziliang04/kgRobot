#  Copyright (c) 2012, Machinalis S.R.L.
#
#  Author: Rafael Carrascosa <rcarrascosa@machinalis.com>
#
#  This file is part of REfO and is distributed under the Modified BSD License.
#  You should have received a copy of license in the LICENSE.txt file.

import unittest
import refo
from refo.match import Match, match as refomatch
import re
import math


def isprime(x):
    if x < 2:
        return False
    top = int(math.sqrt(x))
    for i in xrange(2, top + 1):
        if x % i == 0:
            return False
    return True


def _seq2str(seq):
    xs = []
    for x in seq:
        if isprime(x):
            xs.append("a")
        else:
            xs.append("b")
    return "".join(xs)


def path_function(x):
    def f(xs):
        if x in xs:
            return x * x
        return None
    return f


class TestRefoModule(unittest.TestCase):
    seq = xrange(10000)
    a = refo.Predicate(isprime)
    b = refo.Predicate(lambda x: not isprime(x))
    x = refo.Predicate(path_function(1))
    y = refo.Predicate(path_function(2))
    z = refo.Predicate(path_function(3))
    string = _seq2str(seq)

    def _eq_span_n_stuff(self, m, strm):
        assert (m and strm) or (not m and not strm)
        self.assertNotEqual(m, None)
        self.assertNotEqual(strm, None)
        self.assertEqual(m.span(), strm.span())

    def _eq_list_n_stuff(self, xs, strxs):
        xs = [x.span() for x in xs]
        strxs = [x.span() for x in strxs]
        self.assert_(xs == strxs)

    def test_match1(self):
        regexptn = self.b + self.b + self.a + self.a + self.b
        strregex = re.compile("bbaab")
        m = refomatch(regexptn, self.seq)
        strm = strregex.match(self.string)
        self._eq_span_n_stuff(m, strm)

    def test_match2(self):
        # This regular expression is known to kill the python re module
        # because it exploits the fact that the implementation has exponential
        # worst case complexity.
        # Instead, this implementation has polinomial worst case complexity,
        # and therefore this test should finish in a reasonable time.
        N = 100
        a = refo.Literal("a")
        strg = "a" * N
        regexptn = refo.Question(a) * N + a * N
        m = refomatch(regexptn, strg)
        self.assertNotEqual(m, None)

    def test_search1(self):
        regexptn = self.a + self.b + self.b + self.b + self.a
        strregex = re.compile("abbba")
        m = refo.search(regexptn, self.seq)
        strm = strregex.search(self.string)
        self._eq_span_n_stuff(m, strm)

    def test_search2(self):
        tab = self.a + self.b + self.a
        regexptn = tab + self.b * 3 + tab
        strregex = re.compile("ababbbaba")
        m = refo.search(regexptn, self.seq)
        strm = strregex.search(self.string)
        self._eq_span_n_stuff(m, strm)

    def test_search3(self):
        tab = self.a + self.b
        regexptn = tab + tab + refo.Plus(self.b)
        strregex = re.compile("ababb+")
        m = refo.search(regexptn, self.seq)
        strm = strregex.search(self.string)
        self._eq_span_n_stuff(m, strm)

    def test_search4(self):
        tab = self.a + self.b
        regexptn = tab * 2 + refo.Plus(self.b, greedy=False)
        strregex = re.compile("ababb+?")
        m = refo.search(regexptn, self.seq)
        strm = strregex.search(self.string)
        self._eq_span_n_stuff(m, strm)

    def test_search5(self):
        tab = self.a + self.b
        regexptn = tab * (2, 5)
        strregex = re.compile("(?:ab){2,5}")
        m = refo.search(regexptn, self.seq)
        strm = strregex.search(self.string)
        self._eq_span_n_stuff(m, strm)

    def test_finditer1(self):
        tab = self.a + self.b
        regexptn = tab * (2, None)
        strregex = re.compile("(?:ab){2,}")
        xs = list(refo.finditer(regexptn, self.seq))
        strxs = list(strregex.finditer(self.string))
        self._eq_list_n_stuff(xs, strxs)

    def test_finditer2(self):
        tab = self.a + self.b
        regexptn = tab * (2, None) + refo.Group(refo.Plus(self.b), "foobar")
        strregex = re.compile("(?:ab){2,}(b+)")
        xs = list(refo.finditer(regexptn, self.seq))
        strxs = list(strregex.finditer(self.string))
        xs = [x.group("foobar") for x in xs]
        strxs = [x.span(1) for x in strxs]
        self.assert_(xs == strxs)

    def test_match_path(self):
        seq = [[1, 2],     # x and y
               [1],        # x
               [1, 2, 3],  # x, y and z
               [1, 2],     # x and y
               [2, 3],     # y and z
               [0, 4, 5],
               []]
        regexptn = refo.Star(self.y) + refo.Plus(self.x + self.z)
        m = refomatch(regexptn, seq, keep_path=True)
        self.assert_(isinstance(m, Match))
        path = m.get_path()
        self.assertEqual([4, 1, 9, 1, 9], path)


if __name__ == "__main__":
    unittest.main()
