import sys


def print_usage(exit_program):
    print(f"Usage: {__file__.split('/')[-1]} <mouse_data_file>")
    if exit_program:
        sys.exit(0)


def check_args(argc, argv):
    if argc != 2:
        print_usage(1)
    return argv[1]


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


def output_clean_data(mouse_data_file_path):
    mouse_data_file = safe_open(mouse_data_file_path)
    prev_client_timestamp = 0.0

    for line in mouse_data_file:
        # record timestamp,client timestamp,button,state,x,y
        line_lst = line.split(',')
        client_timestamp = float(line_lst[1])
        if client_timestamp != prev_client_timestamp:
            sys.stdout.write(line)
        prev_client_timestamp = client_timestamp


def main(argc, argv):
    mouse_data_file_path = check_args(argc, argv)
    output_clean_data(mouse_data_file_path)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
