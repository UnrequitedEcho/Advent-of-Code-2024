import os
from copy import deepcopy
from dataclasses import dataclass

area_height = 103
area_width = 101
robots = []

@dataclass
class Point:
	x: int
	y: int

@dataclass
class Robot:
	p: Point
	v: Point

def robot_tick_once(robot):
	robot.p.x += robot.v.x
	robot.p.y += robot.v.y
	if robot.p.x > area_width-1:
		robot.p.x -= area_width
	if robot.p.x < 0:
		robot.p.x += area_width
	if robot.p.y > area_height-1:
		robot.p.y -= area_height
	if robot.p.y < 0:
		robot.p.y += area_height

def print_robots(robots):
	os.system("clear")
	coords = [robot.p for robot in robots]
	for i in range(area_width - 1):
		for j in range(area_height - 1):
			print("." if Point(j, i) not in coords else "X", end="")
		print("")

def part1(robots):
	for _ in range(100):
		for robot in robots:
			robot_tick_once(robot)

	TL = 0
	TR = 0
	BL = 0
	BR = 0
	for robot in robots:
		if robot.p.x < area_width // 2 and robot.p.y < area_height // 2:
			TL += 1
		if robot.p.x > area_width // 2 and robot.p.y < area_height // 2:
			TR += 1
		if robot.p.x < area_width // 2 and robot.p.y > area_height // 2:
			BL += 1
		if robot.p.x > area_width // 2 and robot.p.y > area_height // 2:
			BR += 1
	print(TL*TR*BL*BR)

# for Part2, I tried a bunch of things that did not work. In the end, I quantified how
# "clustered" were the robots, and print their position  when clustering is high.
# That way I could actually see the christmas tree !
def part2(robots):
	i = 0
	old_total_cluster = 0
	while True:
		for robot in robots:
			robot_tick_once(robot)
		i += 1

		total_cluster = 0
		for robot in robots:
			dist = 1
			cluster = 0
			for robot2 in robots:
				if robot2 == robot:
					continue
				if robot2.p.x >= robot.p.x - dist and robot2.p.x <= robot.p.x + dist:
					if robot2.p.y >= robot.p.y - dist and robot2.p.y <= robot.p.y + dist:
						cluster += 1
			total_cluster += cluster

		if total_cluster > old_total_cluster:
			old_total_cluster = total_cluster
			print_robots(robots)
			print(i)
		if total_cluster > 1000:
			break

robots = []
with open("input.txt") as input:
	for line in input:
		p, v = line.strip().split(" ")
		p = p[2:].split(",")
		v = v[2:].split(",")
		robots.append(Robot(Point(int(p[0]), int(p[1])), Point(int(v[0]), int(v[1]))))

part1(deepcopy(robots))
part2(deepcopy(robots))
