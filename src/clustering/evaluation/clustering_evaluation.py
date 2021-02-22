
import sys
import json
import jsonpickle
import defines

DB = defines.DBConnect(db_name="mouse_movement")


def to_json(class_obj):
    serialized = jsonpickle.encode(class_obj)
    return json.dumps(json.loads(serialized), indent=2)


def get_users(table_name):
    users_list = []
    for row in DB.exec(f"select distinct [user] from {table_name}"):
        users_list.append(row["user"])
    return users_list


def get_cluster_ids(table_name):
    users_list = []
    for row in DB.exec(f"select distinct Cluster from {table_name}"):
        users_list.append(row["Cluster"])
    return users_list


def tally_frequencies(user_names, clusters, table_name):
    for cluster_id in clusters:
        cluster = clusters[cluster_id]
        for user_name in cluster.user_freqs:
            result = DB.exec(
                f"select count(*) from {table_name} "
                f"where cluster = {cluster_id} and "
                f"[user] = '{user_name}'")
            cluster.user_freqs[user_name] += result.first()[0]


def evaluate(table_name):
    user_names = get_users(table_name)
    cluster_ids = get_cluster_ids(table_name)

    evaluation = defines.Evaluation(
        clustering_desc=table_name,
        cluster_ids=cluster_ids,
        user_names=user_names)

    tally_frequencies(user_names, evaluation.clusters, table_name)
    #measure_intra_distances(evaluation.clusters)

    #result = DB.exec(f"select distinct [user] from {table_name}")
    #for row in result:
    #    print(f"user: {row['user']}")
    return evaluation


def evaluate_clusters(db):
    evaluations = {}
    for table_name in db.target_table_names:
        evaluations[table_name] = evaluate(table_name)
    return evaluations


def main(argc, argv):
    evaluations = evaluate_clusters(DB)

    print(to_json(evaluations))
    f = open(f"{defines.DIR}/src/clustering/evaluation/out.json", "w")
    json.dump(json.loads(to_json(evaluations)), f, indent=2)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
