#pragma once

#include <vector>
#include <chrono>
#include <algorithm>

class CTimeIt
{
	std::chrono::duration<float> m_Average;
	std::chrono::duration<float> m_Median;
	std::chrono::duration<float> m_Min;
	std::chrono::duration<float> m_Max;
public:

	template<typename FuncResult, typename Func, typename... FuncArgs>
	FuncResult run(size_t count, Func func, FuncArgs... args)
	{
		std::vector<std::chrono::duration<float>> times;
		times.resize(count);

		FuncResult result = FuncResult();
		for( size_t i = 0; i < count; ++i )
		{
			auto tstart = std::chrono::high_resolution_clock::now();

			result = func(args...);

			auto tend = std::chrono::high_resolution_clock::now();

			times[i] = tend - tstart;
		}

		std::sort( times.begin(), times.end() );

		std::chrono::duration<float> total;
		for( size_t i = 0; i < count; ++i )
		{
			total += times[i];
		}

		m_Average = total / count;
		size_t middle = count / 2;
		if( count & 1 )
			m_Median = times[middle];
		else
			m_Median = (times[middle-1] + times[middle]) / 2.0f;

		m_Min = times[0];
		m_Max = times[times.size()-1];

		return result;
	}

	/**
	 * @return Returns the average (in seconds)
	 */
	float average() const
	{
		return m_Average.count();
	}

	/**
	 * @return Returns the median (in seconds)
	 */
	float median() const
	{
		return m_Median.count();
	}

	/**
	 * @return Returns the fastest run (in seconds)
	 */
	float fastest() const
	{
		return m_Min.count();
	}

	/**
	 * @return Returns the longest run (in seconds)
	 */
	float longest() const
	{
		return m_Max.count();
	}

};
