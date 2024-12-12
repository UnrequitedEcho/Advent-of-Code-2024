# I refuse to believe this is an optimal solution...
from collections import Counter

garden_map = []
with open("day12.txt") as input:
	for line in input:
		garden_map.append(line.strip())

already_assigned = set()
regions = []
# Populates regions, a list of plots of the same plant type
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

part1_fences = []
part2_fences = []
for region in regions:
	segments = set()
	for plot in region:
		# generate the list of adjacent plots
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
		# add the fences around each plot if there is no adjacent one
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

	part1_fences.append(len(segments))

	# for part 2, we merge the fences when 1.they have a point in common 2. they are both vertical or both horizontal 3. they aren't delimiting the moebius fencing case
	old_segments = set()
	while len(segments) != len(old_segments):
		old_segments = segments.copy()
		try: 
			for segment1 in segments:
				for segment2 in segments:
					if segment1 == segment2:
						continue
					# point in common
					if segment1.p2 == segment2.p1: 
						# This is the check for moebius fencing corner case
						if ((segment1.p2.y, segment1.p2.x) not in region) and ((segment1.p2.y-1, segment1.p2.x-1) not in region):
							continue
						if ((segment1.p2.y-1, segment1.p2.x) not in region) and ((segment1.p2.y, segment1.p2.x-1) not in region):
							continue

						# both horizontal or both vertical
						if (segment1.p1.x == segment2.p2.x) or (segment1.p1.y == segment2.p2.y):
							segment1.p2 = segment2.p2
							segments.remove(segment2)
							raise StopIteration
		except StopIteration:
			pass
	part2_fences.append(len(segments))


price = 0
for f, r in zip(part1_fences, regions):
	price += f * len(r)
print(price)

price = 0
for f, r in zip(part2_fences, regions):
	price += f * len(r)
print(price)