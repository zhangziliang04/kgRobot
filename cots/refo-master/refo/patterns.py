#  Copyright (c) 2012, Machinalis S.R.L.
#
#  Author: Rafael Carrascosa <rcarrascosa@machinalis.com>
#
#  This file is part of REfO and is distributed under the Modified BSD License.
#  You should have received a copy of license in the LICENSE.txt file.

from .instructions import Atom, Accept, Split, Save


class Pattern(object):
    def _compile(self):
        raise NotImplementedError

    def compile(self):
        return self._compile(Accept())

    def __or__(self, other):
        return Disjunction(self, other)

    def __add__(self, other):
        xs = []
        for item in [self, other]:
            if isinstance(item, Concatenation):
                xs.extend(item.xs)
            else:
                xs.append(item)
        return Concatenation(*xs)

    def __mul__(self, x):
        if isinstance(x, int):
            mn = x
            mx = x
        else:
            assert isinstance(x, tuple)
            mn, mx = x
            if mn is None:
                mn = 0
        return Repetition(self, mn=mn, mx=mx)

    def __str__(self):
        return str(self.arg)

    def __repr__(self):
        return "{1}({0!r})".format(self.arg, self.__class__.__name__)


class Predicate(Pattern):
    def __init__(self, f):
        self.f = f
        self.arg = f

    def _compile(self, cont):
        x = Atom(self.f, succ=cont)
        return x


class Any(Predicate):
    def __init__(self):
        super(Any, self).__init__(lambda x: True)

    def __str__(self):
        return "Any()"

    def __repr__(self):
        return "Any()"


class Literal(Predicate):
    def __init__(self, x):
        super(Literal, self).__init__(lambda y: x == y)
        self.x = x
        self.arg = x


class Disjunction(Pattern):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def _compile(self, cont):
        a = self.a._compile(cont)
        b = self.b._compile(cont)
        return Split(a, b)

    def __str__(self):
        return "(" + " | ".join(map(str, [self.a, self.b])) + ")"

    def __repr__(self):
        return "(" + " | ".join(map(repr, [self.a, self.b])) + ")"


class Concatenation(Pattern):
    def __init__(self, *patterns):
        self.xs = list(patterns)
        assert len(self.xs) != 0

    def _compile(self, cont):
        code = cont
        for x in reversed(self.xs):
            code = x._compile(code)
        return code

    def __str__(self):
        return "(" + " + ".join(map(str, self.xs)) + ")"

    def __repr__(self):
        return "(" + " + ".join(map(repr, self.xs)) + ")"


class Star(Pattern):
    def __init__(self, pattern, greedy=True):
        self.x = pattern
        self.greedy = greedy
        self.arg = pattern

    def _compile(self, cont):
        # In words: split to (`x` and return to split) and `cont`
        split = Split()
        x = self.x._compile(split)
        if self.greedy:
            split.succ = x
            split.split = cont
        else:
            split.succ = cont
            split.split = x
        # `Plus` would return `x`
        return split

    def __str__(self):
        return str(self.x) + "*"


class Plus(Pattern):
    def __init__(self, pattern, greedy=True):
        self.x = pattern
        self.greedy = greedy
        self.arg = pattern

    def _compile(self, cont):
        # In words: take `x` and split to `x` and `cont`
        split = Split()
        x = self.x._compile(split)
        if self.greedy:
            split.succ = x
            split.split = cont
        else:
            split.succ = cont
            split.split = x
        # `Star` would return `split`
        return x

    def __str__(self):
        return str(self.x) + "+"


class Question(Pattern):
    def __init__(self, pattern, greedy=True):
        self.x = pattern
        self.greedy = greedy
        self.arg = pattern

    def _compile(self, cont):
        xcode = self.x._compile(cont)
        if self.greedy:
            return Split(xcode, cont)
        else:
            return Split(cont, xcode)

    def __str__(self):
        return str(self.x) + "?"


class Group(Pattern):
    def __init__(self, pattern, key):
        self.x = pattern
        self.key = key

    def _compile(self, cont):
        start = Save(_start(self.key))
        end = Save(_end(self.key))
        code = self.x._compile(end)
        start.succ = code
        end.succ = cont
        return start

    def __str__(self):
        return "Group({0!s}, {1!s})".format(self.x, self.key)

    def __repr__(self):
        return "Group({0!r}, {1!r})".format(self.x, self.key)


class Repetition(Pattern):
    def __init__(self, pattern, mn=0, mx=None, greedy=True):
        assert mn is not None or mx is not None or mn <= mx
        self.x = pattern
        self.mn = mn
        self.mx = mx
        self.greedy = greedy

    def _compile(self, cont):
        code = cont
        if self.mx is not None:
            q = Question(self.x, self.greedy)
            for _ in range(self.mx - self.mn):
                code = q._compile(code)
        else:
            code = Star(self.x, greedy=self.greedy)._compile(code)
        for _ in range(self.mn):
            code = self.x._compile(code)
        return code

    def __str__(self):
        return self._tostring("{0!s}")

    def __repr__(self):
        return self._tostring("{0!r}")

    def _tostring(self, s):
        base = "(" + s + ")*"
        if self.mn == 0 and self.mx is None:
            return base.format(self.x)
        if self.mn == self.mx:
            return (base + "{1}").format(self.x, self.mn)
        return (base + "*({1},{2})").format(self.x, self.mn, self.mx)


def _start(key):
    return (key, 0)


def _end(key):
    return (key, 1)
