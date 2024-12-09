from pathlib import Path
import argparse
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("day_nb", help="number of the day to build", type=int)
parser.add_argument("-pr", "--profileRelease", help="build without debug info and with -O2", action="store_true")
parser.add_argument("-r", "--run", help="run after building", action="store_true")
args = parser.parse_args()

day = str(args.day_nb)
path = Path(__file__).parent
source = path / ("day" + day + ".cpp")
object_file = path / ("day" + day + ".o")
output = path / ("day" + day)

print("Building day" + day + ".cpp ...")
if args.profileRelease:
    compil_args = ["g++", "-c", str(source), "-o", str(object_file), "-O2"]
else:
    compil_args = ["g++", "-c", str(source), "-o", str(object_file), "-g", "-Og", "-Wall", "-Wextra"]
result = subprocess.run(compil_args)

if result.returncode != 0:
    exit()

print("Linking day" + day + ".o ...")
result = subprocess.run(["g++", str(object_file), "-o", str(output)])

Path(str(object_file)).unlink(missing_ok=True)

if result.returncode == 0 and args.run:
    result = subprocess.run(str(output))

