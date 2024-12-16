from dataclasses import dataclass
from os import curdir

@dataclass
class Tile:
	l: int
	c: int
	orient: str
	score: int


maze = []
with open("input.txt") as input:
	for line in input:
		mazeline = []
		for char in line.strip():
			mazeline.append(char)
		maze.append(mazeline)

start_pos = None
end_pos = None
for i, line in enumerate(maze):
	for j, char in enumerate(line):
		if maze[i][j] == "S":
			start_pos = (i, j)
			maze[i][j] = "."
		if maze[i][j] == "E":
			end_pos = (i, j)
			maze[i][j] = "."

score = 0
seen = []
new_tiles = [Tile(start_pos[0], start_pos[1], ">", 0)]

while new_tiles:
	next_new_tiles = []
	for t in new_tiles:
		already_seen = False
		for s in seen:
			if s.l == t.l and s.c == t.c:
				if s.score < t.score:
					already_seen = True
				else:
					seen.remove(s)

		new_tiles.remove(t)
		if not already_seen:
			seen.append(t)

			if maze[t.l-1][t.c] == ".":
				score = t.score+1 if t.orient == "^" else t.score+1001
				next_new_tiles.append(Tile(t.l-1, t.c, "^", score))
			if maze[t.l+1][t.c] == ".":
				score = t.score+1 if t.orient == "v" else t.score+1001
				next_new_tiles.append(Tile(t.l+1, t.c, "v", score))
			if maze[t.l][t.c-1] == ".":
				score = t.score+1 if t.orient == "<" else t.score+1001
				next_new_tiles.append(Tile(t.l, t.c-1, "<", score))
			if maze[t.l][t.c+1] == ".":
				score = t.score+1 if t.orient == ">" else t.score+1001
				next_new_tiles.append(Tile(t.l, t.c+1, ">", score))
	new_tiles += next_new_tiles 

last_tile = None
for s in seen:
	if s.l == end_pos[0] and s.c == end_pos[1]:
		print(s.score)
		last_tile = s



visited = set()
visited.add((last_tile.l, last_tile.c))
prev_l = 0
prev_c = 0
if last_tile.orient == "^":
	prev_l = last_tile.l + 1
	prev_c = last_tile.c
if last_tile.orient == "v":
	prev_l = last_tile.l - 1
	prev_c = last_tile.c
if last_tile.orient == "<":
	prev_c = last_tile.c + 1
	prev_l = last_tile.l
if last_tile.orient == ">":
	prev_c = last_tile.c - 1
	prev_l = last_tile.l
prev_last_tile = None
for s in seen:
	if s.l == prev_l and s.c == prev_c:
		prev_last_tile = s
		break
visited.add((prev_last_tile.l, prev_last_tile.c))
heads = [(prev_last_tile, last_tile)]
while heads:
	tile = heads[0][0]
	prev = heads[0][1]

	adjacent = []
	for s in seen:
		if s.l == tile.l-1 and s.c == tile.c \
		or s.l == tile.l+1 and s.c == tile.c \
		or s.l == tile.l and s.c == tile.c-1 \
		or s.l == tile.l and s.c == tile.c+1 :
			if s != prev:
				adjacent.append(s)

	print(prev)
	print(tile)
	print(adjacent)

	for a in list(adjacent):	
		score = a.score+2 if a.orient == prev.orient else a.score+1002
		if score != prev.score:
			adjacent.remove(a)


	for a in adjacent:
		heads.append((a, tile))

	visited.add((tile.l, tile.c))
	heads = heads[1:]


print(len(visited))
