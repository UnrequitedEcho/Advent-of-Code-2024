from copy import deepcopy
import enum

warehouse_h = 50
warehouse = []
instructions = ""
with open("input.txt") as input:
	for i, line in enumerate(input):
		if i < warehouse_h:
			line_as_arr = []
			for j in line.strip():
				line_as_arr.append(j)
			warehouse.append(line_as_arr)
		else:
			instructions += line.strip()

robot_pos = None
for i, line in enumerate(warehouse):
	for j, char in enumerate(line):
		if char == "@":
			warehouse[i][j] = "."
			robot_pos = (i, j)

def warehouse_print(wh, pos):
	for i, line in enumerate(wh):
		for j, char in enumerate(line):
			print("@" if (i, j) == pos else char, end="")
		print("")

def process_ahead(ahead):
	try:
		spaceIndex = ahead.index(".")
	except ValueError:
		return None
	for char in ahead[:spaceIndex]:
		if char == "#":
			return None	
	for i, char in enumerate(ahead[:spaceIndex+1]):
		ahead[i] = "O"
	ahead[0] = "."
	return ahead

def execute_instruction(instr, wh, pos):
	match instr:
		case ">":
			next_pos = wh[pos[0]][pos[1]+1]
			if next_pos == ".":
				return wh, (pos[0], pos[1]+1)
			elif next_pos == "#":
				return wh, pos
			else:
				ahead = wh[pos[0]][pos[1]+1:]
				ahead = process_ahead(ahead)
				if ahead is None:
					return wh, pos
				for i, char in enumerate(ahead):
					wh[pos[0]][pos[1]+1+i] = char
				return wh, (pos[0], pos[1]+1)
		case "<":
			next_pos = wh[pos[0]][pos[1]-1]
			if next_pos == ".":
				return wh, (pos[0], pos[1]-1)
			elif next_pos == "#":
				return wh, pos
			else:
				ahead = wh[pos[0]][pos[1]-1::-1]
				ahead = process_ahead(ahead)
				if ahead is None:
					return wh, pos
				for i, char in enumerate(ahead[::-1]):
					wh[pos[0]][i] = char
				return wh, (pos[0], pos[1]-1)
		case "^":
			next_pos = wh[pos[0]-1][pos[1]]
			if next_pos == ".":
				return wh, (pos[0]-1, pos[1])
			elif next_pos == "#":
				return wh, pos
			else:
				ahead = [line[pos[1]] for line in wh]
				ahead = ahead[pos[0]-1::-1]
				ahead = process_ahead(ahead)
				if ahead is None:
					return wh, pos
				for i, char in enumerate(ahead[::-1]):
					wh[i][pos[1]] = char
				return wh, (pos[0]-1, pos[1])
		case "v":
			next_pos = wh[pos[0]+1][pos[1]]
			if next_pos == ".":
				return wh, (pos[0]+1, pos[1])
			elif next_pos == "#":
				return wh, pos
			else:
				ahead = [line[pos[1]] for line in wh]
				ahead = ahead[pos[0]+1:]
				ahead = process_ahead(ahead)
				if ahead is None:
					return wh, pos
				for i, char in enumerate(ahead):
					wh[pos[0]+1+i][pos[1]] = char
				return wh, (pos[0]+1, pos[1])

def enlarge(wh, pos):
	large_wh = []
	for i, line in enumerate(wh):
		large_line = []
		for j, char in enumerate(line):
			match char:
				case "#":
					large_line += ["#", "#"]
				case "O":
					large_line += ["[", "]"]
				case ".":
					large_line += [".", "."]
		large_wh.append(large_line)
	return large_wh, (pos[0], pos[1]*2)


def execute_instruction2(instr, wh, pos):
	pl = pos[0]
	pc = pos[1]
	match instr:
		case ">":
			spaceIndex = 0
			for i, char in enumerate(wh[pl][pc+1:]):
				if char == "#":
					return wh, pos
				if char == ".":
					spaceIndex = i
					break
			for i in range(pc+1+spaceIndex, pc+1, -1):
				wh[pl][i] = wh[pl][i-1]
			wh[pl][pc] = '.'
			return wh, (pl, pc+1)

		case "<":
			spaceIndex = 0
			line = list(reversed(wh[pl][:pc]))
			for i, char in enumerate(line):
				if char == "#":
					return wh, pos
				if char == ".":
					spaceIndex = i
					break
			for i in range(pc-1-spaceIndex, pc-1, 1):
				wh[pl][i] = wh[pl][i+1]
			wh[pl][pc] = "."
			return wh, (pl, pc-1)

		case "^":
			char = wh[pl-1][pc]
			if char == "#":
				return wh, pos
			if char == ".":
				wh[pl][pc] = "."
				return wh, (pl-1, pc)
			
			boxes = []
			if char == "[":
				boxes.append((pl-1, pc))
			if char == "]":
				boxes.append((pl-1, pc-1))	
			for box in boxes:
				aboveL = wh[box[0]-1][box[1]]
				aboveR = wh[box[0]-1][box[1]+1]
				if aboveL == "." and aboveR == ".":
					continue
				if aboveL == "#" or aboveR == "#":
					return wh, pos
				if aboveL == "[":
					boxes.append((box[0]-1, box[1]))
				if aboveL == "]":
					boxes.append((box[0]-1, box[1]-1))
				if aboveR == "[":
					boxes.append((box[0]-1, box[1]+1))
			for box in boxes[::-1]:
				wh[box[0]-1][box[1]] = "["
				wh[box[0]-1][box[1]+1] = "]"
				wh[box[0]][box[1]] = "."
				wh[box[0]][box[1]+1] = "."
			wh[pl][pc] = "."
			return wh, (pl-1, pc)

		case "v":
			char = wh[pl+1][pc]
			if char == "#":
				return wh, pos
			if char == ".":
				wh[pl][pc] = "."
				return wh, (pl+1, pc)
			boxes = []
			if char == "[":
				boxes.append((pl+1, pc))
			if char == "]":
				boxes.append((pl+1, pc-1))
			
			for box in boxes:
				belowL = wh[box[0]+1][box[1]]
				belowR = wh[box[0]+1][box[1]+1]
				if belowL == "." and belowR == ".":
					continue
				if belowL == "#" or belowR == "#":
					return wh, pos
				if belowL == "[":
					boxes.append((box[0]+1, box[1]))
				if belowL == "]":
					boxes.append((box[0]+1, box[1]-1))
				if belowR == "[":
					boxes.append((box[0]+1, box[1]+1))
			for box in boxes[::-1]:
				wh[box[0]+1][box[1]] = "["
				wh[box[0]+1][box[1]+1] = "]"
				wh[box[0]][box[1]] = "."
				wh[box[0]][box[1]+1] = "."
			wh[pl][pc] = "."
			return wh, (pl+1, pc)


wh = deepcopy(warehouse)
pos = robot_pos
for inst in instructions:
	wh, pos = execute_instruction(inst, wh, pos)

solution = 0
for i, line in enumerate(wh):
	for j, char in enumerate(line):
		if char == "O":
			solution += 100 * i + j
print(solution)

wh = deepcopy(warehouse)
pos = robot_pos
wh, pos = enlarge(wh, pos)
warehouse_print(wh, pos)
for i, inst in enumerate(instructions):
	#print(inst, i)
	wh, pos = execute_instruction2(inst, wh, pos)
	#warehouse_print(wh, pos)
warehouse_print(wh, pos)
wh_l = len(wh[0])
wh_h = len(wh)
solution = 0
for i, line in enumerate(wh):
	for j, char in enumerate(line):
		if char == "[":
			solution += i*100 + j

print(solution)
