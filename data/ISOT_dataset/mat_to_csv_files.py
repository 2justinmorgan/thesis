
import sys
import os
import ntpath
import csv
import scipy.io
import numpy as np

TARGET_DIR = "./datasets"


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

    return argv[1]


def write_csv_files(users_dict):
    for user_name in users_dict:
        if type(users_dict[user_name]) != np.ndarray:
            continue

        set_name = user_name.split('_')[0]
        if not os.path.isdir(f"{TARGET_DIR}/{set_name}"):
            sys.stderr.write(f"{TARGET_DIR}/{set_name} dir not found")
            sys.exit(1)

        print(f"{user_name}")
        csv_file = open(f"{TARGET_DIR}/{set_name}/{user_name}.csv", "w")
        csv_file.write(f"type-of-action,traveled-distance,elapsed-time,direction-of-movement\n")
        for row in users_dict[user_name]:
            csv_file.write("%s," % row[0])
            csv_file.write("%s," % row[1])
            csv_file.write("%s," % row[2])
            csv_file.write("%s" % row[3])
            csv_file.write("\n")


def main(argc, argv):
    mat_filepath = check_args(argc, argv)

    users_dict = scipy.io.loadmat(mat_filepath)

    write_csv_files(users_dict)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
    
