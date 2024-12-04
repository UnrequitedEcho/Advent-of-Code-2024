#include <iostream>
#include <fstream>
#include <ostream>
#include <string>
#include <vector>
#include <array>

using namespace std;

unsigned int CountXmas(const vector<string>& ws, unsigned int l, unsigned int c){
    unsigned int accumulator = 0;
    bool space_left = c >= 3;
    bool space_right = c <= ws[0].size() - 4;
    bool space_above = l >= 3;
    bool space_below = l <= ws.size() - 4;

    array<string, 8>maybe_mas_s;
    for (unsigned int i = 1; i < 4; i++){
        if (space_right){ maybe_mas_s[1] += ws[l][c+i]; };
        if (space_left){ maybe_mas_s[0] += ws[l][c-i]; };
        if (space_above){ maybe_mas_s[2] += ws[l-i][c]; };
        if (space_below){ maybe_mas_s[3] += ws[l+i][c]; };
        if (space_right and space_above){ maybe_mas_s[6] += ws[l-i][c+i]; };
        if (space_right and space_below){ maybe_mas_s[7] += ws[l+i][c+i]; };
        if (space_left and space_above){ maybe_mas_s[4] += ws[l-i][c-i]; };
        if (space_left and space_below){ maybe_mas_s[5] += ws[l+i][c-i]; };
    }
    for (string maybe_mas : maybe_mas_s){;
        if (maybe_mas == "MAS"){
            accumulator++;
        }
    }

    return accumulator;
}

unsigned int Part1(const vector<string>& word_search){
    unsigned int accumulator = 0;
    for (unsigned int i = 0; i < word_search.size(); i++){
        for (unsigned int j = 0; j < word_search[0].size(); j++){
            if (word_search[i][j] == 'X'){
                accumulator += CountXmas(word_search, i, j);
            }
        }
    }
    return accumulator;
}

bool IsCrossMas(const vector<string>& ws, unsigned int l, unsigned int c){
    bool space_left = c >= 1;
    bool space_right = c <= ws[0].size() - 2;
    bool space_above = l >= 1;
    bool space_below = l <= ws.size() - 2;

    if (!(space_left and space_right and space_above and space_below)){
        return false;
    }
    
    string diagonal1 = ws[l-1][c-1] + string("A") + ws[l+1][c+1];
    string diagonal2 = ws[l+1][c-1] + string("A") + ws[l-1][c+1];
    
    if ((diagonal1 == "MAS" or diagonal1 == "SAM")
    and (diagonal2 == "MAS" or diagonal2 == "SAM")){
        return true;
    }
    return false;
}

unsigned int Part2(const vector<string>& word_search){
    unsigned int accumulator = 0;
    for (unsigned int i = 0; i < word_search.size(); i++){
        for (unsigned int j = 0; j < word_search[0].size(); j++){
            if (word_search[i][j] == 'A'){
                if (IsCrossMas(word_search, i, j)){
                    accumulator++;
                }
            }
        }
    }
    return accumulator;
}

int main(int argc, char *argv[]){
    string sep = "/";
    string path(argv[0]);
    path = path.substr(0, path.rfind(sep));

    vector<string> word_search;
    ifstream input;
    input.open(path + sep + "input.txt");

    string line;
    while (input >> line){
        word_search.push_back(line);
    }
    input.close();

    cout << Part1(word_search) << endl;
    cout << Part2(word_search) << endl;
    
    return 0;
}