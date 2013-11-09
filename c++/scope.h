#pragma once

#include <chrono>

struct STimeScope
{
	std::chrono::high_resolution_clock::time_point 	m_TimeStart;
	std::chrono::high_resolution_clock::time_point 	m_TimeEnd;
	std::chrono::duration<float>			m_Elapsed;
	uint32_t _pad;

	STimeScope()
	{
		m_TimeStart = std::chrono::steady_clock::now();
	}

	~STimeScope()
	{
	}

	void stop()
	{
		m_TimeEnd = std::chrono::steady_clock::now();
		m_Elapsed = m_TimeEnd - m_TimeStart;
	}

	float seconds()
	{
		stop();
		return m_Elapsed.count();
	}

	float milliseconds()
	{
		return seconds() * 1000.0f;
	}

	float microseconds()
	{
		return seconds() * 1000000.0f;
	}
};
