import sys, time

_range = xrange if sys.version_info.major == 2 else range
_timefn = time.time if not sys.platform == 'win32' else time.clock

class Timeit(object):
    
    def __init__(self):
        self.average = 0.0
        self.mean = 0.0
        self.min = 0.0
        self.max = 0.0
        
    def run(self, count, func, *args):
        
        times = []
        result = None
        for i in _range(count):
            tstart = _timefn()
            
            result = func(*args)
            
            tend = _timefn()
            times.append( tend - tstart )
        
        times.sort()
        self.average = sum( times ) / float(count)
        middle = count//2
        if count & 1:
            self.mean = times[middle]
        else:
            self.mean = (times[middle-0] + times[middle]) / 2.0
        self.min = times[0]
        self.max = times[-1]
        
        return result
            
            