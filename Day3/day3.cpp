// The challenge for this one was not to use regex

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

std::tuple<unsigned int, int> parse_and_execute_mul_instruction(std::string instruction){
    if (instruction.substr(0, 4) == "mul("){
        instruction = instruction.substr(4);
    }
    else{
        return {0, 0};
    }
    std::string a_as_str, b_as_str;
    unsigned char curChar = instruction[0];
    while (true) {
        if (std::isdigit(curChar)){
            a_as_str += curChar;
            instruction.erase(0, 1);
            curChar = instruction[0];
        }
        else if (curChar == ','){
            instruction.erase(0, 1);
            break;
        }
        else if (a_as_str.size() > 3){
            return {0, 0};
        }
        else{
            return {0, 0};
        }
    }
    curChar = instruction[0];
    while (true) {
        if (std::isdigit(curChar)){
            b_as_str += curChar;
            instruction.erase(0, 1);
            curChar = instruction[0];
        }
        else if (curChar == ')'){
            instruction.erase(0, 1);
            break;
        }
        else if (b_as_str.size() > 3){
            return {0, 0};
        }
        else{
            
            return {0, 0};
        }
    }
    int a = std::stoi(a_as_str);
    int b = std::stoi(b_as_str);
    return {a_as_str.size() + b_as_str.size(), a * b};
}

int part1(const std::string& memory){
    std::string maybeInstruction;
    int accumulator = 0;
    unsigned int i = 0;
    while (i < memory.size()){
        unsigned char curChar = memory[i];
        if (curChar == 'm'){
            maybeInstruction = memory.substr(i, 12);
            std::tuple <unsigned int, int> result = parse_and_execute_mul_instruction(maybeInstruction);
            if (std::get<0>(result)){
                accumulator += std::get<1>(result);
                i += std::get<0>(result);
            }
        }
        i++;
    }
    return accumulator;
}

int part2(const std::string& memory){
    std::string maybeInstruction;
    int accumulator = 0;
    unsigned int i = 0;
    bool is_processing_instructions_enabled = true;
    while (i < memory.size()){
        unsigned char curChar = memory[i];
        if (curChar == 'm'  and is_processing_instructions_enabled){
            maybeInstruction = memory.substr(i, 12);
            std::tuple <unsigned int, int> result = parse_and_execute_mul_instruction(maybeInstruction);
            if (std::get<0>(result)){
                accumulator += std::get<1>(result);
                i += std::get<0>(result);
            }
        }
        if (curChar == 'd'){
            maybeInstruction = memory.substr(i, 4);
            if (maybeInstruction == "do()"){
                is_processing_instructions_enabled = true;
            }
            maybeInstruction = memory.substr(i, 7);
            if (maybeInstruction == "don't()"){
                is_processing_instructions_enabled = false;
            }
        }
        i++;
    }
    return accumulator;
}

int main(int argc, char *argv[]){

    std::string sep = "/";
    std::string path(argv[0]);
    path = path.substr(0, path.rfind(sep));
    
    std::string memory;
    std::ifstream input;
    input.open(path + sep + "input.txt");
    std::stringstream ss;
    ss << input.rdbuf();
    input.close();
    memory = ss.str();
    
    std::cout << part1(memory) << std::endl;
    std::cout << part2(memory) << std::endl;
    return 0;
}