#include <filesystem>
#include <fstream>
#include <ostream>
#include <string>
#include <sys/types.h>
#include <vector>
#include <tuple>
#include <iostream>

using namespace std;

enum Orientation { UP, DOWN, LEFT, RIGHT};

struct Position {
    uint x;
    uint y;
};

struct Guard {
    Position pos;
    Orientation orient;
};

bool GuardRunOnce(Guard& guard, const vector<Position>& obstacles, const tuple<uint, uint>& map_size){
    Guard old_guard = guard;
    switch (guard.orient){
        case UP:
            guard.pos.y = 1;
            for (auto obstacle : obstacles){
                if (obstacle.x == guard.pos.x){ // obstacle on the same vertical
                    if (obstacle.y >= guard.pos.y && obstacle.y < old_guard.pos.y){ // obstacle above guard.pos
                        guard.pos.y = obstacle.y + 1;
                        guard.orient = RIGHT;
                    }
                }
            }
            break;
        case DOWN:
            guard.pos.y = get<1>(map_size);
            for (auto obstacle : obstacles){
                if (obstacle.x == guard.pos.x){ // obstacle on the same vertical
                    if (obstacle.y <= guard.pos.y && obstacle.y > old_guard.pos.y){ // obstacle below guard.pos
                        guard.pos.y = obstacle.y - 1;
                        guard.orient = LEFT;
                    }
                }
            }
            break;
        case RIGHT:
            guard.pos.x = get<0>(map_size);
            for (auto obstacle : obstacles){
                if (obstacle.y == guard.pos.y){ // obstacle on the same horizontal
                    if (obstacle.x <= guard.pos.x && obstacle.x > old_guard.pos.x){ // obstacle right of the guard.pos
                        guard.pos.x = obstacle.x - 1;
                        guard.orient = DOWN;
                    }
                }
            }
            break;
        case LEFT:
            guard.pos.x = 1;
            for (auto obstacle : obstacles){
                if (obstacle.y == guard.pos.y){ // obstacle on the same horizontal
                    if (obstacle.x >= guard.pos.x && obstacle.x < old_guard.pos.x){ // obstacle left of the guard.pos
                        guard.pos.x = obstacle.x + 1;
                        guard.orient = UP;
                    }
                }
            }
            break;
    }
    
    // We are out of bounds !
    if (guard.pos.x <= 1){
        guard.pos.x = 1;
        return false;
    }
    if (guard.pos.x >= get<0>(map_size)){
        guard.pos.x = get<0>(map_size);
        return false;
    }
    if (guard.pos.y <= 1){
        guard.pos.y = 1;
        return false;
    }
    if (guard.pos.y >= get<1>(map_size)){
        guard.pos.y = get<1>(map_size);
        return false;
    }    
    return true;
}

vector<Position> GenerateStepsBetween(const Position& start, const Position& end){
    vector<Position> breadcrumb_trail;
    for (uint i = start.x + 1; i < end.x; i++){
            Position breadcrumb;
            breadcrumb.x = i;
            breadcrumb.y = start.y;
            breadcrumb_trail.push_back(breadcrumb);
        }
    for (uint i = start.x - 1; i > end.x; i--){
        Position breadcrumb;
        breadcrumb.x = i;
        breadcrumb.y = start.y;
        breadcrumb_trail.push_back(breadcrumb);
    }
    for (uint i = start.y + 1; i < end.y; i++){
        Position breadcrumb;
        breadcrumb.x = start.x;
        breadcrumb.y = i;
        breadcrumb_trail.push_back(breadcrumb);
    }
    for (uint i = start.y - 1; i > end.y; i--){
        Position breadcrumb;
        breadcrumb.x = start.x;
        breadcrumb.y = i;
        breadcrumb_trail.push_back(breadcrumb);
    }
    return breadcrumb_trail;
}

vector<Position> GuardRunBreadcrumbTrail(const Guard& start_guard, const vector<Position>& obstacles, const tuple<uint, uint>& map_size){
    Guard guard = start_guard;
    vector<Position> breadcrumb_trail = {guard.pos};

    // Actually Running
    while (GuardRunOnce(guard, obstacles, map_size)){
        breadcrumb_trail.push_back(guard.pos);
    }
    breadcrumb_trail.push_back(guard.pos);

    // Add intermediary steps if they are not yet recorded
    // Removes duplicates
    vector<Position> steps;
    for (uint i = 0; i < breadcrumb_trail.size() - 1; i++){

        vector<Position> segment_steps = GenerateStepsBetween(breadcrumb_trail[i], breadcrumb_trail[i + 1]);
        segment_steps.insert(segment_steps.begin(), breadcrumb_trail[i]);
        segment_steps.push_back(breadcrumb_trail[i + 1]);
        
        for (Position segment_step : segment_steps){
            bool is_unique = true;
            for (Position step : steps){
                if (segment_step.x == step.x && segment_step.y == step.y){
                    is_unique = false;
                }
            }
            if (is_unique){
                steps.push_back(segment_step);
            }
        }
    }
    
    return steps;
}

bool GuardRunCheckLoops(const Guard& start_guard, const vector<Position>& obstacles, const tuple<uint, uint>& map_size){
    Guard guard = start_guard;
    vector<Guard> previous_guards;

    // Actually Running
    while (GuardRunOnce(guard, obstacles, map_size)){
        // Check if our guard is running in a loop !
        for (uint i = 0; i < previous_guards.size(); i++){
            // Guard should really be a class with an overloaded == oparator but I can't be bothered
            if (previous_guards[i].pos.x == guard.pos.x
             && previous_guards[i].pos.y == guard.pos.y
             && previous_guards[i].orient == guard.orient){
                return true;
            }
        }
        previous_guards.push_back(guard);
    }
    return false;
}


int Part1(const Guard& start_guard, const vector<Position>& obstacles, const tuple<uint, uint>& map_size){
    return GuardRunBreadcrumbTrail(start_guard, obstacles, map_size).size();
}

int Part2(const Guard& start_guard, const vector<Position>& obstacles, const tuple<uint, uint>& map_size){
    uint solution = 0;

    vector<Position> added_obstacle_positions = GuardRunBreadcrumbTrail(start_guard, obstacles, map_size);
    for (Position added_obstacle_position : added_obstacle_positions){
        vector<Position> upgraded_obstacles = obstacles;
        upgraded_obstacles.push_back(added_obstacle_position);
        if (GuardRunCheckLoops(start_guard, upgraded_obstacles, map_size)){
            solution++;
        }        
    }
    return solution;
}

int main(int argc, char *argv[]){

    ifstream input;
    if (argc <=1) {
        string path(argv[0]);
        string parent_path = path.substr(0, path.rfind(filesystem::path::preferred_separator));
        input.open(parent_path + filesystem::path::preferred_separator + "input.txt");
    }
    else {
        input.open("input.txt");
    }

    vector<Position> obstacles;
    Guard guard;
    guard.orient = UP;
    tuple<uint, uint> map_size;
    string line;
    int y = 0;
    while (getline(input, line)){
        for (uint x = 0; x < line.size(); x++){
            if (line[x] == '#'){
                Position obstacle;
                obstacle.y = y + 1;
                obstacle.x = x + 1;
                obstacles.push_back(obstacle);
            }
            if (line[x] == '^'){
                guard.pos.y = y + 1;
                guard.pos.x = x + 1;
            }
        }
        y++;
        get<0>(map_size) = line.size();
        get<1>(map_size) = y;
    }
    input.close();

    cout << Part1(guard, obstacles, map_size) << endl;
    cout << Part2(guard, obstacles, map_size) << endl;
    
    return 0;
}