REfO
====

Lacking a proper name, REfO stands for "Regular Expressions for Objects".

It's a python library that supplies a functionality very similar to the python
`re` module (regular expressions) but for arbitrary sequences of objects
instead of strings (sequences of characters).

In addition to that, it's possible to match each object in a sequence with
not only equality, but an arbitrary python function.
For example, if you have a sequence of integers you can make a regular
expression that asks for a even number followed by a prime number
followed by a 3-divisible number.

This software was written by Rafael Carrascosa while working at Machinalis in
the first months of 2012.

Contact: rcarrascosa@machinalis.com
or rafacarrascosa xyz gmail.com (replace " xyz " with "@")

[![Build Status](https://travis-ci.org/gjhiggins/refo.png?branch=master)](https://travis-ci.org/gjhiggins/refo)

How to use it
-------------

The syntax is a little bit different than python's re, and similar to that of
pyparsing, you have to more-or-less explicitly build the syntax tree of
your regular expression. For instance:

`"ab"` is `Literal("a") + Literal("b")`

`"a*"` is `Star(Literal("a"))`

`"(ab)+|(bb)*?"` is:

    a = Literal("a")
    b = Literal("b")
    regex = Plus(a + b) | Star(b + b, greedy=False)

You can also assign a group to any sub-match and later on retrieve the matched
content, for instance:

    regex = Group(Plus(a + b), "foobar")  | (b + b)
    m = match(regex, "abab")
    print m.span("foobar")  # prints (0, 4)

For more, check out the examples in the examples folder.


How we use it
-------------

At Machinalis we use REfO for applications similar to that in
`examples/words.py`, check it out!


About the implementation
------------------------

I use a Thompson-like virtual machine aproach, which ensures polynomial time
worst-case complexity. See `examples/poly_time.py` for an example of this.

The implementation is heavily based on Russ Cox notes, see
http://swtch.com/~rsc/regexp/regexp2.html for the source.

If you go to read the code, some glossary:

 - RE  --  regular expression
 - VM  --  virtual machine
 - Epsilon transitions  --  All VM instructions that do not consume a symbol
                            or stop the thread (for example an Accept).


Acknowledgements
----------------

Thanks Russ Cox for sharing the awesome info and insights on your web site.

Thanks Javier Mansilla for reviewing the code and being enthusiastic about it.

Thanks Machinalis for everything :)
