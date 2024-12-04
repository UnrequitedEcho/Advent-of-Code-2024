#include <iostream>
#include <fstream>
#include <ostream>
#include <unordered_map>
#include <vector>
#include <algorithm>

int part1(std::vector<unsigned int> list1, std::vector<unsigned int> list2){
    std::sort(list1.begin(), list1.end());
    std::sort(list2.begin(), list2.end());
    
    unsigned int distance = 0;
    for (unsigned int i = 0; i < list1.size(); i++){
        distance += std::abs(static_cast<int>(list1[i]) - static_cast<int>(list2[i]));
    }
    return distance;
}

int part2(const std::vector<unsigned int>& list1, const std::vector<unsigned int>&list2){
    std::unordered_map<unsigned int, unsigned int> counter;
    for (unsigned int i = 0; i < list2.size(); i++){
        counter[list2[i]]++;
    }
    
    unsigned int similarity = 0;
    for (unsigned int i = 0; i < list1.size(); i++){
        similarity += list1[i] * counter[list1[i]];
    }
    return similarity;
}

int main(int argc, char *argv[]){
    std::vector<unsigned int> list1, list2;
    
    std::string sep = "/";
    std::string path(argv[0]);
    path = path.substr(0, path.rfind(sep));
    std::cout << path << std::endl;
    std::ifstream input;
    input.open(path + sep + "input.txt");
    
    unsigned int a, b;
    while (input >> a >> b){
        list1.push_back(a);
        list2.push_back(b);
    }
    input.close();

    std::cout << part1(list1, list2) << std::endl;
    std::cout << part2(list1, list2) << std::endl;
    
    return 0;
}