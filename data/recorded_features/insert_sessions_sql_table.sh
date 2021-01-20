
sessions_json_filepath="./all_sessions_stats.json";
mapped_sessions_json_filepath="./mapped_sessions.json";
output_insert_csv_filepath="/var/lib/mysql-files/sql_insert.csv";

FEATURES=(\"velocity\", \"xvelocity\", \"yvelocity\", \"acceleration\", \"jerk\", \"theta\");
STATS=(\"mean\", \"median\", \"mode\", \"iqr\", \"stdev\", \"min\", \"max\", \"range\");

python3 << EOF
import json
output_file = open("$output_insert_csv_filepath", "w")
sessions = json.load(open("$sessions_json_filepath", "r"))
session_map = json.load(open("$mapped_sessions_json_filepath", "r"))
for session in sessions:
	for stat in [${STATS[@]}]:
		# insert into sessions (stat,session,user,velocity,xvelocity,yvelocity,acceleration,jerk,theta) values (...
		output_file.write(f"{stat},{session},{session_map[session]}")
		for feature in [${FEATURES[@]}]:
			output_file.write(f",{round(sessions[session][feature][stat], 6)}")
		output_file.write("\n")
output_file.close()
EOF

mysql << EOF
use mouse_movement;
load data infile '$output_insert_csv_filepath'
into table csv_sessions
fields terminated by ','
lines terminated by '\n';
EOF

rm $output_insert_csv_filepath;
