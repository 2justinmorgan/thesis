
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


def get_user_freq_bias_metric(cluster, total_num_sessions, total_num_clusters):
    sorted_users_by_freq = sorted(cluster.user_freqs, key=cluster.user_freqs.get, reverse=True)
    weight = len(cluster.user_freqs)-2
    weighted_diffs = []
    for i in range(len(cluster.user_freqs)-1):
        percentage_a = cluster.user_freqs[sorted_users_by_freq[i]] / cluster.population_count
        percentage_b = cluster.user_freqs[sorted_users_by_freq[i+1]] / cluster.population_count
        weighted_diffs.append((percentage_a - percentage_b) * weight)
        weight -= 1
    avg_num_session_per_cluster = total_num_sessions / total_num_clusters
    diff_from_avg = abs(avg_num_session_per_cluster - cluster.population_count)
    return sum(weighted_diffs) / diff_from_avg if diff_from_avg > 0 else sum(weighted_diffs)


def get_total_num_sessions(table_name):
    result = DB.exec(f"select count(*) from {table_name}")
    return result.first()[0]


def tally_user_frequencies(clusters, table_name):
    total_num_sessions = get_total_num_sessions(table_name)
    total_num_clusters = len(clusters)
    for cluster_id in clusters:
        cluster = clusters[cluster_id]
        for user_name in cluster.user_freqs:
            result = DB.exec(
                f"select count(*) from {table_name} "
                f"where cluster = {cluster_id} and "
                f"[user] = '{user_name}'")
            user_freq_count = result.first()[0]
            cluster.user_freqs[user_name] += user_freq_count
            cluster.population_count += user_freq_count

        cluster.user_freqs = {k: v for k, v in sorted(cluster.user_freqs.items(), key=lambda i: i[1], reverse=True)}
        cluster.user_freq_bias_metric = get_user_freq_bias_metric(cluster, total_num_sessions, total_num_clusters)


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
    clusters_populations_counts = []
    clusters_user_freq_bias_metrics = []
    for cluster in evaluation.clusters.items():
        clusters_populations_counts.append(cluster[1].population_count)
        clusters_user_freq_bias_metrics.append(cluster[1].user_freq_bias_metric)

    evaluation.clusters_populations_mean = statistics.fmean(clusters_populations_counts)
    evaluation.clusters_populations_stdev = statistics.stdev(clusters_populations_counts)
    evaluation.clusters_populations_range["min"] = min(clusters_populations_counts)
    evaluation.clusters_populations_range["max"] = max(clusters_populations_counts)
    evaluation.clusters_user_freq_bias_metric_median = statistics.median(clusters_user_freq_bias_metrics)


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

    tally_user_frequencies(evaluation.clusters, table_name)
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

    for cname in evaluations:
        clusters = evaluations[cname].clusters

        max_users = {}
        for level in range(10):
            level_users = {}
            for cluster_id in clusters:
                cluster = clusters[cluster_id]
                top_user_name = list(cluster.user_freqs.keys())[level]
                freq = cluster.user_freqs[top_user_name]
                level_user_freq = level_users.get(top_user_name, 0)
                if top_user_name not in max_users and freq > level_user_freq:
                    max_users[top_user_name] = f"{freq}|{cluster_id}"

        print(cname)
        print(max_users)
        print(cname + "\n")

    #print(to_json(evaluations))
    f = open(f"{defines.DIR}/src/clustering/evaluation/out.json", "w")
    json.dump(json.loads(to_json(evaluations)), f, indent=2)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
