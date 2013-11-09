#! /usr/bin/python

import sys
import os
from collections import OrderedDict
import subprocess
import json

NUMITERATIONS=1000
PLATFORM=None
if sys.platform == 'darwin':
    PLATFORM='Darwin'
elif sys.platform == 'linux2':
    PLATFORM='Linux'
elif sys.platform == 'win32':
    PLATFORM='Windows'
BUILDDIR=os.path.abspath(os.path.join('build', PLATFORM))

CSHARPINTERPRETER='mono '
if sys.platform == 'win32':
    CSHARPINTERPRETER=''

# If set to true, the output from the actual runs are printed out to the stdout
NOPRESENT='-v' in sys.argv


class Test(object):
    def __init__(self, lang, runstr):
        self.lang = lang
        self.runstr = runstr
        self.results = []
        
    def run(self, kwargs):
        args = ' '.join(map(str, kwargs.itervalues()))
        
        runstr = self.runstr
        runstr += " %d %s" % (NUMITERATIONS, args)
        
        if not NOPRESENT:
            runstr += " > %s/tmp.json" % BUILDDIR
        
        runstr = os.path.expandvars(runstr)
        os.system(runstr)
        
        if not NOPRESENT:
            with open(BUILDDIR+"/tmp.json") as f:
                result = json.loads(f.read())
            
            self.results.append(result)


tests = OrderedDict()

tests['Factorial (recursive)'] = (  [OrderedDict([('n',40)]), OrderedDict([('n',100)]), OrderedDict([('n',200)]), OrderedDict([('n',400)]), OrderedDict([('n',600)]), OrderedDict([('n',800)]) ],
                                    [ Test('C++', BUILDDIR+'/fact_recursive'),
                                       Test('Python 2', 'python python/fact_recursive.py'),
                                       Test('Python 3', 'python3 python/fact_recursive.py'),
                                       Test('C#', CSHARPINTERPRETER + BUILDDIR+'/fact_recursive.exe')] )

tests['Factorial (loop)'] = ( [OrderedDict([('n',40)]), OrderedDict([('n',100)]), OrderedDict([('n',200)]), OrderedDict([('n',400)]), OrderedDict([('n',600)]), OrderedDict([('n',800)]) ],
                                [Test('C++', BUILDDIR+'/fact_loop'),
                                  Test('Python 2', 'python python/fact_loop.py'),
                                  Test('Python 3', 'python3 python/fact_loop.py'),
                                  Test('C#', CSHARPINTERPRETER + BUILDDIR+'/fact_loop.exe')] )

tests['Fibonacci (recursive)'] = (  [OrderedDict([('n',4)]), OrderedDict([('n',8)]), OrderedDict([('n',12)]), OrderedDict([('n',16)]), OrderedDict([('n',20)]) ],
                                    [ Test('C++', BUILDDIR+'/fib_recursive'),
                                      Test('Python 2', 'python python/fib_recursive.py'),
                                      Test('Python 3', 'python3 python/fib_recursive.py'),
                                      Test('C#', CSHARPINTERPRETER + BUILDDIR+'/fib_recursive.exe')
                                    ])

tests['Fibonacci (loop)'] = (  [OrderedDict([('n',25)]), OrderedDict([('n',50)]), OrderedDict([('n',75)]), OrderedDict([('n',100)]), OrderedDict([('n',250)]), OrderedDict([('n',500)]) ],
                                    [ Test('C++', BUILDDIR+'/fib_loop'),
                                      Test('Python 2', 'python python/fib_loop.py'),
                                      Test('Python 3', 'python3 python/fib_loop.py'),
                                      Test('C#', CSHARPINTERPRETER + BUILDDIR+'/fib_loop.exe')
                                    ])


def find_time_unit(t):
    if t < 0.000001:
        return 'ns'
    if t < 0.001:
        return '\xb5s'
    if t < 0.1:
        return 'ms'
    return 's'

def convert_time(t, unit):
    if unit == 'ns':
        return t * 1000000000.0
    if unit == '\xb5s':
        return t * 1000000.0
    if unit == 'ms':
        return t * 1000.0
    return t

def get_average_time(tests):
    t = sum([test.results[-1]['time_avg'] for test in tests])
    return t / len(tests)

def present(groupname, args, tests):
    timeunit = find_time_unit(get_average_time(tests))
    args = '(' + ','.join(['%s = %s' % (k, v) for k, v in args.iteritems()]) + ')'
    
    print groupname, args
    for test in tests:
        print test.lang.ljust(14), 'average', convert_time(test.results[-1]['time_avg'], timeunit), timeunit
    print ""

