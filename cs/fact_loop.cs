using System;
using System.Threading;
using System.Globalization;
using Mono.Math;

public class Program
{
    static BigInteger Factorial(ulong n)
    {
        BigInteger factorial = 1;
        for(ulong i = 1; i <= n; i++)
        {
            factorial *= i;
        }
        return factorial;
    }

    public static void Main(string[] args)
    {
        Thread.CurrentThread.CurrentCulture = new CultureInfo("en-US");

        ulong iterations = args.Length > 0 ? Convert.ToUInt64(args[0]) : 100;
        ulong n = args.Length > 1 ? Convert.ToUInt64(args[1]) : 40;

        Timeit timeit = new Timeit();
        BigInteger result = timeit.Run<ulong, BigInteger>(iterations, Factorial, n);

        Reporter.write_result(Console.OpenStandardOutput(),
                                String.Format("Factorial (loop) n = {0}", n),
                                iterations,
                                timeit.Average,
                                timeit.Mean,
                                timeit.Min,
                                timeit.Max,
                                String.Format("{0}", result) );
    }
}
