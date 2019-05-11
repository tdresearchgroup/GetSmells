DIR_PATTERN="_flattened_src"

# check if directories exist
if [[ $(ls -d *$DIR_PATTERN/) ]]; then
    echo "Running getsmells on flattened source directories"
else
    echo "No flattened source directories"
    exit 1
fi

mkdir rnn/data
mkdir rnn/all_sources_words
mkdir rnn/class_dict
mkdir rnn/class_output

# cp project list into rnn
cp project_name_with_version_list.txt rnn/


for src_dir in $(ls -d *$DIR_PATTERN/); 
do 
    # run getsmells and generate the csv file for the flattened source directory
    python getsmells.py $src_dir;
    return_status=$? # check return status of python script
    if [ $return_status -ne 0 ]; then
        exit 1 # exit if getsmells.py doesn't work
    fi

    # move the flattened source directory into the 'data' directory
    mv $src_dir rnn/data/;
    
    # move the csv labels into the 'data' directory
    length_of_src_dir_name=${#src_dir};
    mv "getsmells-output/${src_dir:0:length_of_src_dir_name-1}-smells-classes.csv" rnn/data/; # remove the '/' last character
done


# clean
rm -rf __pycache__
rm understandapi.pyc
