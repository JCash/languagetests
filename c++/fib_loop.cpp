#include "test.h"

static bigint_t Fibonacci(int n)
{
	bigint_t a = 0;
	bigint_t b = 1;
	int i = 1;
    while( i <= n )
    {
    	bigint_t c = a + b;
        a = b;
        b = c;
        i += 1;
    }
    return a;
}

int main(int argc, const char** argv)
{
	Test(argc, argv, "Fibonacci (loop)", Fibonacci);
	return 0;
}
