def blink_once(stone):
	if stone == 0:
		return [1]

	elif len(str(stone)) % 2 == 0:
		stone_as_str = str(stone)
		midpoint = len(stone_as_str) // 2
		first_half = int(stone_as_str[:midpoint])
		second_half = int(stone_as_str[midpoint:])
		return [first_half, second_half]

	else :
		return [stone * 2024]

def blink_multiple(stones, blinks):
	for _ in range(blinks):
		next_stones = {}
		for stone in stones:
			blink_results = blink_once(stone)
			for result in blink_results:
				if result in next_stones:
					next_stones[result] += stones[stone]
				else:
					next_stones[result] = stones[stone]
		stones = next_stones
	print(sum(stones.values()))

with open("day11.txt", "r") as input:
	stones_as_str = input.read().strip()
stones = {int(k): 1 for k in stones_as_str.split()}

blink_multiple(stones.copy(), 25)
blink_multiple(stones.copy(), 75)
