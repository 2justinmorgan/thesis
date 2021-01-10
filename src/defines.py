
MOUSE_DATA_FILE_ARGV_TITLE = "<mouse_data_file>"
RECORDED_FEATURES_DIR = "../data/recorded_features"
MAIN_FILE = ""  # defined in script with main func

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
    def __init__(self, user="", id="", _inherited=False):
        super().__init__()
        self.user = user
        self.id = id
        self.setlock(_inherited)


class Range(Locker):
    def __init__(self, low=0.0, high=0.0, _inherited=False):
        super().__init__()
        self.low = low
        self.high = high
        self.setlock(_inherited)


class Stats(Locker):
    def __init__(self, mean=0.0, median=0.0, mode=0.0, stdev=0.0, range=Range(), _inherited=False):
        super().__init__()
        self.mean = mean
        self.median = median
        self.mode = mode
        self.stdev = stdev
        self.range = range
        self.setlock(_inherited)


class Feature(Locker):
    def __init__(self, name="", _inherited=False):
        super().__init__()
        self.name = name
        self.stats = Stats()
        self.records = []
        self.setlock(_inherited)

    def add(self, record):
        self.records.append(record)
