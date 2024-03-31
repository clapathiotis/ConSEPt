#!/bin/bash
set -e

# Creating the new directory for the edited user project files
echo Creating project directories
mkdir -p $PARENT_FOLDER_OF_USER_PROJECT
cp -R $USER_PROJECT_PATH $PARENT_FOLDER_OF_USER_PROJECT

cp $MOUNTED_MUTATION_FOLDER/build.sh $EDITED_USER_PROJECT_PATH
cp $MOUNTED_MUTATION_FOLDER/test.sh $EDITED_USER_PROJECT_PATH
cp $MOUNTED_MUTATION_FOLDER/.dextool_mutate.toml $EDITED_USER_PROJECT_PATH

# TODO find the directory cmakeLists.txt is in
# TODO edit cmakeLists.txt
echo Rebuilding project
cd $EDITED_USER_PROJECT_PATH
[ -d build ] || mkdir build
rm -rf build/*
cd build
cmake .. -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

echo Building scripts
cd $EDITED_USER_PROJECT_PATH
chmod 755 build.sh test.sh
echo Analyzing scripts
dextool mutate analyze

echo Running mutation tests
dextool mutate test
echo Creating reports
dextool mutate report --style html --section tc_similarity --section tc_min_set --section tc_full_overlap_with_mutation_id --section tc_killed_no_mutants --section tc_full_overlap --section trend
cp -r $EDITED_USER_PROJECT_PATH/html $MOUNTED_MUTATION_FOLDER
