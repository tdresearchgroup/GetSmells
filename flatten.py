# flatten script in python alternative
import os
import sys
import glob
import tarfile
import zipfile
import shutil

ARCHIVED_PROJECT_ZIP_FILE_DIR = "archived_project_zip_files"
FLATTENED_SRC_DIR_SUFFIX = "_flattened_src"
PROCESSED_PROJECTS_LIST_TXT_FILE_NAME = "project_name_with_version_list.txt"

if __name__ == "__main__":

	if not os.path.exists(ARCHIVED_PROJECT_ZIP_FILE_DIR):
		os.mkdir(ARCHIVED_PROJECT_ZIP_FILE_DIR)

	EXTENSIONS = ["zip", "tar.gz"]

	compressed_files = []

	for extension in EXTENSIONS:
		compressed_files_of_extension = glob.glob1(".", "*.{}".format(extension))
		compressed_files.extend(compressed_files_of_extension)


	if (len(compressed_files) > 0):
		compressed_file_name_without_extension_list = []

		for compressed_file in compressed_files:
			compressed_file_name = compressed_file.lower()
			compressed_file_name_without_extension, extension = os.path.splitext(compressed_file_name)

			# uncompress the files into directory called [compressed_file_name_without_extension]
			if extension == ".zip":
				with zipfile.ZipFile(compressed_file_name, "r") as zip_ref:
					if not os.path.exists(compressed_file_name_without_extension):
						os.mkdir(compressed_file_name_without_extension)
					zip_ref.extractall(compressed_file_name_without_extension)
					
			elif extension == ".gz" and compressed_file_name_without_extension[-len(".tar"):] == ".tar":
				# special case for tar.gz file - remove the ".tar" (last four characters)
				compressed_file_name_without_extension = compressed_file_name_without_extension[:-len(".tar")]

				with tarfile.open(compressed_file_name, "r:gz") as tar_ref:
					tar_ref.extractall(compressed_file_name_without_extension)

			# add name of the directory with uncompressed files into a list
			compressed_file_name_without_extension_list.append(compressed_file_name_without_extension)

			# move the compressed directory into the archived folder
			shutil.move(compressed_file_name, ARCHIVED_PROJECT_ZIP_FILE_DIR)

		# extract only java files from uncompressed directory into flattened source directories for each project
		for base_dir_for_project in compressed_file_name_without_extension_list:
			target_dir_for_project = base_dir_for_project + FLATTENED_SRC_DIR_SUFFIX
			if not os.path.exists(target_dir_for_project):
				os.mkdir(target_dir_for_project)

			# move all java files from the unzipped directory into the target directory
			for dir_name, dir_names, file_names in os.walk(base_dir_for_project):
				for file_name in file_names:
					source = os.path.join(dir_name, file_name)
					if file_name.endswith(".java"):
						if not os.path.exists(os.path.join(target_dir_for_project, file_name)):
							shutil.move(source, target_dir_for_project)

			# delete the java-less uncompressed directory
			shutil.rmtree(base_dir_for_project, ignore_errors=True)

		with open(PROCESSED_PROJECTS_LIST_TXT_FILE_NAME, "a") as file:
			for project_name_with_version in compressed_file_name_without_extension_list:
				file.write("{}, \\\n".format(project_name_with_version)) # can be simpler, but this allows direct copying into python list


	else:
		print("No compressed files to extract java files from")