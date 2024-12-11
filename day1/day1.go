package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"slices"
)

func part1(array1 []int, array2 []int)(distance int){
	slices.Sort(array1)
	slices.Sort(array2)

	for i, _ := range array1 {
		dist := array2[i] - array1[i]
		// Amazingly, it seems there is no built-in abs function for ints...
		if dist > 0 { 
			distance += dist
		} else {
			distance += -dist
		}
	}
	return distance
}

func part2(array1 []int, array2 []int) (similarity int) {
	for _, v := range(array1) {
		nb_occurences := 0
		// ... and no built-in way to count the number of a specific element in a slice
		for _, w := range(array2){
			if v == w {
				nb_occurences += 1
			}
		}
		similarity += v * nb_occurences
	}
	return similarity
}

func main(){
	inFile, err := os.Open("day1.txt")
	if err != nil {
		panic(err)
	}
	defer inFile.Close()
	scanner := bufio.NewScanner(inFile)

	array1 := make([]int, 0)
	array2 := make([]int, 0)

	for scanner.Scan() {
		line := scanner.Text()
		nb, err := strconv.Atoi(line[:5])
		if err == nil{
			array1 = append(array1, nb)
		}
		
		nb, err = strconv.Atoi(line[len(line)-5:])
		if err == nil {
			array2 = append(array2, nb)
		}
	}

	
	fmt.Println(part1(array1[:],array2[:]))
	fmt.Println(part2(array1,array2))
}