#  Copyright (c) 2012, Machinalis S.R.L.
#
#  Author: Rafael Carrascosa <rcarrascosa@machinalis.com>
#
#  This file is part of REfO and is distributed under the Modified BSD License.
#  You should have received a copy of license in the LICENSE.txt file.


from refo import finditer, Predicate, Plus

import re
import copy

# This example demonstrates the purpose for which I felt the need to create
# the refo library.
# This code is a mocked-down version of a production code we are using at
# Machinalis.
#
# The problem:
# We would like to have a linguist writting down rules to seek errors (perhaps
# fix them too) in natural language sentences (written human language, for
# example english) and we would like she to do so in a linguist-friendly
# format, ie: Not having to be able to program software to do so.
#
# Assumptions:
# A natural language sentence is a sequence of words, each word having a token,
# and a part-of-speech tag (pos).
#
# What we did:


class Word(object):
    def __init__(self, token, pos):
    
        self.token = token
        #ДЪад
        self.pos = pos


class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            if "victim" in m:
                i, j = m.span("victim")
            self.action(sentence[i:j])


def capitalize_name(x):
    for nnp in x:
        print "Capitalizing"
        nnp.token = nnp.token.capitalize()


def feet_to_mt(x):
    number, units = x
    mt = float(number.token) * 0.3048
    number.token = "{0:.2}".format(mt)
    units.token = "mt."
    units.pos = "UNITS_METERS"


rules = [

    Rule(condition=W(pos="NUMBER") + W(pos="UNITS_FEET"),
         action=feet_to_mt),

    Rule(condition=Plus(W(token="[^A-Z].*", pos="NNP")),
         action=capitalize_name),

]

sentence = "My|PRP friend|NN john|NNP smith|NNP is|VBZ 2|NUMBER " +\
           "feet|UNITS_FEET taller|JJR than|IN mary|NNP Jane|NNP"

sentence = [Word(*x.split("|")) for x in sentence.split()]
original = copy.deepcopy(sentence)

for rule in rules:
    rule.apply(sentence)

print "From: " + " ".join((w.token for w in original))
print "To:   " + " ".join((w.token for w in sentence))
