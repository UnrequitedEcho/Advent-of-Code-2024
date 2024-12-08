from pathlib import Path
from tqdm import tqdm

class Node:
    def __init__(self, res):
        self.add = None
        self.mul = None
        self.conc = None
        self.res = res

    def calculate(self, number, part_nb):
        self.add = Node(self.res + number)
        self.mul = Node(self.res * number)
        if part_nb == 1:
            return [self.add, self.mul]
        else:
            self.conc = Node(int(str(self.res) + str(number)))
            return [self.add, self.mul, self.conc]

def solve(equations, part_nb):
    solution = 0
    for equation in tqdm(equations):
        expected = equation[0]
        numbers = equation[1:]
        nodes = [Node(numbers[0])]
        numbers = numbers[1:]

        for number in numbers:
            for node in list(nodes):
                nodes.remove(node)
                for result_node in node.calculate(number, part_nb=part_nb):
                    if result_node.res <= expected:
                        nodes.append(result_node)            

        for node in nodes:
            if node.res == expected:
                solution += expected
                break
                
    print(solution)

equations = []
with open(Path(__file__).parent / "input.txt", "r") as input:
    for line in input:
        equations.append([int(line.split(":")[0])] + [int(x) for x in line.split(":")[1].strip().split(" ")])

solve(equations, part_nb=1)
solve(equations, part_nb=2)

