#!/bin/bash

project_name="seata"
project_versions=(0.5.0 0.4.0 0.3.1 0.2.0 0.1.0)

for project_version in "${project_versions[@]}"
do
    project_src_dir="${project_name}-${project_version}"
    project_flattened_src_dir="${project_src_dir}_flattened_src"

    mkdir $project_flattened_src_dir
    cd $project_src_dir
    find . -name "*.java" -exec mv {} "../${project_flattened_src_dir}" \;
    cd ..
done
