import sys
import defines

Session = defines.Session


def print_usage(exit_program):
    sys.stderr.write(f"Usage: {defines.MAIN_FILE} {defines.MOUSE_DATA_FILE_ARGV_TITLE}\n")
    if exit_program:
        sys.exit(1)


def check_args(argc, argv):
    if argc != 2:
        print_usage(1)
    if "user" not in argv[1] and "session" not in argv[1]:
        sys.stderr.write(f"{defines.MOUSE_DATA_FILE_ARGV_TITLE} must have \"user\" and \"session\" in its filepath\n")
        sys.exit(1)
    return argv[1]


def get_session(filepath):
    filepath_lst = filepath.split('/')
    user = ""
    session_id = ""
    for element in filepath_lst:
        if "user" in element:
            user = element
        if "session" in element:
            session_id = element

    if len(user) <= 0 or len(session_id) <= 0:
        sys.stderr.write(f"Unable to get session info\n")
        sys.exit(1)

    return Session(user, session_id)


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
