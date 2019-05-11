import csv
import itertools
import operator
import numpy as np
import nltk
import sys
import os
import re

import pickle

def words_and_dict(PROJECT_NAMES):
	for project_name in PROJECT_NAMES:
		FLATTENED_SRC_DIRECTORY = './data/' + project_name + '_flattened_src/'

		CLASS_DELIMITER = "public class"

		# used to compute the word frequencies, and then the dictionary
		all_sources = ''

		# key = class_name, value = class_source
		class_dict = {}

		for file in os.listdir(FLATTENED_SRC_DIRECTORY):
			if file.endswith(".java"):
				with open(FLATTENED_SRC_DIRECTORY + file, 'r', encoding = "ISO-8859-1") as fp:
					file_content = fp.read()

					all_sources = all_sources  + " " + file_content

					tokenized_file = re.split(r'(?<!\*\s)public class(?=\s[a-zA-Z]+\s)', file_content)


					for i in range(1, len(tokenized_file)):
						# ignores the imports
						# add back the public class used as delimiter
						class_source = "public class" + tokenized_file[i]

						# add source to all_sources
						all_sources = all_sources + " " + class_source

						# since the first two words in the class source are "public", "class"
						CLASS_NAME_INDEX = 2

						class_name = (class_source.split())[CLASS_NAME_INDEX]

						# add source to dictionary of sources
						class_dict[class_name] = nltk.word_tokenize(class_source)

		if 'public' in class_dict.keys():
			print(class_dict['public'])

		all_sources_words = nltk.word_tokenize(all_sources)

		with open(("all_sources_words/" + project_name + "_all_sources_words"), "wb") as fp:
				pickle.dump(all_sources_words, fp)

		with open(("class_dict/" + project_name + "_class_dict"), "wb") as fp:
				pickle.dump(class_dict, fp)

def class_output(PROJECT_NAMES):
	"""
	output the labels for each class for each project in the arg PROJECT_NAMES
	"""
	for project_name in PROJECT_NAMES:
		output_vector = {}
		
		print('Reading CSV file...')
		with open('data/' + project_name + '_flattened_src-smells-classes.csv', 'r') as f:
		    reader = csv.reader(f, skipinitialspace=True, delimiter=',')
		    labels = next(reader)


		    for row in reader:
		    	class_name=row[0]

		    	output_for_class = []
		    	for column in range(1, 8):
		    		if row[column] == "True":
		    			output_for_class.append(1)
		    		else:
		    			output_for_class.append(0)

		    	output_vector[class_name] = output_for_class

		with open(("class_output/" + project_name + "_class_output"), "wb") as fp:
			pickle.dump(output_vector, fp)

if __name__ == "__main__":

	project_names_list = open('project_name_with_version_list.txt', 'r')
	PROJECT_NAMES = project_names_list.read().split(', \\\n')
	del PROJECT_NAMES[-1] # remove the empty string last element


	words_and_dict(PROJECT_NAMES)
	class_output(PROJECT_NAMES)
