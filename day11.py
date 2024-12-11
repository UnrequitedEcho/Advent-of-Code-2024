from tqdm import tqdm

def blink(stones, blinks):
	for blink_nb in range(blinks):
		i = 0
		for i in range(len(stones)):
			stone = stones[i]
			stone_as_str = str(stone)
			stone_length = len(str(stone))
			if stone == 0:
				stones[i] = 1
			elif stone_length % 2 == 0:
				midpoint = stone_length // 2
				first_half = int(stone_as_str[:midpoint])
				second_half = int(stone_as_str[midpoint:])

				stones[i] = first_half
				stones.append(second_half)
			else :
				stones[i] = stone * 2024
	return stones

def part2(stones_as_lst, blinks):
	stones = {}
	for stone in stones_as_lst:
		if stone in stones:
			stones[stone] += 1
		else:
			stones[stone] = 1
	for blink_nb in tqdm(range(blinks)):
		next_stones = {}
		for stone in stones:
			result = blink([stone], 1)
			for next_stone in result:
				if next_stone in next_stones:
					next_stones[next_stone] += stones[stone]
				else:
					next_stones[next_stone] = stones[stone]
		stones = next_stones
	total = 0
	for stone in stones:
		total += stones[stone]
	print(total)



stones = []
with open("day11.txt", "r") as input:
	stones_as_str = input.read().strip()
for stone_as_str in stones_as_str.split():
	stones.append(int(stone_as_str))

part2(stones, 75)
#print(blink2(stones[:], 75))
