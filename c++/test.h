#pragma once

#include <iostream>
#include <iomanip>
#include "timeit.h"
#include "reporter.h"


#ifdef HAVE_GMP
#include <gmpxx.h>			// ~102 us us for n=400
typedef mpz_class	bigint_t;
#warning "Using GMP"
#else
#include "InfInt.h"			// ~106 us for n=400
typedef InfInt	bigint_t;
#warning "Using InfInt"
#endif
//#include "bigInt.h"	// ~60000 us for n=400
//#include "BigUnsigned.hh" // ~4100 us for n=400


template<typename Func>
void Test(int argc, const char** argv, const std::string& title, Func func)
{
	const size_t iterations = argc > 1 ? (size_t)std::stoi( argv[1] ) : 100;
	const int n = argc > 2 ? std::stoi( argv[2] ) : 40;

	CTimeIt timeit;
	bigint_t result = timeit.run<bigint_t>( iterations, func, n );

	write_result(std::cout,
			title,
			iterations,
			timeit.average(),
			timeit.median(),
			timeit.fastest(),
			timeit.longest(),
			result);
}
