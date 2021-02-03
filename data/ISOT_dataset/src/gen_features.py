import sys
import math
import statistics
import copy
import commons
import formatout
import defines

defines.MAIN_FILE = __file__.split('/')[-1]

FEATURES = defines.FEATURES
Csv_Vector = defines.Csv_Vector


def get_val(feature_name, csv_vector):

    if feature_name == "velocity":
        return csv_vector.traveled_distance / csv_vector.elapsed_time if csv_vector.elapsed_time else 0

    if feature_name == "angle":
        return csv_vector.direction_of_movement

    return -1


def record_features(session):
    mouse_data_file = commons.safe_open(session.input_data_filepath)
    mouse_data_file.readline()

    for line in mouse_data_file:
        for feature in FEATURES:
            feature_val = get_val(feature, Csv_Vector(line))
            session.features[feature].add_record(feature_val)


def main(argc, argv):
    mouse_data_file_path = commons.check_args(argc, argv)
    session = commons.get_session(mouse_data_file_path)

    record_features(session)

    formatout.store(session)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)

