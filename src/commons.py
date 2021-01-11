import sys
import os
import json
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


def get_user_obj(target_filepath):
    if not os.path.isfile(target_filepath):
        user_file = open(target_filepath, "w")
        json.dump({}, user_file)
        user_file.close()
    return json.load(open(target_filepath, "r"))


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


def num_digits(float_num, to_left_of_decimal=True):
    float_num = round(float_num, 6)

    if to_left_of_decimal:
        num_digits_to_the_left = 0
        while int(float_num) >= 1:
            float_num *= 0.1
            num_digits_to_the_left += 1
        return num_digits_to_the_left

    num_digits_to_the_right = 0
    while float_num - int(float_num) > 0:
        float_num = round(float_num*10, 9-num_digits_to_the_right)
        num_digits_to_the_right += 1
    return num_digits_to_the_right


def num_zero_decimal_digits(float_num):
    if float_num == 0 or float_num == int(float_num):
        return 0

    decimal_number = round(abs(float_num - int(float_num)), 6)
    whole_number = int(decimal_number)
    num_zero_decimal_digits_to_the_right = -1

    while whole_number <= 0:
        decimal_number *= 10
        whole_number = int(decimal_number)
        num_zero_decimal_digits_to_the_right += 1

    return num_zero_decimal_digits_to_the_right


def rkey(key, d):
    for k in d:
        if isinstance(d[k], dict):
            rkey(key, d[k])
    if key in d:
        d.pop(key, None)


def class_obj_to_dict(class_obj, keys_to_remove=None):
    d = json.loads(json.dumps(class_obj, default=lambda o: getattr(o, '__dict__', str(o))))

    keys_to_remove = keys_to_remove if keys_to_remove else []
    for key in keys_to_remove:
        rkey(key, d)

    return d
