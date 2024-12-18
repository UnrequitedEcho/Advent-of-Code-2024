A = 0
B = 0
C = 0
PROGRAM = []
IP = 0
OUTPUT = ""

with open("input.txt") as input:
	for i, line in enumerate(input):
		if line.startswith("Register"):
			if line.split()[1].startswith("A"):
				A = int(line.split()[2].strip())
			elif line.split()[1].startswith("B"):
				B = int(line.split()[2].strip())
			elif line.split()[1].startswith("C"):
				C = int(line.split()[2].strip())
		if line.startswith("Program"):
			Program_as_str = line.split()[1].split(",")
			PROGRAM = [int(x) for x in Program_as_str]

def get_combo_operand(code):
	if code <=3:
		return code
	elif code == 4:
		return A
	elif code == 5:
		return B
	elif code == 6:
		return C
	else:
		return "err"

def execute_instruction():
	global A, B, C, IP, OUTPUT
	operand = PROGRAM[IP+1]
	#print(IP, PROGRAM[IP], operand, A, B, C)

	match PROGRAM[IP]:
		case 0: # adv
			operand = get_combo_operand(operand)
			if operand == "err":
				return False
			A = A // (2 ** operand)
		case 1: # bxl
			B = B ^ operand
		case 2: # bst
			operand = get_combo_operand(operand)
			if operand == "err":
				return False
			B = operand % 8
		case 3: # jnz
			if A != 0:
				IP = operand
				return True
		case 4: # bxc
			B = B ^ C
		case 5: # out
			operand = get_combo_operand(operand)
			if operand == "err":
				return False
			result = operand % 8
			print(result, end=",")
		case 6: # bdv
			operand = get_combo_operand(operand)
			if operand == "err":
				return False
			B = A // (2 ** operand)
		case 7: # cdv
			operand = get_combo_operand(operand)
			if operand == "err":
				return False
			C = A // (2 ** operand)

	IP += 2
	if IP > len(PROGRAM) - 1:
		print("")
		return False
	return True

while execute_instruction():
	pass

# 2,4,1,2,7,5,1,3,4,3,5,5,0,3,3,0
# 2,4 : B = A % 8
# 1,2 : B = B ^ 2
# 7,5 : C = A // (1 << B)
# 1,3 : B = B ^ 3
# 4,3 : B = B ^ C
# 5,5 : Print(B % 8)
# 0,3 : A = A // 8
# 3.0 : Goto(0)

# Print (((A % 8) ^ 2) ^ 3) ^ (A // (1 << ((A % 8) ^ 2)))
# A = A // 8

# Program will only ever output 0 and exit if A == i.
for i in range(1000):
	res = ((((i % 8) ^ 2) ^ 3) ^ (i // (1 << ((i % 8) ^ 2)))) % 8
	if res == 0 and i // 8 == 0:
		pass
		#print(i)

# Turns out the only last A possible is 1
# So the right A is smaller than 7 ** 15. Great !

prog = [2,4,1,2,7,5,1,3,4,3,5,5,0,3,3,0]
old_possibilities = [1]
for i in range(1, 16):
	possibilities = []
	for p in old_possibilities:
		for j in range(p*8, p*8 + 8):
			res = ((((j % 8) ^ 2) ^ 3) ^ (j // (1 << ((j % 8) ^ 2)))) % 8
			if res == prog[len(prog)-1-i]:
				#print(i, "(", prog[len(prog)-1-i], ")", j)
				possibilities.append(j)
	
	old_possibilities = possibilities
print(min(old_possibilities))

