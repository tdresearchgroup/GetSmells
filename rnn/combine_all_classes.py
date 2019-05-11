import pickle
import sys

# get name of project names with their versions
project_names_list = open('project_name_with_version_list.txt', 'r')
PROJECT_NAMES = project_names_list.read().split(', \\\n')
del PROJECT_NAMES[-1] # remove the empty string last element



OUTPUT_FILENAME = "combined_project_4"
if (len(sys.argv) == 1):
	print("Using default project name for output: {}".format(OUTPUT_FILENAME))
elif (len(sys.argv) == 2):
	OUTPUT_FILENAME = str(sys.argv[1])
	print("Project name for output: {}".format(OUTPUT_FILENAME))
else:
	print("Usage: python {} [OUTPUT_FILENAME]".format(sys.argv[0]))
	sys.exit()

# write OUTPUT_FILENAME into file
with open('OUTPUT_FILENAME.txt', 'w') as file:
	file.write(OUTPUT_FILENAME)


all_project_class_labels = {}

all_project_class_sources = {}

all_project_words = []

for project_name in PROJECT_NAMES:

	_CLASSES_OUTPUT_FILENAME = "class_output/" + project_name + '_class_output'
	_CLASS_DICT_FILENAME = "class_dict/" + project_name + '_class_dict'
	_ALL_SOURCES_WORDS_FILENAME = "all_sources_words/" + project_name + '_all_sources_words'

	# read preprocessed data
	with open(_CLASSES_OUTPUT_FILENAME, 'rb') as fp:
	    classes_output = pickle.load(fp)

	with open(_ALL_SOURCES_WORDS_FILENAME, 'rb') as fp:
		all_sources_words = pickle.load(fp)

	with open(_CLASS_DICT_FILENAME, 'rb') as fp:
		# each class source is already tokenized into a list of 'words'
		class_dict = pickle.load(fp)


	# add every source to combined project class source dictionary
	for class_name, class_source in class_dict.items():
		all_project_class_sources[class_name + "_" + project_name] = class_source

	# add every label to the combined project class label's dictionary
	for class_name, class_label in classes_output.items():
		all_project_class_labels[class_name + "_" + project_name] = class_label

	# add source
	all_project_words.extend(all_sources_words)

with open(OUTPUT_FILENAME + "_class_output", 'wb') as fp:
	pickle.dump(all_project_class_labels, fp)

with open(OUTPUT_FILENAME + "_class_dict", 'wb') as fp:
	pickle.dump(all_project_class_sources, fp)

with open(OUTPUT_FILENAME + "_all_sources_words", 'wb') as fp:
	pickle.dump(all_project_words, fp)
