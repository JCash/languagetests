Language Tests
==============

This is my quite unscientific playground for comparing execution times between languages and platforms
in different situations. I choose the languages I usually work with or are interested in working with.

For instance, I've heard it so many times that Python is slower than c++ so I start to wonder exactly
''how'' much slower it is.


Implementation Details
======================

Since C++ doesn't have a built in big int implementation, I first used the InfInt (https://code.google.com/p/infint).
I also tried the BigInteger (https://mattmccutchen.net/bigint) and bigInt (http://netcologne.dl.sourceforge.net/project/cpp-bigint).
After trying these out, I felt that I needed more "production quality" (i.e. speed) so I tried GMP (http://gmplib.org/).

Here is an example of timings for C++ big int classes (if you are looking into one).

Factorial(n=400) (time in microseconds):
<table>
    <tr><td>Lib</td><td>Time (us)</td></tr>
    <tr><td>gmp</td><td>~13.7</td></tr>
    <tr><td>InfInt</td><td>~107</td></tr>
    <tr><td>BigInteger</td><td>~4100</td></tr>
    <tr><td>bigInt</td><td>~60000</td></tr>
</table>

I've made it so that the tests use GMP if it's installed, or InfInt.h otherwise (since it's a single header file).

For C#, I use the built in BigInteger class, and for Python the built in integer class (it's handled by default)

I also make a point of using the same implementation in all languages, since that's how new comers usually do.
They code the way they're used to if they don't know anything specific about the language.

Also, I don't try to optimize the examples too much, since that in real situations, you might not always have time to do that.

