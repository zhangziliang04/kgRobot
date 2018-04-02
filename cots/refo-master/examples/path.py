import refo


def path_function(x):
    def f(xs):
        if x in xs:
            return x * x
        return None
    return f


x = refo.Predicate(path_function(1))
y = refo.Predicate(path_function(2))
z = refo.Predicate(path_function(3))

seq = [[1, 2],     # x and y
       [1],        # x
       [1, 2, 3],  # x, y and z
       [3],        # z
       [0, 4, 5],
       []]


regex = refo.Star(y) + refo.Plus(x + z)
m = refo.match(regex, seq, keep_path=True)
print m.get_path()
