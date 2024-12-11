#include <iostream>
#include <fstream>
#include <ostream>
#include <unordered_map>
#include <vector>
#include <algorithm>

using namespace std;

int part1(vector<int> vec1, vector<int> vec2){
    sort(vec1.begin(), vec1.end());
    sort(vec2.begin(), vec2.end());
    
    int distance = 0;
    for (unsigned int i = 0; i < vec1.size(); i++){
        distance += abs(vec1[i] - vec2[i]);
    }
    return distance;
}

int part2(const vector<int>& vec1, const vector<int>& vec2){
    int similarity = 0;
    for (unsigned int i = 0; i < vec1.size(); i++){
        similarity += vec1[i] * count(vec2.begin(), vec2.end(), vec1[i]);
    }
    return similarity;
}

int main(){
    vector<int> vec1, vec2;
    
    ifstream input;
    input.open("day1.txt");
    
    int a, b;
    while (input >> a >> b){
        vec1.push_back(a);
        vec2.push_back(b);
    }
    input.close();

    cout << part1(vec1, vec2) << endl;
    cout << part2(vec1, vec2) << endl;
    
    return 0;
}