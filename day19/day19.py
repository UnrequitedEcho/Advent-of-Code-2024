from functools import cache

available = []
wishs = []
with open("input.txt") as input:
	for i, line in enumerate(input):
		if i == 0:
			available = [a.strip() for a in line.strip().split(",")]
		else:
			if line.strip():
				wishs.append(line.strip())

@cache
def is_elements(string):
	start = []

	for a in available:
		if string.startswith(a):
			if len(string) == len(a):
				return True
			else:
				start.append(a)
	if start:
		return any([is_elements(string[len(s):]) for s in start])
	else:
		return False

'''
@cache
def cached_pc(string):
	print(string, cached_pc.cache_info())
	total = 0
	result = []
	for a in available:
		if string.startswith(a):
			if len(string) == len(a):
				total += 1
			else:
				result.append(a)
	return result, total


def possible_combinations(string, total):
	start, tot = cached_pc(string)
	total += tot

	# for a in available:
	# 	if string.startswith(a):
	# 		if len(string) == len(a):
	# 			total += 1
	# 		else:
	# 			start.append(a)



	if start:
		for s in start:
			total = possible_combinations(string[len(s):], total)

	return total


'''

total_cache = {}
def possible_combinations(string, total):
	global total_cache
	start =[]

	if string in total_cache:
		total = total_cache[string]

	else:
		total = 0
		for a in available:
			if string.startswith(a):
				if len(string) == len(a):
					total += 1
				else:
					start.append(a)
		



		if start:
			for s in start:
				total += possible_combinations(string[len(s):], total)
	total_cache[string] = total

	
	return total

possible = 0
for wish in wishs:
	if is_elements(wish):
		possible += 1
print(possible)

total_possible = 0
for wish in wishs:
	total_possible += possible_combinations(wish, 0)
	print(wish, total_cache)

print(total_possible)