import commons

HOME_DIR = "c:/dev/thesis"
MOUSE_DATA_FILE_ARGV_TITLE = "<mouse_data_file>"
RECORDED_SESSIONS_DIR = f"{HOME_DIR}/data/ISOT_dataset/datasets/recorded_features/sessions"
MAIN_FILE = ""  # defined in script with main func

FEATURES = [
    "velocity",
    "angle"
]


class Locker:
    __locked = False

    def __setattr__(self, key, val):
        if self.__locked and not hasattr(self, key):
            raise TypeError("%r does not allow setting new attributes after object instantiation" % self)
        if key == '_Locker__locked' and val != True:
            raise TypeError(f"Unable to Falsify the {key} attribute of %r instances" % self.__class__)
        object.__setattr__(self, key, val)

    def setlock(self, _inherited):
        if not _inherited:
            self._Locker__locked = True


class Csv_Vector(Locker):
    def __init__(self, csv_line_str, _inherited=False):
        # csv_vector: type-of-action, traveled-distance (pixels), elapsed-time, direction-of-movement
        l = csv_line_str.split(',')

        self.type_of_action = float(l[0])
        self.traveled_distance = float(l[1])
        self.elapsed_time = float(l[2])
        self.direction_of_movement = float(l[3])


class Session(Locker):
    def __init__(self, user="", id="", input_data_filepath="", _inherited=False):
        super().__init__()
        self.user = user
        self.id = id
        self.input_data_filepath = input_data_filepath
        self.features = commons.init_features_obj(num_of_records=commons.line_count(input_data_filepath))
        self.setlock(_inherited)


class Feature(Locker):
    def __init__(self, name="", num_of_records=0, _inherited=False):
        super().__init__()
        self.name = name
        self.records = [0.0]*num_of_records
        self.records_counter = 0
        self.setlock(_inherited)

    def add_record(self, record):
        self.records[self.records_counter] = record
        self.records_counter += 1

