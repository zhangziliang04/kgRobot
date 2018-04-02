#  Copyright (c) 2012, Machinalis S.R.L.
#
#  Author: Rafael Carrascosa <rcarrascosa@machinalis.com>
#
#  This file is part of REfO and is distributed under the Modified BSD License.
#  You should have received a copy of license in the LICENSE.txt file.


class Instruction(object):
    """
    Non-opaque class to represent RE VM instructions.
    Instructions join among themselves to form code (a program).
    Instructions are joined like a linked list usign the `succ` and `split`
    attributes, thus forming a directed graph.
    """


class Atom(Instruction):
    def __init__(self, comparison_function, succ=None):
        self.comparison_function = comparison_function
        if succ is not None:
            self.succ = succ

    def __repr__(self):
        return "Atom({0})".format(repr(self.comparison_function))


class Accept(Instruction):
    succ = None

    def __repr__(self):
        return "Accept"


class Split(Instruction):
    def __init__(self, s1=None, s2=None):
        if s1 is not None:
            self.succ = s1
        if s2 is not None:
            self.split = s2

    def __repr__(self):
        return "Split({0}, {1})".format(repr(self.succ), repr(self.split))


class Save(Instruction):
    def __init__(self, record, succ=None):
        self.record = record
        if succ is not None:
            self.succ = succ

    def __repr__(self):
        return "Save({0})".format(repr(self.record))
