import pickle
import nltk
import random

vocabulary_size = 8000
UNKNOWN_TOKEN = "UNKNOWN_TOKEN"


PROJECT_NAME = 'combined_project_4'

_CLASSES_OUTPUT_FILENAME = PROJECT_NAME + '_class_output'
_CLASS_DICT_FILENAME = PROJECT_NAME + '_class_dict'
_ALL_SOURCES_WORDS_FILENAME = PROJECT_NAME + '_all_sources_words'


# read preprocessed data
with open(_CLASSES_OUTPUT_FILENAME, 'rb') as fp:
	# load dictionary
    classes_output = pickle.load(fp)

with open(_ALL_SOURCES_WORDS_FILENAME, 'rb') as fp:
	# load array
	all_sources_words = pickle.load(fp)

with open(_CLASS_DICT_FILENAME, 'rb') as fp:
	# each class source is already tokenized into a list of 'words'
	# load dictionary
	class_dict = pickle.load(fp)

word_freq = nltk.FreqDist(all_sources_words)

vocab = word_freq.most_common(vocabulary_size-1) # subtract 1 because we are adding the UNKNOWN_TOKEN 
index_to_word = [x[0] for x in vocab]
index_to_word.append(UNKNOWN_TOKEN)
word_to_index = dict([(w,i) for i,w in enumerate(index_to_word)])

class_name_to_understand_api_class_name = {}

ignore_class_names = []

print("Number of classes to process: {}".format(len(class_dict)))

progress_count = 0

for class_name in class_dict.keys():
	if (progress_count % 100 == 0):
		print("Current class: {}".format(progress_count))
		
	# convert the sources to 
	original_class_src = class_dict[class_name]
	class_dict[class_name] = [word if word in word_to_index else UNKNOWN_TOKEN for word in original_class_src]
	class_src_with_unknown_token = class_dict[class_name]

	class_dict[class_name] = [word_to_index[word] for word in class_src_with_unknown_token]

	class_name_count = 0
	# convert class_name to UnderstandAPI's class name
	for understand_api_class_name in classes_output.keys():
		if understand_api_class_name == class_name:
			class_name_to_understand_api_class_name[class_name] = understand_api_class_name

			class_name_count = class_name_count + 1
		elif understand_api_class_name.endswith("." + class_name):
			class_name_to_understand_api_class_name[class_name] = understand_api_class_name

			class_name_count = class_name_count + 1

	if class_name_count != 1:
		#print("Error: class_name: " + str(class_name) + " class_name_count: " + str(class_name_count))
		if (class_name not in ignore_class_names):
			ignore_class_names.append(class_name)

	progress_count += 1


class_name_list = [key for key in class_dict.keys() if key not in ignore_class_names]
random.shuffle(class_name_list)

sequences = [class_dict[class_name] for class_name in class_name_list]

# only doing 'god class' labels, will do one by one
GOD_CLASS_INDEX = 0

labels = [classes_output[class_name_to_understand_api_class_name[class_name]][GOD_CLASS_INDEX] for class_name in class_name_list]

with open(PROJECT_NAME + "_sequences", 'wb') as fp:
	pickle.dump(sequences, fp)
with open(PROJECT_NAME + "_labels", 'wb') as fp:
	pickle.dump(labels, fp)
