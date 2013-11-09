import sys
from timeit import Timeit
import reporter


def Fibonacci(n):
    if n <= 1:
        return n
    return Fibonacci(n - 1) + Fibonacci(n - 2)


iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 100
n = int(sys.argv[2]) if len(sys.argv) > 2 else 10

timeit = Timeit()

result = timeit.run(iterations, Fibonacci, n)

reporter.write_result(sys.stdout,
                      "Fibonacci (loop) n = %d" % n,
                      iterations,
                      timeit.average,
                      timeit.mean,
                      timeit.min,
                      timeit.max,
                      str(result))
