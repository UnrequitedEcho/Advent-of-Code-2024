package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Yet again, I am amazed that this is not in the standard library !
func copy_map(input map[int]int)(copy map[int]int){
	copy = make(map[int]int)
	for k, v := range input {
		copy[k] = v
	}
	return copy
}

func blink_once(stone int)(result []int){
	if stone == 0 {
		result = append(result, 1)
	} else if len(strconv.Itoa(stone)) % 2 == 0 {
		stone_as_str := strconv.Itoa(stone)
		midpoint := len(stone_as_str) / 2
		first_half, _ := strconv.Atoi(stone_as_str[:midpoint])
		second_half, _ := strconv.Atoi(stone_as_str[midpoint:])
		result = append(result, first_half)
		result = append(result, second_half)
	} else {
		result = append(result, stone * 2024)
	}
	return result
}

func blink_multiple(stones map[int]int, blinks int){
	for i:=0; i<blinks; i++ {
		next_stones := make(map[int]int)
		for stone, stone_quantity := range stones {
			blink_results := blink_once(stone)
			for _, result := range blink_results {
				next_stones[result] = next_stones[result] + stone_quantity
			}
		}
		stones = next_stones
	}
	solution := 0
	for _, stone_quantity := range stones {
		solution += stone_quantity
	}
	fmt.Println(solution)
}

func main() {
	inFile, err := os.ReadFile("day11.txt")
	if err != nil {
		panic(err)
	}
	stones_as_strs := strings.Split(string(inFile), " ")
	stones := make(map[int]int, 0)
	for _, str := range stones_as_strs {
		stone_as_int, _ := strconv.Atoi(str)
		stones[stone_as_int] = 1
	}

	stones_copy := copy_map(stones)
	blink_multiple(stones_copy, 25)
	stones_copy = copy_map(stones)
	blink_multiple(stones_copy, 75)
}