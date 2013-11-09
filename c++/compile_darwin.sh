
SOURCEDIR=`dirname $0`
PLATFORM=`uname -s`
BUILDDIR=$SOURCEDIR/../build/$PLATFORM

if [ -e /usr/local/include/gmpxx.h ]; then
    GMPFLAGS="-I/usr/local/include -L/usr/local/lib -lgmpxx -lgmp"
    GMPDEFINES="-DHAVE_GMP"
fi

CXXFLAGS="-std=c++11 -g -O4 -stdlib=libc++ -Wno-c++98-compat -Wno-c++98-compat-pedantic -Weverything -pedantic -Wno-global-constructors -Wno-exit-time-destructors $GMPFLAGS $GMPDEFINES"
LDFLAGS=""
COMPILER=clang++

if [ ! -d "$BUILDDIR" ]; then
  mkdir -p $BUILDDIR
fi

$COMPILER $CXXFLAGS -o $BUILDDIR/fact_recursive $SOURCEDIR/fact_recursive.cpp
$COMPILER $CXXFLAGS -o $BUILDDIR/fact_loop $SOURCEDIR/fact_loop.cpp
$COMPILER $CXXFLAGS -o $BUILDDIR/fib_recursive $SOURCEDIR/fib_recursive.cpp
$COMPILER $CXXFLAGS -o $BUILDDIR/fib_loop $SOURCEDIR/fib_loop.cpp
