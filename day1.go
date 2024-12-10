package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"slices"
)

func absInt(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func parseInput()(list1 []int, list2 []int){
	inFile, err := os.Open("day1.txt")
	if err != nil {
		fmt.Println(err.Error())
		panic(err)
	}
	defer inFile.Close()

	scanner := bufio.NewScanner(inFile)
	for scanner.Scan() {
		line := scanner.Text()
		nb1, err := strconv.Atoi(line[:5])
		if err != nil{
			fmt.Println("Parsing Error")
			panic(err)
		}
		list1 = append(list1, nb1)
		nb2, err := strconv.Atoi(line[len(line)-5:])
		if err != nil {
			fmt.Println("Parsing Error")
			panic(err)
		}
		list2 = append(list2, nb2)
	}
	return list1, list2
}

func part1(list1 []int, list2 []int)(result int){
	for len(list1) > 0 {
		min1 := slices.Min(list1)
		min2 := slices.Min(list2)
		result += absInt(min1 - min2)
		for i, v := range(list1) {
			if v == min1 {
				list1[i] = list1[len(list1)-1]
				list1 = list1[:len(list1)-1]
				break
			} 
		}
		for i, v := range(list2) {
			if v == min2 {
				list2[i] = list2[len(list2)-1]
				list2 = list2[:len(list2)-1]
				break
			} 
		}
	}
	return result
}

func part2(list1 []int, list2 []int) (result int) {
	for _, v := range(list1) {
		nb_occurences := 0
		for _, w := range(list2){
			if v == w {
				nb_occurences += 1
			}
		}
		result += v * nb_occurences
	}
	return result
}

func main(){
	list1, list2 := parseInput()
	list1copy := make([]int, len(list1))
	list2copy := make([]int, len(list2))
	copy(list1copy, list1)
	copy(list2copy, list2)
	fmt.Println(part1(list1copy,list2copy))
	fmt.Println(part2(list1,list2))
}