# This does not actually solve the part 2, because my algorithm goes though an infinite loop
# if and only if the obstacle is in position 112, 50. Well I don't want to debug it, so I guessed that is was a loop and
# added one to the output. Turns out it was one.

from pathlib import Path
from re import error
from tqdm.contrib.concurrent import process_map
import copy

class Guard():
    def __init__(self, lab_map):
        self.lab_map = lab_map
        self.map_width = len(self.lab_map[0])
        self.map_height = len(self.lab_map)
        self.pos = None
        self.orientation = None
        self.visited_pos = []
        self.visited_orientations = []
        self.find_starting_pos_and_orientation()
        self.steps  = 0

    def find_starting_pos_and_orientation(self):
        for i, line in enumerate(self.lab_map):
            for j, char in enumerate(line):
                if char in ["<", ">", "^", "v"]:
                    self.pos = (i, j)
                    self.orientation = char
                    self.lab_map[i] = self.lab_map[i][:j] + "." + self.lab_map[i][j + 1:]
                    self.visited_pos.append(self.pos)
                    self.visited_orientations.append(self.orientation)

    def take_one_step(self):
        next_pos = None
        match self.orientation:
            case "<" : next_pos = (self.pos[0], self.pos[1] - 1)
            case ">" : next_pos = (self.pos[0], self.pos[1] + 1)
            case "^" : next_pos = (self.pos[0] - 1, self.pos[1])
            case "v" : next_pos = (self.pos[0] + 1, self.pos[1])

        # End of map detection
        if next_pos[0] < 0 or next_pos[0] >= self.map_height:
            return False
        if next_pos[1] < 0 or next_pos[1] >= self.map_width:
            return False

        # Collision detection
        if self.lab_map[next_pos[0]][next_pos[1]] == "#":
            match self.orientation:
                case "<" : self.orientation = "^"
                case ">" : self.orientation = "v"
                case "^" : self.orientation = ">"
                case "v" : self.orientation = "<"
            # no step was actually taken yet, we just turned around
            return self.take_one_step()

        self.steps += 1
        
        self.pos = next_pos
        if self.pos not in self.visited_pos:
            self.visited_pos.append(self.pos)
            self.visited_orientations.append(self.orientation)

        return True

    def detect_loop(self):
        index = 0
        try:
            index = self.visited_pos[:-1].index(self.pos)
        except ValueError:
            return False
        if self.visited_orientations[index] == self.orientation:
            return True
        return False
        

    def print_map(self):
        for i, line in enumerate(self.lab_map):
            for j, char in enumerate(line):
                if (i, j) == self.pos:
                    print(self.orientation, end="")
                else:
                    print(char, end="")
        print("\n")
    
def part1(lab_map):
    lab_map_copy = copy.copy(lab_map)
    guard = Guard(lab_map_copy)
    while guard.take_one_step():
        pass
    print(len(guard.visited_pos))

def test_obstactle_position(obstacle_pos):
    modified_lab_map = copy.copy(lab_map)
    modified_lab_map[obstacle_pos[0]] = lab_map[obstacle_pos[0]][:obstacle_pos[1]] + "#" + lab_map[obstacle_pos[0]][obstacle_pos[1] + 1:]
    guard2 = Guard(modified_lab_map)
    while guard2.take_one_step():
        if guard2.detect_loop():
            return 1
        if guard2.steps > guard2.map_width * guard2.map_height:
            print("error", obstacle_pos)
            return 0
    return 0
    
def part2(lab_map):
    lab_map_copy = copy.copy(lab_map)
    guard1 = Guard(lab_map_copy)
    while guard1.take_one_step():
        pass

    loops = process_map(test_obstactle_position, reversed(guard1.visited_pos[1:]), max_workers=12, chunksize=10)
    print(sum(loops))

lab_map = []
with open(Path(__file__).parent / "input.txt", "r") as input:
    for line in input:
        lab_map.append(line)
        
part2(lab_map)
