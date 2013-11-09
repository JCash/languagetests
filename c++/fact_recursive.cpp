#include "test.h"

static bigint_t Factorial(int n)
{
	if( n == 1 )
		return 1;

	return Factorial(n - 1) * n;
}

int main(int argc, const char** argv)
{
	Test(argc, argv, "Factorial (recursive)", Factorial);
	return 0;
}


