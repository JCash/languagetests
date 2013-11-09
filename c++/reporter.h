#pragma once

#include <istream>
#include <iomanip>
#include <string>

template<typename RESULT>
void write_result(std::ostream& stream,
		const std::string& title,
		size_t iterations,
		float time_avg,
		float time_mean,
		float time_min,
		float time_max,
		RESULT result
		)
{
	stream << std::fixed << std::setprecision(12);
	stream << "{" << std::endl;
	stream << "\"title\": \"" << title << "\"," << std::endl;
    stream << "\"iterations\": " << iterations << "," << std::endl;
    stream << "\"time_avg\": " << time_avg << "," << std::endl;
    stream << "\"time_mean\": " << time_mean << "," << std::endl;
    stream << "\"time_min\": " << time_min << "," << std::endl;
    stream << "\"time_max\": " << time_max << "," << std::endl;
    stream << "\"result\": \"" << result << "\"" << std::endl;
	stream << "}" << std::endl;
}