def present_csv(stream, groupname, argslst, tests):
    timeunit = find_time_unit(get_average_time(tests))
    
    separator = ';'
    
    print >>stream, "%s (time in %s)" % (groupname, timeunit)
    
    # write the headers of the columns
    stringargslist = []
    for args in argslst:
        stringargslist.append( ','.join(['%s = %s' % (k, v) for k, v in args.iteritems()]))
    print >>stream, "(language, arguments)" + separator + separator.join(stringargslist) 
    
    # write the results of the tests
    for test in tests:
        print >>stream, "%s" % test.lang + separator + separator.join(["%.12f" % convert_time(result['time_avg'], timeunit) for result in test.results]) 


def present_html(stream, groupname, argslst, tests):
    
    html = """
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart%(FUNCTIONTITLE)s);
      function drawChart%(FUNCTIONTITLE)s() {
        var data = google.visualization.arrayToDataTable(
            %(TABLEDATA)s
        );

        var options = {
          title: '%(TITLE)s',
          hAxis: {title: '%(HAXIS_TITLE)s'},
          vAxis: {title: '%(VAXIS_TITLE)s'},
          is3D: true,
          backgroundColor: {
            'fill': '#F4F4F4',
            'strokeWidth': 1,
            'opacity': 100
             },
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div_%(FUNCTIONTITLE)s'));
        chart.draw(data, options);
      }
    </script>
    """
    
    timeunit = find_time_unit(get_average_time(tests))
    
    info = dict()
    info['TITLE'] = groupname
    info['FUNCTIONTITLE'] = ''.join([x for x in groupname if str.isalpha(x)])
    info['VAXIS_TITLE'] = 'Unit: ' + timeunit
    info['HAXIS_TITLE'] = 'Args'
    info['TABLEDATA'] = ''
    
    headers = ['Args']
    for args in argslst:
        headers.append( ','.join(['%s = %s' % (k, v) for k, v in args.iteritems()]))
    
    info['TABLEDATA'] = [headers]
    
    
    for test in tests:
        langinfo = [test.lang] + [convert_time(result['time_avg'], timeunit) for result in test.results]
        info['TABLEDATA'].append(langinfo) 

    # transpose the data
    info['TABLEDATA'] = zip(*info['TABLEDATA'])
    info['TABLEDATA'] = map(list, info['TABLEDATA'])
    
    print >>stream, html % info

def present_html_header(stream, alltests):
    
    html = """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script>
        function toggle_visibility(id) {
            var e = document.getElementById(id);
            if(e.style.display == 'none')
                e.style.display = 'block';
            else
                e.style.display = 'none';
        }
    </script>
      """
    print >>stream, html

def present_html_footer(stream, alltests):
    html1 = """
      </head>
  <body>
    """
    html2 = """
  </body>
</html>
    """
    
    
    div = """
        <hr />
        <a id="chart_div_anchor_%(FUNCTIONTITLE)s" />
        %(TEXT)s
        <div id="chart_div_%(FUNCTIONTITLE)s" style="width: 600px; height: 350px;"></div>
        <a href="#" onclick="toggle_visibility('chart_div_result_%(FUNCTIONTITLE)s');">Results:</a>
        <div id="chart_div_result_%(FUNCTIONTITLE)s" style="display: none">
        <pre>
%(RESULT)s
        </pre>
        </div>
    """
    
    link = """<a href="#chart_div_anchor_%(FUNCTIONTITLE)s">%(TITLE)s</a><br>"""
    
    print >>stream, html1
    
    
    for groupname, (argslst, tests) in alltests.iteritems():
        info = dict()
        info['TITLE'] = groupname
        info['FUNCTIONTITLE'] = ''.join([x for x in groupname if str.isalpha(x)])
        
        print >>stream, link % info
    
    print >>stream, "<p/>"
    
    for groupname, (argslst, tests) in alltests.iteritems():
        info = dict()
        info['FUNCTIONTITLE'] = ''.join([x for x in groupname if str.isalpha(x)])
        info['TEXT'] = ''
        
        info['RESULT'] = ''        
        for i, args in enumerate(argslst):
            info['RESULT'] += ','.join(['%s = %s' % (k, v) for k, v in args.iteritems()]) + ':\n'
            for test in tests:
                info['RESULT'] += ' '*4 + test.lang.ljust(14) + test.results[i]['result'] + '\n'
            info['RESULT'] += '\n'
        print >>stream, div % info
    
    print >>stream, html2

def runall(alltests):
    output = sys.stdout
    if len(sys.argv) > 1:
        output = open(sys.argv[1], 'wb')
    
    if not NOPRESENT:
        present_html_header(output, alltests)
            
    for groupname, (argslst, tests) in alltests.iteritems():
        for kwargs in argslst:
            for test in tests:
                test.run(kwargs)

            if not NOPRESENT:
                present(groupname, kwargs, tests)
            
        if not NOPRESENT:
            present_html(output, groupname, argslst, tests)
            output.write('\n')
    
    if not NOPRESENT:
        present_html_footer(output, alltests)
            
runall(tests)
