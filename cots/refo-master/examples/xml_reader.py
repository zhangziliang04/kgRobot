#!/usr/bin/python

# This script opens an xml file and prints its document tree... sort of.
# This example uses refo syntax to simple express an otherwise more-or-less
# complicated regular expression.

import argparse
parser = argparse.ArgumentParser(description="Prints an xml document tree" +
                                             "... sort of.")
parser.add_argument("filename", action="store")
cfg = parser.parse_args()
text = open(cfg.filename).read()


from refo import finditer, Predicate, Literal, Any, Group, Star


def notin(xs):
    return lambda x: x not in xs


name = Predicate(notin("/")) + Star(Predicate(notin(" >")))
name = Group(name, "name")
inside = name + Star(Any(), greedy=False)
opentag = Literal("<") + inside + Literal(">")
opentag = Group(opentag, "open")
closetag = Literal("<") + Literal("/") + inside + Literal(">")
closetag = Group(closetag, "close")
regex = closetag | opentag

depth = 0
for m in finditer(regex, text):
    if "open" in m:
        i, j = m["name"]
        print "  " * depth + text[i:j]
        depth += 1
    else:
        assert "close" in m
        depth -= 1
