#  Copyright (c) 2012, Machinalis S.R.L.
#
#  Author: Rafael Carrascosa <rcarrascosa@machinalis.com>
#
#  This file is part of REfO and is distributed under the Modified BSD License.
#  You should have received a copy of license in the LICENSE.txt file.

from .virtualmachine import VirtualMachine
from .patterns import Pattern, Any, Star, Group, _start, _end


class Match(object):
    """
    Non-opaque class used to return RE match information.
    Matching soubgroup key `None` is reserved for the matching of the whole
    string.
    """
    def __init__(self, state=None):
        self.state = state

    def span(self, key=None):
        return self[key]

    def start(self, key=None):
        return self[key][0]

    def end(self, key=None):
        return self[key][1]

    def group(self, key=None):
        return self[key]

    def __getitem__(self, key):
        try:
            return self.state[_start(key)], self.state[_end(key)]
        except KeyError:
            raise KeyError(key)

    def __contains__(self, key):
        return _start(key) in self.state

    def offset(self, amount):
        assert "path" not in self.state
        self.state = dict((key, i + amount) for key, i in self.state.items())

    def get_path(self):
        return self.state["path"]

    def __iter__(self):
        for key in set(x[0] for x in self.state):
            yield key


def _match(pattern, iterable, keep_path=False):
    assert isinstance(pattern, Pattern)
    code = pattern.compile()
    vm = VirtualMachine(code, keep_path)
    m = Match()
    # Start VM
    vm.do_epsilon_transitions()
    m.state = vm.accepting_state(None)
    vm.cutoff()
    for x in iterable:
        if not vm.is_alive():
            break
        vm.feed(x)
        vm.do_epsilon_transitions()
        m.state = vm.accepting_state(m.state)
        vm.cutoff()
    if m.state is None:
        return None
    return m


def match(pattern, iterable, keep_path=False):
    pattern = Group(pattern, None)
    return _match(pattern, iterable, keep_path)


def search(pattern, iterable):
    assert isinstance(pattern, Pattern)
    pattern = Star(Any(), greedy=False) + Group(pattern, None)
    return _match(pattern, iterable)


def finditer_lame(pattern, sequence):
    """
    The lame implementation
    """
    offset = 0
    while offset <= len(sequence):
        it = (sequence[i] for i in range(offset, len(sequence)))
        m = search(pattern, it)
        if m is None:
            break
        m.offset(offset)
        yield m
        i, offset = m.span()
        if i == offset:
            offset += 1


def finditer_alt(pattern, iterable):
    """
    An experimental implementation of finditer.
    The idea here is to make an implementation that is able to work with any
    iterator, not necessariry the indexable ones.
    This implies (among other things) that each element is feeded only once and
    then discarded.
    """
    assert isinstance(pattern, Pattern)
    pattern = Star(Star(Any(), greedy=False) + Group(pattern, None))
    code = pattern.compile()
    vm = VirtualMachine(code)
    m = Match()
    new = Match()
    # Start VM
    vm.do_epsilon_transitions()
    vm.cutoff()
    for x in iterable:
        if not vm.is_alive():
            break
        vm.feed(x)
        vm.do_epsilon_transitions()
        new.state = vm.accepting_state(None)
        if new.state is not None:
            if m.state is None:
                m.state = new.state
            elif m.start() == new.start() and m.end() < new.end():
                m.state = new.state
            elif m.start() != new.start():
                yield m
                m = new
                new = Match()
        vm.cutoff()
    if m.state is not None:
        yield m


finditer = finditer_lame
