#!/bin/bash

mkdir "archived_project_zip_files"

zip_file_count=$(ls -1 *.zip 2>/dev/null | wc -l)
tar_file_count=$(ls -1 *.tar.gz 2>/dev/null | wc -l)

if [ $zip_file_count != 0 ]
then
for project_zip_file in ./*.zip
do
    # lowercase each filename
    project_zip_file=$(echo $project_zip_file | tr "[A-Z]" "[a-z]")

    length_of_string=${#project_zip_file}
    # Start after "./" at index 2
    # Cut out the last 4 characters ".zip", which makes the length 6 less
    project_name_with_version=${project_zip_file:2:$length_of_string-6}
    echo $project_name_with_version
    echo "${project_name_with_version}, \\" >> project_name_with_version_list.txt 
    
    mkdir $project_name_with_version
    unzip -qq $project_zip_file -d $project_name_with_version


    project_flattened_src_dir="${project_name_with_version}_flattened_src"

    mkdir $project_flattened_src_dir
    cd "./${project_name_with_version}"
    find . -name "*.java" -exec mv {} "../${project_flattened_src_dir}" \;
    cd ..

    # delete java-less unzipped files
    rm -rf $project_name_with_version
    # move zip files into archived zip file direcctory
    mv $project_zip_file ./archived_project_zip_files/
done
fi

if [ $tar_file_count != 0 ]
then
# complete violation of DRY
for project_zip_file in ./*.tar.gz
do
    # lowercase each filename
    project_zip_file=$(echo $project_zip_file | tr "[A-Z]" "[a-z]")
    
    length_of_string=${#project_zip_file}
    # Start after "./" at index 2
    # Cut out the last 7 characters ".tar.gz", which makes the length 9 less
    project_name_with_version=${project_zip_file:2:$length_of_string-9}
    echo $project_name_with_version
    echo "${project_name_with_version}, \\" >> project_name_with_version_list.txt 
    
    mkdir $project_name_with_version
    tar -xzf $project_zip_file -C $project_name_with_version


    project_flattened_src_dir="${project_name_with_version}_flattened_src"

    mkdir $project_flattened_src_dir
    cd "./${project_name_with_version}"
    find . -name "*.java" -exec mv {} "../${project_flattened_src_dir}" \;
    cd ..

    # delete java-less unzipped files
    rm -rf $project_name_with_version
    # move zip files into archived zip file direcctory
    mv $project_zip_file ./archived_project_zip_files/
done
fi
