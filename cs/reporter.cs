using System;
using System.IO;
using System.Json;
using System.Web;
using System.Web.Script.Serialization;

public class Reporter
{
    public static void write_result(
                Stream stream,
                String title,
                ulong iterations,
                double time_avg,
                double time_mean,
                double time_min,
                double time_max,
                String result )
    {
        /*
        JsonObject obj = new JsonObject();
        obj.Add( "title", title );
        obj.Add( "iterations", iterations );
        obj.Add( "time_avg", time_avg );
        obj.Add( "time_mean", time_mean );
        obj.Add( "time_min", time_min );
        obj.Add( "time_max", time_max );
        obj.Add( "result", result );
        */
        
        StreamWriter sw = new StreamWriter(stream);
        JavaScriptSerializer serializer = new JavaScriptSerializer();
        var json = serializer.Serialize(new {
                                            title = title,
                                            iterations = iterations,
                                            time_avg = time_avg,
                                            time_mean = time_mean,
                                            time_min = time_min,
                                            time_max = time_max,
                                            result = result
                                        });
        
        sw.Write(json);
        sw.Write("\n");
        sw.Flush();
    }
}