using System;
using System.Threading;
using System.Globalization;
using Mono.Math;

public class Program
{
    static BigInteger Fibonacci(ulong n)
    {
        if( n <= 1 )
            return n;
    
        return Fibonacci(n - 2) + Fibonacci(n - 1);
    }

    public static void Main(string[] args)
    {
        Thread.CurrentThread.CurrentCulture = new CultureInfo("en-US");
        
        ulong iterations = args.Length > 0 ? Convert.ToUInt64(args[0]) : 100;
        ulong n = args.Length > 1 ? Convert.ToUInt64(args[1]) : 10;

        Timeit timeit = new Timeit();
        BigInteger result = timeit.Run<ulong, BigInteger>(iterations, Fibonacci, n);

        Reporter.write_result(Console.OpenStandardOutput(),
                                String.Format("Fibonacci (recursive) n = {0}", n),
                                iterations,
                                timeit.Average,
                                timeit.Mean,
                                timeit.Min,
                                timeit.Max,
                                String.Format("{0}", result) );
    }
}
