from pathlib import Path
from tqdm import tqdm

def checksum(disk_map):
    checksum = 0
    for i, x in enumerate(disk_map):
        if x is not None:
            checksum += i*x
    return checksum

def Part1(disk_map2):
    new_disk_map2 = []
    for x in disk_map2:
        if x is not None:
            new_disk_map2.append(x)
            disk_map2 = disk_map2[1:]
        else:
            while disk_map2[-1] is None:
                disk_map2 = disk_map2[:-1]
            new_disk_map2.append(disk_map2[-1])
            disk_map2 = disk_map2[1:-1]
        if not disk_map2:
            break
    print(checksum(new_disk_map2))

def Part2(disk_map3):
    files_length = {}
    for x in [y for y in disk_map3 if y is not None]:
        if x in files_length:
            files_length[x] += 1
        else:
            files_length[x] = 1
    space = 0

    for f_id in tqdm(reversed(sorted(files_length.keys()))):
        '''for item in disk_map3:
            if item is None:
                print(".", end="")
            else:
                print(item, end="")
        print("")'''
        f_length = files_length[f_id]
        for i, x in enumerate(disk_map3):
            if x is None:
                space = 0
                while disk_map3[i + space] is None:
                    if i + space >= len(disk_map3) - 1:
                        break
                    space += 1

                if space >= f_length:
                    replacement = [f_id] * f_length + [None] * (space - f_length)
                    disk_map3 = disk_map3[:i] + replacement + disk_map3[i+len(replacement):]
                    disk_map3 = disk_map3[:i+len(replacement)] + [None if y == f_id else y for y in disk_map3[i+len(replacement):]]
                    del files_length[f_id]
                    break
            elif x == f_id:
                break
    print(checksum(disk_map3))


disk_map_as_str = ""
disk_map = []

with open(Path(__file__).parent / "input.txt", "r") as input:
    disk_map_as_str  = input.read().strip()

disk_map = [int(c) for c in disk_map_as_str]
new_disk_map = []

f_id = 0
for i, x in enumerate(disk_map):
    if i%2 == 0:
        c_f_id = f_id
        f_id += 1
    else:
        c_f_id = None
    for i in range(0, x):
        new_disk_map.append(c_f_id)

Part1(list(new_disk_map))
Part2(new_disk_map)
