claw_machines = []
with open("input.txt") as input:
	while True:
		claw_machine = {}
		line1 = input.readline().strip()
		line2 = input.readline().strip()
		line3 = input.readline().strip()

		line1 = line1[10:]
		claw_machine["Ax"] = int(line1.split(",")[0][2:])
		claw_machine["Ay"] = int(line1.split(",")[1][3:])

		line2 = line2[10:]
		claw_machine["Bx"] = int(line2.split(",")[0][2:])
		claw_machine["By"] = int(line2.split(",")[1][3:])

		line3 = line3[7:]
		claw_machine["Px"] = int(line3.split(",")[0][2:])
		claw_machine["Py"] = int(line3.split(",")[1][3:])
		claw_machines.append(claw_machine)

		if not input.readline():
			break

# Part 1 : Kept the bruteforce method for posterity's sake, but it would obviously be
# faster with the Part2 method
total_tokens = 0
for cm in claw_machines:
	fewest_tokens = 0
	for a in range(100):
		for b in range(100):
			if a * cm["Ax"] + b * cm["Bx"] == cm["Px"]:
				if a * cm["Ay"] + b * cm["By"] == cm["Py"]:
					tokens = a * 3 + b
					if tokens < fewest_tokens or fewest_tokens == 0:
						fewest_tokens = tokens
	total_tokens += fewest_tokens

print(total_tokens)


# Edit data for Part 2
for cm in claw_machines:
	cm["Px"] += 10000000000000
	cm["Py"] += 10000000000000


# Part 2 : Solve the linear equation system with the inverse matrix multiply method
# I could have imported numpy, but it has been ages since i did it manually and it is a good reminder

# linear equations :
# a*Ax + b*Bx = Px
# a*Ay + b*By = Py

# Corresponding matrices :
#| Ax Bx | | Px |
#| Ay By | | Py |

total_tokens = 0
for cm in claw_machines:
	Py = cm["Py"]
	Px = cm["Px"]
	Ax = cm["Ax"]
	Ay = cm["Ay"]
	Bx = cm["Bx"]
	By = cm["By"]

	# Determinant
	det = (Ax * By) - (Bx * Ay)
	# Inverse Matrix
	i_Ax = By / det
	i_Bx = -Bx / det
	i_Ay = -Ay / det
	i_By = Ax / det
	# Dot Product
	a = (i_Ax * Px) + (i_Bx * Py)
	b = (i_Ay * Px) + (i_By * Py)

	epsilon = 0.001
	print(a, b)
	if round(a) > a - epsilon and round(a) < a + epsilon:
		if round(b) > b - epsilon and round(b) < b + epsilon:
			a = round(a)
			b = round(b)

			total_tokens += a * 3 + b

print(total_tokens)