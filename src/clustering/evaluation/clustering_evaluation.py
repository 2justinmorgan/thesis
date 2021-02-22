
import sys
import json
import jsonpickle
import statistics
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
            user_frequency_count = result.first()[0]
            cluster.user_freqs[user_name] += user_frequency_count
            cluster.population_count += user_frequency_count


def measure_intra_distances(clusters, table_name):
    for cluster_id in clusters:
        cluster = clusters[cluster_id]
        result = DB.exec(
            f"select Distance from {table_name} "
            f"where Cluster = {cluster_id}"
        )
        count = 0
        intra_distances = []
        for row in result:
            count += 1
            intra_distances.append(row["Distance"])
        cluster.intra_dist_mean = statistics.fmean(intra_distances)
        cluster.intra_dist_stdev = statistics.stdev(intra_distances) if count >= 2 else 0.0


def analyze_clusters_populations(evaluation, table_name):
    clusters_populations_counts = [cluster[1].population_count for cluster in evaluation.clusters.items()]

    evaluation.clusters_populations_mean = statistics.fmean(clusters_populations_counts)
    evaluation.clusters_populations_stdev = statistics.stdev(clusters_populations_counts)
    evaluation.clusters_populations_range["min"] = min(clusters_populations_counts)
    evaluation.clusters_populations_range["max"] = max(clusters_populations_counts)


def analyze_clusters_intra_distances(evaluation, table_name):
    clusters_mean_intra_distances = []
    clusters_stdev_intra_distances = []
    for cluster in evaluation.clusters.items():
        clusters_mean_intra_distances.append(cluster[1].intra_dist_mean)
        clusters_stdev_intra_distances.append(cluster[1].intra_dist_stdev)
    evaluation.clusters_intra_dist_mean_mean = statistics.fmean(clusters_mean_intra_distances)
    evaluation.clusters_intra_dist_mean_stdev = statistics.stdev(clusters_mean_intra_distances)
    evaluation.clusters_intra_dist_stdev_mean = statistics.fmean(clusters_stdev_intra_distances)
    evaluation.clusters_intra_dist_stdev_stdev = statistics.stdev(clusters_stdev_intra_distances)


def evaluate(table_name):
    user_names = get_users(table_name)
    cluster_ids = get_cluster_ids(table_name)

    evaluation = defines.Evaluation(
        clustering_desc=table_name,
        cluster_ids=cluster_ids,
        user_names=user_names)

    tally_frequencies(user_names, evaluation.clusters, table_name)
    measure_intra_distances(evaluation.clusters, table_name)
    analyze_clusters_intra_distances(evaluation, table_name)
    analyze_clusters_populations(evaluation, table_name)

    return evaluation


def evaluate_clusters(db):
    evaluations = {}
    for table_name in db.target_table_names:
        evaluations[table_name] = evaluate(table_name)
    return evaluations


def main(argc, argv):
    evaluations = evaluate_clusters(DB)

    #print(to_json(evaluations))
    f = open(f"{defines.DIR}/src/clustering/evaluation/out.json", "w")
    json.dump(json.loads(to_json(evaluations)), f, indent=2)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
