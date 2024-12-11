package main

import "core:fmt"
import "core:os"
import "core:strings"
import "core:strconv"
import "core:slice"

part1 :: proc(array1: []int, array2: []int) -> (distance: int) {
	slice.sort(array1)
	slice.sort(array2)
	for _, i in array1 {
		distance += abs(array2[i] - array1[i])
	}
	return distance
}

part2 :: proc(array1: []int, array2: []int) -> (similarity: int) {
	for v in array1 {
		similarity += v * slice.count(array2, v)
	}
	return similarity
}

main :: proc() {
	infile, ok := os.read_entire_file("day1.txt")
	if !ok {
		os.exit(1)
	}
	defer delete(infile)
	input := string(infile)

	array1 := [dynamic]int{}
	defer delete(array1)
	array2 := [dynamic]int{}
	defer delete(array2)

	for line in strings.split_lines_iterator(&input) {
		nb, ok := strconv.parse_int(line[:5])
		if ok {
			append_elem(&array1, nb)
		}
		nb, ok = strconv.parse_int(line[len(line)-5:])
		if ok {
			append_elem(&array2, nb)
		}
	}

	fmt.println(part1(array1[:], array2[:]))
	fmt.println(part2(array1[:], array2[:]))
}
