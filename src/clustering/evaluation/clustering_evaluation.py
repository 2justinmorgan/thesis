
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


def evaluate(table_name):
    evaluation = defines.Evaluation(
        clustering_desc=table_name,
        cluster_ids=get_cluster_ids(table_name),
        user_names=get_users(table_name))

    #result = db.exec(f"select distinct [user] from {table_name}")
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


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
