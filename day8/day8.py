#!/usr/bin/env python3

def part1():
    antinodes = set()
    for frequency in antennas_pos:
        for pos1 in antennas_pos[frequency]:
            for pos2 in antennas_pos[frequency]:
                if pos1 == pos2:
                    continue
                dist = (pos2[0] - pos1[0], pos2[1] - pos1[1])
                maybe_antinodes = [(pos1[0]-dist[0], pos1[1]-dist[1]), (pos1[0]+dist[0], pos1[1]+dist[1])]
                maybe_antinodes = [pos for pos in maybe_antinodes if pos != pos2]
                maybe_antinodes = [pos for pos in maybe_antinodes if pos[0] >= 1 and pos[0] <= map_size[0] and pos[1] >=1 and pos[1] <= map_size[1]]
                antinodes.update(maybe_antinodes)
    print(len(antinodes))

def part2():
    antinodes = set()
    for frequency in antennas_pos:
        for pos1 in antennas_pos[frequency]:
            for pos2 in antennas_pos[frequency]:
                if pos1 == pos2:
                    continue
                dist = (pos2[0] - pos1[0], pos2[1] - pos1[1])
                antinodes_pos = []
                antinode_pos = pos1
                while True:
                    antinode_pos = (antinode_pos[0] - dist[0], antinode_pos[1] - dist[1])
                    if antinode_pos[0] < 1 or antinode_pos[0] > map_size[0] or antinode_pos[1] < 1 or antinode_pos[1] > map_size[1]:
                        break
                    antinodes_pos.append(antinode_pos)
                while True:
                    antinode_pos = (antinode_pos[0] + dist[0], antinode_pos[1] + dist[1])
                    if antinode_pos[0] < 1 or antinode_pos[0] > map_size[0] or antinode_pos[1] < 1 or antinode_pos[1] > map_size[1]:
                        break
                    antinodes_pos.append(antinode_pos)
                antinodes.update(antinodes_pos)
    print(len(antinodes))


antennas_pos = {}
map_size = (0, 0)

with open("day8.txt", "r") as input:
    for y, line in enumerate (input):
        for x, char in enumerate(line.strip()):
            if char != ".":
                if char in antennas_pos:
                    antennas_pos[char].append((x+1, y+1))
                else:
                    antennas_pos[char] = [(x+1, y+1)]
        map_size = (len(line.strip()), y+1)    

part1()
part2()