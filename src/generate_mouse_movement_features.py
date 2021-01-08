import math
import statistics
import sys
import copy

FEATURES = [
    "velocity",
    "xvelocity",
    "yvelocity",
    "acceleration",
    "jerk",
    "theta"
]

METRICS = {
    "all": [],
    "stats": {
        "stdev": 0.0,
        "mean": 0.0,
        "range": []
    }
}


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TPoint(Point):
    def __init__(self, x, y, time):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.time = time

    @staticmethod
    def list_to_tpoint(tpoint_list):
        x = tpoint_list[0]
        y = tpoint_list[1]
        time = tpoint_list[2]
        return TPoint(x, y, time)


def print_usage(exit_program):
    print(f"Usage: {__file__.split('/')[-1]} <mouse_data_file>")
    if exit_program:
        sys.exit(0)


def check_args(argc, argv):
    if argc != 2:
        print_usage(1)
    return argv[1]


def hello(name):
    return "hello " + str(name)


def write_stdout(content):
    sys.stdout.write(content)


def theta(point_a, point_b):
    delta_x = abs(point_a[0] - point_b[0])
    delta_y = abs(point_a[1] - point_b[1])
    return math.atan2(delta_y, delta_x)


def velocity(axis, tpoint_a, tpoint_b):
    if axis != 'x' and axis != 'y' and axis != 'xy':
        return -1

    if axis == 'xy':
        x_velocity = velocity('x', tpoint_a, tpoint_b)
        y_velocity = velocity('y', tpoint_a, tpoint_b)
        return (x_velocity ** 2 + y_velocity ** 2) ** .5

    delta_axis = 0
    if axis == 'x':
        delta_axis = abs(tpoint_a.x - tpoint_b.x)
    if axis == 'y':
        delta_axis = abs(tpoint_a.y - tpoint_b.y)

    delta_t = abs(tpoint_a.time - tpoint_b.time)
    return delta_axis / delta_t if delta_t else 0


def get_val(feature_name, tpoints):
    #
    # need case that returns if feature_name is invalid
    #
    if "velocity" in feature_name:
        if feature_name == "velocity":
            return velocity("xy", tpoints[0], tpoints[1])
        # the first arg, axis, can be 'x' or 'y'
        return velocity(feature_name[0], tpoints[0], tpoints[1])

    if feature_name == "acceleration":
        velocity_a = velocity('xy', tpoints[0], tpoints[1])
        velocity_b = velocity('xy', tpoints[2], tpoints[3])
        delta_t = abs(tpoints[0].time - tpoints[3].time)
        return abs(velocity_a - velocity_b) / delta_t if delta_t else 0

    if feature_name == "jerk":
        acceleration_a = get_val("acceleration", tpoints[:4])
        acceleration_b = get_val("acceleration", tpoints[4:])
        delta_t = abs(tpoints[0].time - tpoints[7].time)
        return abs(acceleration_a - acceleration_b) / delta_t if delta_t else 0

    if feature_name == "theta":
        delta_y = abs(tpoints[0].y - tpoints[1].y)
        delta_x = abs(tpoints[0].x - tpoints[1].x)
        return delta_y / delta_x if delta_x else 0

    return -1


def read_nlines(file_obj, n):
    lines_list = [""] * n
    for i in range(n):
        try:
            lines_list[i] = file_obj.readline()
        except Exception as e:
            sys.stderr.write(e)
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


def get_tpoint(csv_line_str):
    # description: record timestamp,client timestamp,button,state,x,y
    # input (str):
    # 291.082999945,291.082,NoButton,Move,544,594
    # output (TPoint):
    # TPoint(544, 594, 291.082)

    csv_line_list = csv_line_str.split(',')
    tpoint_str_list = [csv_line_list[4], csv_line_list[5], csv_line_list[1]]
    tpoint = TPoint.list_to_tpoint([float(e) for e in tpoint_str_list])
    return tpoint


def init_features_obj():
    features_obj = {}
    for feature in FEATURES:
        features_obj[feature] = copy.deepcopy(METRICS)
    return features_obj


def record_features(mouse_data_file_path):
    mouse_data_file = safe_open(mouse_data_file_path)
    features_obj = init_features_obj()
    tpoints = [get_tpoint(e) for e in read_nlines(mouse_data_file, 8)]

    for line in mouse_data_file:
        for feature in FEATURES:
            feature_val = get_val(feature, tpoints)
            features_obj[feature]["all"].append(feature_val)
        tpoints.pop(0)
        tpoints.append(get_tpoint(line))

    return features_obj


def insert_stats(features_obj):
    stats_metrics = list(METRICS.keys()).remove("all")
    for feature in features_obj:
        vals = features_obj[feature]["all"]
        stats_obj = features_obj[feature]["stats"]
        stats_obj["stdev"] = statistics.stdev(vals)
        stats_obj["mean"] = statistics.fmean(vals)
        stats_obj["range"] = [min(vals), max(vals)]


def format_print(features_obj):
    for feature in features_obj:
        print(feature)
        for stat in features_obj[feature]["stats"]:
            val = features_obj[feature]["stats"][stat]
            sys.stdout.write(f" {stat}:")
            if type(val) == list:
                for e in val:
                    e = round(e, 2)
                    sys.stdout.write(f"{e} ")
            else:
                val = round(val, 2)
                sys.stdout.write(f"{val}")
        print()


if __name__ == "__main__":
    mouse_data_file_path = check_args(len(sys.argv), sys.argv)
    features_obj = record_features(mouse_data_file_path)
    insert_stats(features_obj)
    format_print(features_obj)
    import json

    outfile = open('features.json', 'w')
    json.dump(features_obj, outfile)
