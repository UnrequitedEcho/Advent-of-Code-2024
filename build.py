from pathlib import Path
import argparse
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("first", help="first day to build, only day if last is not specified", type=int)
parser.add_argument("-l", "--last", help="will build every day from first to last included", type=int)
parser.add_argument("-pr", "--profileRelease", help="build without debug info and with -O2", action="store_true")
parser.add_argument("-r", "--run", help="run after building", action="store_true")
args = parser.parse_args()

if args.last and args.last > args.first:
    work_on_day = [i for i in range(args.first, args.last + 1)]
else:
    work_on_day = [args.first]

for day in work_on_day:
    source = Path(Path(__file__).parent.as_posix() + "/Day" + str(day) + "/day" + str(day) + ".cpp")
    object_file = Path(source).with_suffix(".o")
    output = Path(source).with_suffix("")

    build_error = True
    link_error = True
    
    print("Building day" + str(day) + ".cpp ...")
    if args.profileRelease:
        build_error = subprocess.call(["g++", "-c", source.as_posix(), "-o", object_file.as_posix(), "-O2"])
    else:
        build_error = subprocess.call(["g++", "-c", source.as_posix(), "-o", object_file.as_posix(), "-g", "-Og", "-Wall", "-Wextra"])
    if build_error:
        print("Build Error : ", build_error)
        exit()
    
    print("Linking day" + str(day) + ".o ...")
    link_error = subprocess.call(["g++", object_file.as_posix(), "-o", output])
    if link_error:
        print("Link Error : ", link_error)
        object_file.unlink(missing_ok = True)
        exit()
    object_file.unlink()
    
    if args.run:
        result = subprocess.call([output.as_posix()])

