from flatten import FLATTENED_SRC_DIR_SUFFIX, PROCESSED_PROJECTS_LIST_TXT_FILE_NAME
import glob
import shutil
import getsmells
import os

def make_directories_in_rnn(directories_to_make):
	"""
	For each directory in the argument, make the directory in the 'rnn/' directory if it doesn't already exist
	"""

	for dir_name in directories_to_make:
		dir_path = os.path.join('rnn', dir_name)
		if not os.path.exists(dir_path):
			os.mkdir(dir_path)

def generate_labels_for_flattened_src_directory(flattened_project_dir_name):
	"""
	Generate 'classes.csv' file with labels for each class in the src directory.
	Move the flattened_src into the 'rnn/' directory
	Move the 'classes.csv' label file into the 'rnn/' directory
	"""

	DUMMY_STRING = "" # needed because getsmells cli requires length two list
	getsmells.cli([DUMMY_STRING, flattened_project_dir_name]) # Generate 'classes.csv' file with labels for each class in the src directory.

	CLASSES_LABEL_CSV_SUFFIX = "-smells-classes.csv"
	classes_labels_csv_path = os.path.join(getsmells.OUTPUT_DIR_NAME, flattened_project_dir_name + CLASSES_LABEL_CSV_SUFFIX)

	if os.path.exists(classes_labels_csv_path):
		shutil.move(flattened_project_dir_name, 'rnn/data/') # Move the flattened_src into the 'rnn/' directory
		shutil.move(classes_labels_csv_path, 'rnn/data/') # Move the 'classes.csv' label file into the 'rnn/' directory
	else:
		print("Getsmells.py did not generate csv files.")

if __name__ == "__main__":
	# check if java-only 'flattened_src' directories exist in working directory
	flattened_projects_list = glob.glob("*{}".format(FLATTENED_SRC_DIR_SUFFIX))
	if len(flattened_projects_list) > 0:
		DIR_TO_MAKE = ['data', # 'data' will house 'flattened_src' dirs and '-classes.csv' (aka, correct labels) files 
					   'all_sources_words', 
					   'class_dict', 
					   'class_output']

		make_directories_in_rnn(DIR_TO_MAKE)

		shutil.copy(PROCESSED_PROJECTS_LIST_TXT_FILE_NAME, 'rnn')

		# run getsmells on each of the flattened project directories and move files into 'rnn/data/'
		for flattened_project_dir_name in flattened_projects_list:
			generate_labels_for_flattened_src_directory(flattened_project_dir_name)

	else:
		print("No directories with pattern '{}'".format(FLATTENED_SRC_DIR_SUFFIX))