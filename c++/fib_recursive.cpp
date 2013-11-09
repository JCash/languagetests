#include "test.h"

static bigint_t Fibonacci(int n)
{
	if( n <= 1 )
		return n;
	return Fibonacci(n - 2) + Fibonacci(n - 1);
}

int main(int argc, const char** argv)
{
	Test(argc, argv, "Fibonacci (recursive)", Fibonacci);
	return 0;
}
