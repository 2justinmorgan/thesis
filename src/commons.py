import sys


def read_nlines(file_obj, n):
    lines_list = [""] * n
    for i in range(n):
        try:
            lines_list[i] = file_obj.readline()
        except Exception as e:
            sys.stderr.write(str(e))
            return lines_list

    return lines_list


def safe_open(file_path):
    try:
        f = open(file_path, 'r')
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)
    read_nlines(f, 1)
    return f
