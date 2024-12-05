from pathlib import Path
import math

def is_page_well_placed(page, page_ordering_rules, update):
    pages_that_should_precede = [por[0] for por in page_ordering_rules if page == por[1]]
    pages_that_should_follow = [por[1] for por in page_ordering_rules if page == por[0]]
    for page_that_should_precede in pages_that_should_precede:
        if page_that_should_precede not in update:
            continue
        if update.index(page_that_should_precede) > update.index(page):
            return False
    for page_that_should_follow in pages_that_should_follow:
        if page_that_should_follow not in update:
            continue
        if update.index(page_that_should_follow) < update.index(page):
            return False
    return True

def is_update_well_ordered(update, page_ordering_rules):
    for page in update:
        if not is_page_well_placed(page, page_ordering_rules, update):
             return False
    return True

def order_update(update, page_ordering_rules):
    ordered_update = []
    for current_page in update:
        pages_that_should_precede = [por[0] for por in page_ordering_rules if current_page == por[1]]
        pages_that_should_follow = [por[1] for por in page_ordering_rules if current_page == por[0]]
        try:
            min_index = max([i for i, page in enumerate(ordered_update) if page in pages_that_should_precede]) + 1
        except ValueError:
            min_index = 0
        try: 
            max_index = min([i for i, page in enumerate(ordered_update) if page in pages_that_should_follow])
        except ValueError:
            max_index = 0 if not ordered_update else len(ordered_update)
        if min_index > max_index:
            print("Uh oh... : ")
        else:
            ordered_update.insert(min_index, current_page)
    return ordered_update

def part1(page_ordering_rules, page_numbers):
    accumulator = 0
    for update in page_numbers:
        if is_update_well_ordered(update, page_ordering_rules):
            accumulator += update[math.floor(len(update) / 2)]
    print(accumulator)

def part2(page_ordering_rules, page_numbers):
    accumulator = 0
    for update in page_numbers:
        if not is_update_well_ordered(update, page_ordering_rules):
            update = order_update(update, page_ordering_rules)
            accumulator += update[math.floor(len(update) / 2)]
    print(accumulator)

with open(Path(__file__).parent / "input.txt", "r") as input:
    page_ordering_rules = []
    page_numbers = []
    for line in input:
        if "|" in line:
            page_ordering_rules.append([int(x) for x in line.split("|")])
        if "," in line:
            page_numbers.append([int(x) for x in line.split(",")])

part1(page_ordering_rules, page_numbers)
part2(page_ordering_rules, page_numbers)