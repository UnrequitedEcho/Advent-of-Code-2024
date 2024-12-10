#!/usr/bin/env python3
from collections import Counter

def part1(list1, list2):
    distance = 0
    while list1:
        min1 = min(list1)
        min2 = min(list2)
        distance += abs(min1 - min2)
        list1.remove(min1)
        list2.remove(min2)
    print(distance)

def part2(list1, list2):
    similarity_score = 0
    list2_counter = Counter(list2)
    for location_id in list1:
        similarity_score += location_id * list2_counter[location_id]
    print(similarity_score)

list1 = []
list2 = []
with open("day1.txt", "r") as input:
    for line in input:
        list1.append(int(line[:5]))
        list2.append(int(line[-6:-1]))

part1(list(list1), list(list2))
part2(list(list1), list(list2))