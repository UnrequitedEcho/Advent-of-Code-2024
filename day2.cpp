// The challenge for this one was not to use bruteforce

#include <iostream>
#include <fstream>
#include <ostream>
#include <sstream>
#include <vector>
#include <string>
#include <tuple>

std::tuple<bool, unsigned int> is_report_safe(const std::vector<unsigned short>& report){
    std::vector<int> differences;
    int sumDiff = 0;
    for (unsigned int i = 0; i < report.size() - 1; i++){
        differences.push_back(static_cast<int>(report[i + 1]) - static_cast<int>(report[i]));
        sumDiff += (differences.back() >= 0) ? 1 : -1;
    }
    bool isIncreasing = (sumDiff >= 0) ? true : false;
    for (unsigned int i = 0; i < report.size() - 1; i++){
        if ((isIncreasing and (differences[i] < 1 or differences[i] > 3))
        or (!isIncreasing and (differences[i] < -3 or differences[i] > -1))){
            return {false, i};
        }
    }
    return {true, 0};
}

int part1(const std::vector<std::vector<unsigned short>>& reports){
    unsigned int accumulator = 0;
    for (const std::vector<unsigned short>& report : reports){
        if (std::get<bool>(is_report_safe(report))){
            accumulator++;
        }
    }
    return accumulator;
}

int part2(const std::vector<std::vector<unsigned short>>& reports){
    unsigned int accumulator = 0;
    for (const std::vector<unsigned short>& report : reports){
        std::tuple<bool, unsigned int> result = is_report_safe(report);
        if (std::get<bool>(result)){
            accumulator++;
        }
        else {
            std::vector<unsigned short> dampened_report1 = report;
            dampened_report1.erase(dampened_report1.begin() + std::get<unsigned int>(result));
            std::vector<unsigned short> dampened_report2 = report;
            dampened_report2.erase(dampened_report2.begin() + std::get<unsigned int>(result) + 1);
            
            if (std::get<bool>(is_report_safe(dampened_report1)) or std::get<bool>(is_report_safe(dampened_report2))){
                accumulator++;
            }
        }
    }
    return accumulator;
}

int main(int argc, char *argv[]){
    std::vector<std::vector<unsigned short>> reports;
    
    std::ifstream input;
    input.open("day2.txt");
    std::string line;
    while (std::getline(input, line)){
        std::vector<unsigned short> report;
        std::stringstream ss(line);
        std::string item;
        while(std::getline(ss, item, ' ')){
            report.push_back(std::stoi(item));
        }
        reports.push_back(report);
    }
    input.close();

    std::cout << part1(reports) << std::endl;
    std::cout << part2(reports) << std::endl;
    
    return 0;
}