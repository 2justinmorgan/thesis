
gen_features_script_filepath="../../src/gen_features.py";
clean_data_dirs=( \
	"../clean_mouse_data/test_files" \
	"../clean_mouse_data/training_files");

if [[ ! -f $gen_features_script_filepath ]]; then
	>&2 echo "$gen_features_script_filepath script not found";
	exit 1;
fi

for clean_data_dir in ${clean_data_dirs[@]}; do
	if [[ ! -d $clean_data_dir ]]; then
		>&2 echo "$clean_data_dir source dir not found";
		exit 1;
	fi

	# user_dir is the name of the user i.e. user12
	for user_dir in $(ls $clean_data_dir); do
		echo $user_dir;
		for session_file in $(ls ${clean_data_dir}/${user_dir}); do
			session_filepath="${clean_data_dir}/${user_dir}/${session_file}";
			python3 $gen_features_script_filepath $session_filepath;
		done
	done
done
