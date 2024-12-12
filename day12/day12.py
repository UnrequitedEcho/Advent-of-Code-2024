# I refuse to believe this is an optimal solution...
from collections import Counter

garden_map = []
with open("day12.txt") as input:
	for line in input:
		garden_map.append(line.strip())

already_assigned = set()
regions = []

for y, line in enumerate(garden_map):
	for x, plant_type in enumerate(line):
		if (y, x) in already_assigned:
			continue
		regions.append([(y, x)])
		already_assigned.add((y, x))
		plots_to_check = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
		while plots_to_check:
			plot = plots_to_check[-1]
			plots_to_check  = plots_to_check[:-1]
			if plot in already_assigned:
				continue
			if plot[0] < 0 or plot[0] >= len(garden_map):
				continue
			if plot[1] < 0 or plot[1] >= len(garden_map[0]):
				continue
			if garden_map[plot[0]][plot[1]] != plant_type:
				continue
			regions[-1].append(plot)
			already_assigned.add(plot)
			plots_to_check += [(plot[0]-1, plot[1]), (plot[0]+1, plot[1]), (plot[0], plot[1]-1), (plot[0], plot[1]+1)]

# Part 1
fences = []
for region in regions:
	fences.append(0)
	for plot in region:
		adjacent_plots = []
		for maybe_adjacent in region:
			if maybe_adjacent == plot:
				continue
			if maybe_adjacent[0] == plot[0] and (maybe_adjacent[1] == plot[1]+1 or maybe_adjacent[1] == plot[1]-1):
				adjacent_plots.append(maybe_adjacent)
				continue
			if maybe_adjacent[1] == plot[1] and (maybe_adjacent[0] == plot[0]+1 or maybe_adjacent[0] == plot[0]-1):
				adjacent_plots.append(maybe_adjacent)
				continue

		fences[-1] += 4 - len(adjacent_plots)

price = 0
for f, r in zip(fences, regions):
	price += f * len(r)
print(price)

# Part 2
class Point():
	def __init__(self, y, x):
		self.y = y
		self.x = x
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

class Segment():
	def __init__(self, p1, p2):
		if (p2.x > p1.x) or (p2.y > p1.y):
			self.p1 = p1
			self.p2 = p2
		else:
			self.p1 = p2
			self.p2 = p1

	def is_horizontal(self):
		if self.p1.x == self.p2.x:
			return True

	def __repr__(self):
		return "Segment : " + str(self.p1.y) + "," + str(self.p1.x) + "-" + str(self.p2.y) + "," + str(self.p2.x)

fences = []
for region in regions:
	print("New Region")
	segments = set()
	for plot in region:
		adjacent_plots = []
		for maybe_adjacent in region:
			if maybe_adjacent == plot:
				continue
			if maybe_adjacent[0] == plot[0] and (maybe_adjacent[1] == plot[1]+1 or maybe_adjacent[1] == plot[1]-1):
				adjacent_plots.append(maybe_adjacent)
				continue
			if maybe_adjacent[1] == plot[1] and (maybe_adjacent[0] == plot[0]+1 or maybe_adjacent[0] == plot[0]-1):
				adjacent_plots.append(maybe_adjacent)
				continue
		TL = Point(plot[0], plot[1])
		BL = Point(plot[0]+1, plot[1])
		TR = Point(plot[0], plot[1]+1)
		BR = Point(plot[0]+1, plot[1]+1)
		if (plot[0]-1, plot[1]) not in adjacent_plots: # above
			segments.add(Segment(TL, TR))
		if (plot[0]+1, plot[1]) not in adjacent_plots: # below
			segments.add(Segment(BL, BR))
		if (plot[0], plot[1]-1) not in adjacent_plots: # left
			segments.add(Segment(TL, BL))
		if (plot[0], plot[1]+1) not in adjacent_plots: # right
			segments.add(Segment(TR, BR))
	old_segments = set()
	while len(segments) != len(old_segments):
		old_segments = segments.copy()
		try: 
			for segment1 in segments:
				for segment2 in segments:
					if segment1 == segment2:
						continue
					if segment1.p2 == segment2.p1: # point in commont
						# This is the check for moebius fencing corner case
						if ((segment1.p2.y, segment1.p2.x) not in region) and ((segment1.p2.y-1, segment1.p2.x-1) not in region):
							continue
						if ((segment1.p2.y-1, segment1.p2.x) not in region) and ((segment1.p2.y, segment1.p2.x-1) not in region):
							continue

						if (segment1.p1.x == segment2.p2.x) or (segment1.p1.y == segment2.p2.y):	# both horizontal or both vertical
							segment1.p2 = segment2.p2
							segments.remove(segment2)
							raise StopIteration
		except StopIteration:
			pass
	print(segments)
	fences.append(len(segments))



price = 0
for f, r in zip(fences, regions):
	price += f * len(r)
print(price)
