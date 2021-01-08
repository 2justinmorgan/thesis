
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
