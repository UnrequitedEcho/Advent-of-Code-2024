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

def part2(equations):
    solution = 0
    for expected, numbers in tqdm(equations.items()):
        nodes = [Node(numbers[0])]
        numbers = numbers[1:]
        found = False
        while not found and numbers :
            for node in list(nodes):
                node.add = Node(node.res + numbers[0])
                if node.add.res == expected:
                    found = True
                node.mul = Node(node.res * numbers[0])
                if node.mul.res == expected:
                    found = True
                node.conc = Node()
                if node.conc.res == expected:
                    found = True
                nodes.remove(node)
                nodes.append(node.add)
                nodes.append(node.mul)
                nodes.append(node.conc)
            numbers = numbers[1:]

        if found:
            solution += expected
    print(solution)

equations = []
with open(Path(__file__).parent / "input.txt", "r") as input:
    for line in input:
        equations.append([int(line.split(":")[0])] + [int(x) for x in line.split(":")[1].strip().split(" ")])

#equations = [[292, 11, 6, 16, 20]]
solve(equations, part_nb=1)
solve(equations, part_nb=2)
#part2(equations) 

