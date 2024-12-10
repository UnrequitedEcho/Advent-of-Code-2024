#!/usr/bin/env python3

# This is an overly complicated solution for part 1.
# It creates diagonal strings to use the str.count() function on them
# So many off-by-one errors...

def part1(word_search):
    accumulator = 0
    # horizontal
    accumulator = 0
    for line in word_search:
        accumulator += line.count("XMAS")
        accumulator += line.count("SAMX")
    # vertical
    for column_index in range(len(word_search)):
        column = ''.join([line[column_index] for line in word_search])
        accumulator += column.count("XMAS")
        accumulator += column.count("SAMX")

    vertical_size = len(word_search)
    horizontal_size = len(word_search[0])
    # diagonal pi/4 rad
    for i in range(horizontal_size + vertical_size - 1):
        diagonal = ""
        for column, line in zip(range(0, horizontal_size), range(i, -1, -1)):
            if not line < 0 and not line > vertical_size - 1:
                diagonal += word_search[line][column]
        accumulator += diagonal.count("XMAS")
        accumulator += diagonal.count("SAMX")

    # diagonal 3pi/4 rad
    fliped_word_search = []
    for line in word_search:
        fliped_word_search.append(line[::-1])
    
    for i in range(horizontal_size + vertical_size - 1):
        diagonal = ""
        for column, line in zip(range(0, horizontal_size), range(i, -1, -1)):
            if not line < 0 and not line > vertical_size - 1:
                diagonal += fliped_word_search[line][column]
        accumulator += diagonal.count("XMAS")
        accumulator += diagonal.count("SAMX")
    print(accumulator)

def part2(word_search):
    accumulator = 0
    nblines = len(word_search)
    nbcols = len(word_search[0])
    for i in range(nblines):
        for j in range(nbcols):
            if word_search[i][j] == 'A' \
            and (i > 0 and i < nblines - 1) \
            and (j > 0 and j < nbcols - 1):
                top_left = word_search[i - 1][j - 1]
                top_right = word_search[i - 1][j + 1]
                bot_left = word_search[i + 1][j - 1]
                bot_right = word_search[i + 1][j + 1]

                if top_left == 'M' and bot_right == 'S' \
                or top_left == 'S' and bot_right == 'M':
                    if top_right == 'M' and bot_left == 'S' \
                    or top_right == 'S' and bot_left == 'M':
                        accumulator += 1

    print(accumulator)

word_search = []
with open("day4.txt", "r") as input:
    for line in input:
        word_search.append(line)

part1(word_search)
part2(word_search)
