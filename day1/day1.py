#!/usr/bin/env python3

def part1(list1, list2):
    distance = 0
    list1 = sorted(list1)
    list2 = sorted(list2)
    for i, _ in enumerate(list1):
        distance += abs(list2[i] - list1[i])
    return distance

def part2(list1, list2):
    similarity = 0
    for v in list1:
        similarity += v * list2.count(v)
    return similarity

list1 = []
list2 = []
with open("day1.txt", "r") as input:
    for line in input:
        list1.append(int(line[:5]))
        list2.append(int(line[-6:-1]))

print(part1(list1, list2))
part2(list(list1), list(list2))