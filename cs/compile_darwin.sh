
SOURCEDIR=`dirname $0`
PLATFORM=`uname -s`
BUILDDIR=$SOURCEDIR/../build/$PLATFORM
CSFLAGS="--lint -warnaserror -v -r:System -r:Mono.Security -r:System.Json -r:System.Web.Extensions"
COMPILER=gmcs

if [ ! -d "$BUILDDIR" ]; then
  mkdir -p $BUILDDIR
fi

COMMON="$SOURCEDIR/reporter.cs $SOURCEDIR/timeit.cs"

$COMPILER $CSFLAGS -out:$BUILDDIR/fact_recursive.exe $COMMON $SOURCEDIR/fact_recursive.cs
$COMPILER $CSFLAGS -out:$BUILDDIR/fact_loop.exe $COMMON $SOURCEDIR/fact_loop.cs
$COMPILER $CSFLAGS -out:$BUILDDIR/fib_recursive.exe $COMMON $SOURCEDIR/fib_recursive.cs
$COMPILER $CSFLAGS -out:$BUILDDIR/fib_loop.exe $COMMON $SOURCEDIR/fib_loop.cs
    