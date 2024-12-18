package main

import "core:fmt"


execute :: proc(PROGRAM: []int, OUTPUT: []int, A: int) {
	OUT_INDEX: int = 0
	OPERAND: int = 0
	A := A
	IP:= 0
	B := 0
	C := 0

	for {
		switch PROGRAM[IP+1] {
				case 0..=3:
					OPERAND = PROGRAM[IP+1]
				case 4:
					OPERAND = A
				case 5:
					OPERAND = B
				case 6:
					OPERAND = C
			}

		switch PROGRAM[IP] {
			case 0:
				if PROGRAM[IP+1] == 7 { return }
				A = A / (1 << cast(uint)OPERAND)
			case 1:
				B = B ~ PROGRAM[IP+1]
			case 2:
				if PROGRAM[IP+1] == 7 { return }
				B = OPERAND % 8
			case 3:
				if A != 0 {
					IP = PROGRAM[IP+1]
					continue
				}
			case 4:
				B = B ~ C
			case 5:
				if PROGRAM[IP+1] == 7 {return }
				if OUT_INDEX >= len(OUTPUT) { return }
				OUTPUT[OUT_INDEX] = OPERAND % 8
				OUT_INDEX += 1
			case 6:
				if PROGRAM[IP+1] == 7 { return }
				B = A / (1 << cast(uint)OPERAND)
			case 7:
				if PROGRAM[IP+1] == 7 { return }
				C = A / (1 << cast(uint)OPERAND)
		}

		IP += 2
		if IP >= len(PROGRAM) { return }
	}
}

main :: proc() {
	PROGRAM := [?]int{2,4,1,2,7,5,1,3,4,3,5,5,0,3,3,0}
	OUTPUT := 0
	OUT_INDEX: int = 0
	OPERAND: int = 0
	IP:= 0
	A := 0
	B := 0
	C := 0
	i := 0
	
	main: for {
		i+= 1
		A = i
		B = 0
		C = 0
		IP = 0
		OUTPUT = 0
		OUT_INDEX = 0
		OPERAND = 0

		if A % 1_000_000 == 0 {
			fmt.println(A)
		}

		prog_loop: for {
			switch PROGRAM[IP+1] {
					case 0..=3:
						OPERAND = PROGRAM[IP+1]
					case 4:
						OPERAND = A
					case 5:
						OPERAND = B
					case 6:
						OPERAND = C
				}

			switch PROGRAM[IP] {
				case 0:
					if PROGRAM[IP+1] == 7 { break prog_loop }
					A = A / (1 << cast(uint)OPERAND)
				case 1:
					B = B ~ PROGRAM[IP+1]
				case 2:
					if PROGRAM[IP+1] == 7 { break prog_loop }
					B = OPERAND % 8
				case 3:
					if A != 0 {
						IP = PROGRAM[IP+1]
						continue
					}
				case 4:
					B = B ~ C
				case 5:
					if PROGRAM[IP+1] == 7 {break prog_loop }
					OUTPUT := OPERAND % 8
					if OUTPUT != PROGRAM[OUT_INDEX] {
						break prog_loop
					}
					OUT_INDEX += 1
					if OUT_INDEX >= 15 { 
						break main
					}
				case 6:
					if PROGRAM[IP+1] == 7 { break prog_loop }
					B = A / (1 << cast(uint)OPERAND)
				case 7:
					if PROGRAM[IP+1] == 7 { break prog_loop }
					C = A / (1 << cast(uint)OPERAND)
			}

			IP += 2
			if IP >= len(PROGRAM) { break prog_loop }
		}
	}
	fmt.println(i)
}