import sys
from timeit import Timeit
import reporter


def Factorial(n):
    if n == 1:
        return 1
    return Factorial(n - 1) * n


iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 100
n = int(sys.argv[2]) if len(sys.argv) > 2 else 40

timeit = Timeit()

result = timeit.run(iterations, Factorial, n)

reporter.write_result(sys.stdout,
                      "Factorial (recursive) n = %d" % n,
                      iterations,
                      timeit.average,
                      timeit.mean,
                      timeit.min,
                      timeit.max,
                      str(result))
