
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


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TPoint(Point):
    def __init__(self, x, y, time):
        super().__init__(x, y)
        self.x = int(x)
        self.y = int(y)
        self.time = float(time)


class Session:
    def __init__(self, user="", id=""):
        self.user = user
        self.id = id


class Range:
    def __init__(self, low=0.0, high=0.0):
        self.low = low
        self.high = high


class Stats:
    def __init__(self, mean=0.0, median=0.0, mode=0.0, stdev=0.0, range=Range()):
        self.mean = mean
        self.median = median
        self.mode = mode
        self.stdev = stdev
        self.range = range


class Feature:
    def __init__(self, name=""):
        self.name = name
        self.stats = Stats()
        self.records = []

    def add(self, record):
        self.records.append(record)
