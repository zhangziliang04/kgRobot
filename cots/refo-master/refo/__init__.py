#  Copyright (c) 2012, Machinalis S.R.L.
#
#  Author: Rafael Carrascosa <rcarrascosa@machinalis.com>
#
#  This file is part of REfO and is distributed under the Modified BSD License.
#  You should have received a copy of license in the LICENSE.txt file.

from .match import match, search, finditer
from .patterns import (
    Predicate, Any, Literal, Disjunction, Concatenation,
    Star, Plus, Question, Group, Repetition
)
# tedious means of satisfying flake8
assert match
assert search
assert finditer
assert Predicate
assert Any
assert Literal
assert Disjunction
assert Concatenation
assert Star
assert Plus
assert Question
assert Group
assert Repetition
