#include <iostream>
#include <fstream>
#include <ostream>
#include <sstream>
#include <string>
#include <vector>
#include <cmath>

using namespace std;

vector<unsigned int> OrderUpdate(const vector<unsigned int>& update, const vector<tuple<unsigned int, unsigned int>>& ordering_rules){
    vector<unsigned int> ordered_update;
    for (auto page_nb : update){

        vector<unsigned int> page_nbs_that_should_be_before;
        for (auto ordering_rule : ordering_rules){            
            if (get<1>(ordering_rule) == page_nb){
                page_nbs_that_should_be_before.push_back(get<0>(ordering_rule));
            }
        }

        vector<unsigned int>::iterator min_pos = ordered_update.begin();
        if (page_nbs_that_should_be_before.size() > 0 and ordered_update.size() > 0){
            for (auto page_nb_that_should_be_before : page_nbs_that_should_be_before){ 
                for (auto it = ordered_update.begin(); it != ordered_update.end(); it++){
                    if (*it == page_nb_that_should_be_before && it >= min_pos){
                        min_pos = it;
                        min_pos++;
                    }
                }
            }
        }
        
        ordered_update.insert(min_pos, page_nb);
    }
    return ordered_update;
}

unsigned int Part1(const vector<vector<unsigned int>>& updates, const vector<tuple<unsigned int, unsigned int>>& ordering_rules){
    int solution = 0;
    for (auto update : updates){
        if (update == OrderUpdate(update, ordering_rules)){
            solution += update[update.size() / 2];
        }
    }
    return solution;
}

unsigned int Part2(const vector<vector<unsigned int>>& updates, const vector<tuple<unsigned int, unsigned int>>& ordering_rules){
    int solution = 0;
    for (auto update : updates){
        vector<unsigned int> ordered_update = OrderUpdate(update, ordering_rules);
        if (update != ordered_update){
            solution += ordered_update[update.size() / 2];
        }
    }
    return solution;
}

int main(int argc, char *argv[]){
    ifstream input;
    
    input.open("day5.txt");

    vector<tuple<unsigned int, unsigned int>> ordering_rules;
    vector<vector<unsigned int>> updates;
    string line;
    while (getline(input, line)){
        stringstream ss(line);
        if (line.find('|') != string::npos){
            tuple<unsigned int, unsigned int> ordering_rule;
            char c;
            ss >> get<0>(ordering_rule) >> c >> get<1>(ordering_rule);
            ordering_rules.push_back(ordering_rule);
        }
        if (line.find(',') != string::npos){
            vector<unsigned int> update;
            while (ss.good()){
                string page_nb_as_str;
                getline(ss, page_nb_as_str, ',');
                update.push_back(stoi(page_nb_as_str));
            }
            updates.push_back(update);
        }
    }
    input.close();
    
    cout << Part1(updates, ordering_rules) << endl;
    cout << Part2(updates, ordering_rules) << endl;

    return 0;
}
