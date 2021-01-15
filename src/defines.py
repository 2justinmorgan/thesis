import commons

HOME_DIR = "/home/jmorga27/Thesis"
MOUSE_DATA_FILE_ARGV_TITLE = "<mouse_data_file>"
RECORDED_SESSIONS_DIR = f"{HOME_DIR}/data/recorded_features/sessions"
MAIN_FILE = ""  # defined in script with main func

FEATURES = [
    "velocity",
    "xvelocity",
    "yvelocity",
    "acceleration",
    "jerk",
    "theta"
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


class Point(Locker):
    def __init__(self, x, y, _inherited=False):
        super().__init__()
        self.x = x
        self.y = y
        self.setlock(_inherited)


class TPoint(Point, Locker):
    def __init__(self, x, y, time, _inherited=False):
        super().__init__(x, y, _inherited=True)
        self.x = int(x)
        self.y = int(y)
        self.time = float(time)
        self.setlock(_inherited)


class Session(Locker):
    def __init__(self, user="", id="", input_data_filepath="", _inherited=False):
        super().__init__()
        self.user = user
        self.id = id
        self.input_data_filepath = input_data_filepath
        self.features = commons.init_features_obj()
        self.setlock(_inherited)


class Feature(Locker):
    def __init__(self, name="", _inherited=False):
        super().__init__()
        self.name = name
        self.records = []
        self.setlock(_inherited)

    def add(self, record):
        self.records.append(record)
