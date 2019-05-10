DIR_PATTERN="_flattened_src"

mkdir rnn/data
mkdir rnn/all_sources_words
mkdir rnn/class_dict
mkdir rnn/class_output

# cp project list into rnn
cp project_name_with_version_list.txt rnn/

for src_dir in $(ls -d *$DIR_PATTERN/); 
do 
	python getsmells.py $src_dir;
	mv $src_dir rnn/data/;

	length_of_src_dir_name=${#src_dir};
	mv "getsmells-output/${src_dir:0:length_of_src_dir_name-1}-smells-classes.csv" rnn/data/;
done


# clean
rm -rf __pycache__
rm understandapi.pyc