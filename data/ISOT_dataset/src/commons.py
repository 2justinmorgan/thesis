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


def is_path(path, exit_on_fail=False, exit_code=1):
    valid = os.path.isdir(path) or os.path.isfile(path)
    if not valid:
        sys.stderr.write(f"{path} not found\n")
        if exit_on_fail:
            sys.exit(exit_code)

    return valid


def line_count(filepath):
    if not is_path(filepath):
        return 0
    return sum(1 for l in open(filepath))


def init_features_obj(num_of_records=0):
    features = {}
    for feature_name in defines.FEATURES:
        features[feature_name] = defines.Feature(feature_name, num_of_records=num_of_records)
    return features


def get_session(filepath):
    filepath_lst = filepath.split('/')
    try:
        user = filepath_lst[-1].split('_')[1].split('.')[0]
        session_id = filepath_lst[-1].split('_')[0]
    except Exception as e:
        sys.stderr.write(f"Unable to get session info\n")
        sys.stderr.write(f"{e}")
        sys.exit(1)

    return Session(user=user, id=session_id, input_data_filepath=filepath)


def get_user_obj(target_filepath):
    if not os.path.isfile(target_filepath):
        user_file = open(target_filepath, "w")
        json.dump({}, user_file)
        user_file.close()
    return json.load(open(target_filepath, "r"))


def safe_open(file_path):
    try:
        f = open(file_path, 'r')
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)
    return f


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

