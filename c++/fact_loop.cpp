#include "test.h"

static bigint_t Factorial(int n)
{
	bigint_t factorial = 1;
	for(int i = 1; i <= n; i++)
	{
		factorial *= i;
	}
	return factorial;
}

int main(int argc, const char** argv)
{
	Test(argc, argv, "Factorial (loop)", Factorial);
	return 0;
}
