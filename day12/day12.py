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
