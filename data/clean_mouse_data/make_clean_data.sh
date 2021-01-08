
cleaning_script_filepath="clean_data.py";
raw_data_dirs=( \
	"../raw_mouse_data/test_files" \
	"../raw_mouse_data/training_files");

if [[ ! -f $cleaning_script_filepath ]]; then
	>&2 echo "$cleaning_script_filepath data cleaning script not found";
	exit 1;
fi

for raw_data_dir in ${raw_data_dirs[@]}; do
	if [[ ! -d $raw_data_dir ]]; then
		>&2 echo "$raw_data_dir source dir not found";
		exit 1;
	fi
	raw_data_dir_name=$(echo $raw_data_dir | rev | cut -d'/' -f1 | rev);

	# user_dir is the name of the user i.e. user12
	for user_dir in $(ls $raw_data_dir); do
		echo $user_dir;
		if [[ ! -d $raw_data_dir_name/$user_dir ]]; then
			mkdir -p $raw_data_dir_name/$user_dir;
		fi
		for session_file in $(ls ${raw_data_dir}/${user_dir}); do
			session_filepath="${raw_data_dir}/${user_dir}/${session_file}";
			python3 $cleaning_script_filepath $session_filepath \
				> $raw_data_dir_name/$user_dir/$session_file;
		done
	done
done
