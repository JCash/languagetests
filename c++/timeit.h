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
	size_t m_Count;
public:

	template<typename FuncResult, typename Func, typename... FuncArgs>
	FuncResult run(size_t count, Func func, FuncArgs&... args)
	{
		m_Count = count;
		std::vector<std::chrono::duration<float>> times;
		times.resize(m_Count);

		FuncResult result = FuncResult();
		for( size_t i = 0; i < m_Count; ++i )
		{
			auto tstart = std::chrono::high_resolution_clock::now();

			result = func(args...);

			auto tend = std::chrono::high_resolution_clock::now();

			times[i] = tend - tstart;
		}

		std::sort( times.begin(), times.end() );

		std::chrono::duration<float> total;
		for( size_t i = 0; i < m_Count; ++i )
		{
			total += times[i];
		}

		m_Average = total / m_Count;
		size_t middle = m_Count / 2;
		if( m_Count & 1 )
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

	void report_time(std::ostream& stream, float t)
	{
		if( t < 0.000001f )
			stream << t * 1000000000.0 << " ns";
		else if( t < 0.001f )
			stream << t * 1000000.0 << " \u00b5s";
		else if( t < 0.1f )
			stream << t * 1000.0 << " ms";
		else
			stream << t << " s";
	}

	void report(std::ostream& stream, const std::string& title)
	{
		stream << std::fixed << std::setprecision(3);
		stream << title << "\titerations:" << m_Count;
		stream << "\tavg: "; report_time(stream, average());
		stream << "\tmedian: "; report_time(stream, median());
		stream << "\tmin: "; report_time(stream, fastest());
		stream << "\tmax: "; report_time(stream, longest());
		stream << std::endl;
	}
};
