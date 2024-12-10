top_reached = set()
def walk_trail(pos):
	height = topomap[pos[0]][pos[1]]
	if height == 9:
		top_reached.add(pos)
	else:
		if pos[0]-1 >= 0 and topomap[pos[0]-1][pos[1]] == height+1:
			walk_trail((pos[0]-1, pos[1]))
		if pos[0]+1 < topo_height and topomap[pos[0]+1][pos[1]] == height+1:
			walk_trail((pos[0]+1, pos[1]))
		if pos[1]-1 >= 0 and topomap[pos[0]][pos[1]-1] == height+1:
			walk_trail((pos[0], pos[1]-1))
		if pos[1]+1 < topo_width and topomap[pos[0]][pos[1]+1] == height+1:
			walk_trail((pos[0], pos[1]+1))

def part1():
	score = 0
	for trailhead in trailheads:
		walk_trail(trailhead)
		score += len(top_reached)
		top_reached.clear()
	print(score)


rating = 1
def walk_trail2(pos):
	global rating
	height = topomap[pos[0]][pos[1]]

	if height < 9:
		nb_paths = 0
		if pos[0]-1 >= 0 and topomap[pos[0]-1][pos[1]] == height+1:
			nb_paths += 1
			walk_trail2((pos[0]-1, pos[1]))
		if pos[0]+1 < topo_height and topomap[pos[0]+1][pos[1]] == height+1:
			nb_paths += 1
			walk_trail2((pos[0]+1, pos[1]))
		if pos[1]-1 >= 0 and topomap[pos[0]][pos[1]-1] == height+1:
			nb_paths += 1
			walk_trail2((pos[0], pos[1]-1))
		if pos[1]+1 < topo_width and topomap[pos[0]][pos[1]+1] == height+1:
			nb_paths += 1
			walk_trail2((pos[0], pos[1]+1))
		if nb_paths > 0:
			rating += nb_paths-1
		else:
			if height != 9:
				rating -= 1

def part2():
	global rating
	total_rating = 0
	for trailhead in trailheads:
		walk_trail2(trailhead)
		total_rating += rating
		rating = 1
	print(total_rating)

topomap = []
with open("day10.txt", "r") as input:
	for i, line in enumerate(input):
		intline = []
		for char in line.strip():
			if char == ".":
				intline.append(2)
			else:
				intline.append(int(char))
		topomap.append(intline)

topo_width = len(topomap[0])
topo_height = len(topomap)

trailheads = []
for i in range(topo_width):
	for j in range(topo_height):
		if topomap[i][j] == 0:
			trailheads.append((i, j))

part1()
part2()