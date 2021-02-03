
gen_features_script_filepath="./gen_features.py";
raw_data_dirs=( \
	"../datasets/raw_data/set1" \
	"../datasets/raw_data/set2");

if [[ ! -f $gen_features_script_filepath ]]; then
	>&2 echo "$gen_features_script_filepath script not found";
	exit 1;
fi

for raw_data_dir in ${raw_data_dirs[@]}; do
	if [[ ! -d $raw_data_dir ]]; then
		>&2 echo "$raw_data_dir source dir not found";
		exit 1;
	fi

	for user_csv in $(ls $raw_data_dir); do
		echo $user_csv;
		session_filepath="${raw_data_dir}/${user_csv}";
		winpty python3 $gen_features_script_filepath $session_filepath;
	done
done
