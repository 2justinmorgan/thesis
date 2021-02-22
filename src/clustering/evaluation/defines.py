
import platform
import json
import sqlalchemy

HOME_DIRS = {
    "linux": "/home/jmorga27/Thesis",
    "windows": "c:/dev/thesis"
}

# ENV can be linux, windows, etc
ENV = platform.system().lower()
DIR = HOME_DIRS[ENV]
DB_CONFIGS = json.load(open(f"{DIR}/src/db_connect.json"))


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


class Cluster(Locker):
    def init_user_freqs_obj(self, user_names):
        obj = {}
        for user_name in user_names:
            obj[user_name] = 0
        return obj

    def __init__(self, cluster_id, user_names, _inherited=False):
        assert isinstance(cluster_id, str)
        assert isinstance(user_names, list)
        super().__init__()
        self.cluster_id = cluster_id
        self.intra_dist_mean = 0.0
        self.intra_dist_stdev = 0.0
        self.user_freqs = self.init_user_freqs_obj(user_names)
        self.setlock(_inherited)


class Evaluation(Locker):
    def init_clusters_obj(self, cluster_ids, user_names):
        clusters_obj = {}
        for cluster_id in cluster_ids:
            clusters_obj[cluster_id] = Cluster(cluster_id=cluster_id, user_names=user_names)
        return clusters_obj

    def __init__(self, clustering_desc, cluster_ids, user_names, _inherited=False):
        assert isinstance(clustering_desc, str)
        assert isinstance(cluster_ids, list)
        assert isinstance(user_names, list)
        super().__init__()
        self.clustering_desc = clustering_desc
        self.clusters_populations_mean = 0.0
        self.clusters_populations_stdev = 0.0
        self.clusters = self.init_clusters_obj(cluster_ids, user_names)
        self.setlock(_inherited)


class DBConnect(Locker):
    def exec(self, statement):
        return self.engine.execute(statement)

    def __init__(self, db_name, _inherited=False):
        assert isinstance(db_name, str)
        super().__init__()
        self.name = db_name
        self.engine = sqlalchemy.create_engine(DB_CONFIGS[db_name]["connection_strings"][ENV])
        self.target_table_names = DB_CONFIGS[db_name]["table_groups"]["cluster_distances"]
        self.setlock(_inherited)
