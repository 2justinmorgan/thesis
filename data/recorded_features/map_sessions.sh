
output_sessions_obj_filepath="./mapped_sessions.json";
clean_data_dirs=( \
	"../clean_mouse_data/test_files" \
	"../clean_mouse_data/training_files");

echo "{" > $output_sessions_obj_filepath;

for clean_data_dir in ${clean_data_dirs[@]}; do
	if [[ ! -d $clean_data_dir ]]; then
		>&2 echo "$clean_data_dir source dir not found";
		exit 1;
	fi

	# user_dir is the name of the user i.e. user12
	for user_dir in $(ls $clean_data_dir); do
		for session_file in $(ls ${clean_data_dir}/${user_dir}); do
			echo "  \"$session_file\": \"$user_dir\"," \
				>> $output_sessions_obj_filepath;
		done
	done
done

echo '  "": 0' >> $output_sessions_obj_filepath;
echo "}" >> $output_sessions_obj_filepath;

sessions_json=$(jq . $output_sessions_obj_filepath);

if [[ $? -ne 0 ]]; then
	>&2 echo "WARNING: $output_sessions_obj_filepath did not parse as a json.";
	exit 1;
fi

