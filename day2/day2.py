#!/usr/bin/env python3

def is_report_safe(report):
    if report[0] == report[1]:
        return False
    report_is_increasing = report[0] < report[1]
    for level, next_level in zip(report, report[1:] + [None]):
        if next_level is None:
            return True
        level_difference = next_level - level
        if report_is_increasing:
            if level_difference < 1 or level_difference > 3:
                return False
        if not report_is_increasing:
            if level_difference < -3 or level_difference > -1:
                return False

def part1(reports):
    nb_safe = 0
    for report in reports:
        if is_report_safe(report):
            nb_safe += 1
    print(nb_safe)

def part2(reports):
    nb_safe = 0
    for report in reports:
        if is_report_safe(report):
            nb_safe += 1
            continue
        for i in range(len(report)):
            dampened_report = list(report)
            del (dampened_report[i])
            if is_report_safe(dampened_report):
                nb_safe += 1
                break

    print(nb_safe)

reports = []

with open("day2.txt", "r") as input:
    for line in input:
        reports.append(line.split())
        reports[-1] = [int(n) for n in reports[-1]]

part1(reports)
part2(reports)
