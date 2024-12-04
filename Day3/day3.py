from pathlib import Path
import re

def exec_mul_instruction(instruction):
    regex  = r"mul\((\d+),(\d+)\)"
    matches = re.findall(regex, instruction)
    return [int(match[0]) * int(match[1]) for match in matches][0]

def part1(memory):
    regex  = r"mul\(\d+,\d+\)"
    matches = re.findall(regex, memory)
    result = sum([exec_mul_instruction(match) for match in matches])
    print(result)

def part2(memory):
    regex = r"(mul\(\d+,\d+\)|do\(\)|don't\(\))"
    matches = re.findall(regex, memory)
    is_processing_instructions_enabled = True
    accumulator = 0
    for match in matches:
        if match.startswith("mul") and is_processing_instructions_enabled:
            accumulator += exec_mul_instruction(match)
        elif match == "do()":
            is_processing_instructions_enabled = True
        elif match == "don't()":
            is_processing_instructions_enabled = False
    print(accumulator)

memory = ""
with open(Path(__file__).parent / "input.txt", "r") as input:
    memory = input.read()
part1(memory)
part2(memory)