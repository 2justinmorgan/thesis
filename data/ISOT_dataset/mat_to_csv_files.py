
import sys
import ntpath
import csv
import scipy.io

def usage():
    sys.stderr.write(f"Usage: {ntpath.basename(__file__)} <mat_file>\n")


def safe_open(filepath, mode="r"):
    try:
        f = open(filepath, mode)
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)
    return f


def check_args(argc, argv):
    if argc != 2:
        usage()
        sys.exit(1)

    return safe_open(argv[1])


def main(argc, argv):
    mat_filepath = check_args(argc, argv)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
    
