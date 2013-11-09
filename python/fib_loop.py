import sys
from timeit import Timeit
import reporter

_range = xrange if sys.version_info.major == 2 else range


def Fibonacci(n):
    a = 0
    b = 1
    c = 0
    i = 1
    while i <= n:
        c = a + b
        a = b
        b = c
        i += 1
    return a

iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 100
n = int(sys.argv[2]) if len(sys.argv) > 2 else 10

timeit = Timeit()

result = timeit.run(iterations, Fibonacci, n)

reporter.write_result(sys.stdout,
                      "Fibonacci (recursive) n = %d" % n,
                      iterations,
                      timeit.average,
                      timeit.mean,
                      timeit.min,
                      timeit.max,
                      str(result))
