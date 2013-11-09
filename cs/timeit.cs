using System;
using System.Linq;
using System.Diagnostics;
using System.Collections.Generic;

public class Timeit
{
    public double Average;
    public double Mean;
    public double Min;
    public double Max;

    public TResult Run<TResult>(ulong count, Func<TResult> func, params object[] args) {
        return RunInternal<TResult>(count, func, args);
    }
    public TResult Run<T1,TResult>(ulong count, Func<T1,TResult> func, params object[] args) {
        return RunInternal<TResult>(count, func, args);
    }
    public TResult Run<T1,T2,TResult>(ulong count, Func<T1,T2,TResult> func, params object[] args) {
        return RunInternal<TResult>(count, func, args);
    }

    private TResult RunInternal<TResult>(ulong count, Delegate func, params object[] args)
    {
        TimeSpan[] times = new TimeSpan[count];
        
        TResult result = default(TResult);
        for(ulong i = 0; i < count; ++i)
        {
            Stopwatch watch = new Stopwatch();
            watch.Start();
            
            result = (TResult)func.DynamicInvoke(args);
            
            watch.Stop();
            
            times[i] = watch.Elapsed;
        }
        
        Array.Sort(times);
        long averageTicks = Convert.ToInt64(times.Average(timeSpan => timeSpan.Ticks));
        TimeSpan average = new TimeSpan(averageTicks);
        Average = average.TotalSeconds;
        
        ulong middle = count / 2;
        if( (count & 1) == 1 )
            Mean = times[middle].TotalSeconds;
        else
            Mean = new TimeSpan((times[middle-1].Ticks + times[middle].Ticks) / 2).TotalSeconds;
        
        Min = times[0].TotalSeconds;
        Max = times[count-1].TotalSeconds;
        
        return result;
    }
    

}