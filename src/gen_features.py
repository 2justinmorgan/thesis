import sys
import math
import statistics
import copy
import commons
import formatout
import defines

defines.MAIN_FILE = __file__.split('/')[-1]

FEATURES = defines.FEATURES
Feature = defines.Feature
TPoint = defines.TPoint


def theta(point_a, point_b):
    delta_x = abs(point_a.x - point_b.x)
    delta_y = abs(point_a.y - point_b.y)
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
        return theta(tpoints[0], tpoints[1])

    return -1


def get_tpoint(csv_line_str):
    # description: record timestamp,client timestamp,button,state,x,y
    # input (str):
    # 291.082999945,291.082,NoButton,Move,544,594
    # output (TPoint):
    # TPoint(544, 594, 291.082)

    csv_line_list = csv_line_str.split(',')
    return TPoint(csv_line_list[4], csv_line_list[5], csv_line_list[1])


def record_features(session):
    mouse_data_file = commons.safe_open(session.input_data_filepath)
    tpoints = [get_tpoint(e) for e in commons.read_nlines(mouse_data_file, 8)]

    for line in mouse_data_file:
        for feature in FEATURES:
            feature_val = round(get_val(feature, tpoints), 6)
            session.features[feature].add(feature_val)
        tpoints.pop(0)
        tpoints.append(get_tpoint(line))


def soften_records(floats_list):
    softened_list = copy.deepcopy(floats_list)
    i = 0
    while i < len(softened_list):
        float_num = round(softened_list[i], 6)

        if float_num <= 0:
            softened_list.pop(i)
            continue

        num_left_digits = commons.num_digits(float_num)
        num_leading_zero_right_digits = commons.num_zero_decimal_digits(float_num)
        if num_left_digits > 0:
            float_num = round(float_num, -1 * (num_left_digits - 2))
        else:
            float_num = round(float_num, (num_leading_zero_right_digits + 2))

        softened_list[i] = float_num
        i += 1

    return softened_list


def get_mode(floats_list):
    clean_floats_list = soften_records(floats_list)
    frequencies = {}
    max_frequency = 0
    mode = 0
    for float_num in clean_floats_list:
        float_key = round(float_num, 6)
        if float_key not in frequencies:
            frequencies[float_key] = 0
            continue
        frequencies[float_key] += 1
        if frequencies[float_key] > max_frequency:
            max_frequency = frequencies[float_key]
            mode = float_num

    return mode


def insert_stats(features_obj):
    rnd = 7
    for feature in features_obj:
        records = features_obj[feature].records
        features_obj[feature].stats.mean = round(statistics.fmean(records), rnd)
        features_obj[feature].stats.median = round(statistics.median(records), rnd)
        features_obj[feature].stats.mode = round(get_mode(records), rnd)
        features_obj[feature].stats.stdev = round(statistics.stdev(records), rnd)
        positive_numbers = [r for r in records if r > 0]
        features_obj[feature].stats.range = defines.Range(round(min(positive_numbers), rnd), round(max(records), rnd))


def hello(name):
    return "hello " + str(name)


def write_stdout(content):
    sys.stdout.write(content)


def main(argc, argv):
    mouse_data_file_path = commons.check_args(argc, argv)
    session = commons.get_session(mouse_data_file_path)

    record_features(session)
    insert_stats(session.features)

    #formatout.format_print(features_obj)
    formatout.create_json(session)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
