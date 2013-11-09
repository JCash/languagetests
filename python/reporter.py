import json
from json import encoder

from collections import OrderedDict

def write_result(stream,
                 title,
                 iterations,
                 time_avg,
                 time_mean,
                 time_min,
                 time_max,
                 result):
    original_float_repr = encoder.FLOAT_REPR
    encoder.FLOAT_REPR = lambda o: format(o, '.12f')

    try:
        obj = OrderedDict()
        obj["title"]        = title
        obj["iterations"]   = iterations
        obj["time_avg"]     = time_avg
        obj["time_mean"]    = time_mean
        obj["time_min"]     = time_min
        obj["time_max"]     = time_max
        obj["result"]       = result
        s = json.dumps(obj, indent=4)
        stream.write(s)
    except:    
        encoder.FLOAT_REPR = original_float_repr
        raise
