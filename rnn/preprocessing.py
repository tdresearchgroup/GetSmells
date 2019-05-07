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

	# PROJECT_NAMES = ['ant', 'argouml', 'columba', 'jEdit', 'jfreechart', 'jmeter', \
	# 				'jruby', 'incubator_dubbo', 'spring_boot', 'seata', 'skywalking', \
	# 				'eclipse', 'titan']

	# spring_boot_versions = ['1.4.0.M3', '1.3.0.M3', '1.2.0.M2', '1.1.0.RELEASE', '0.5.0.M2']
	# seata_versions = ['0.5.0', '0.4.0', '0.3.1', '0.2.0', '0.1.0']
	# titan_versions = ['0.9.0-M2', '0.5.1', '0.4.1', '0.3.1', '0.2.1']
	# spring_boot_project_names = [('spring-boot-' + version) for version in spring_boot_versions]
	# seata_project_names = [('seata-' + version) for version in seata_versions]
	# titan_project_names = [('titan-' + version) for version in titan_versions]

	# PROJECT_NAMES = []
	# PROJECT_NAMES.extend(spring_boot_project_names)
	# PROJECT_NAMES.extend(seata_project_names)
	# PROJECT_NAMES.extend(titan_project_names)
	PROJECT_NAMES = ['apache-jmeter-5.0_src', \
					'argouml-0.10.1-src', \
					'argouml-0.16-src', \
					'argouml-0.22-src', \
					'argouml-0.26.2-src', \
					'argouml-0.30-src', \
					'eclipse-SDK-2.0-win32', \
					'eclipse-SDK-2.1-win32', \
					'eclipse-SDK-3.0-win32', \
					'incubator-dubbo-dubbo-2.0.7', \
					'incubator-dubbo-dubbo-2.1.0', \
					'incubator-dubbo-dubbo-2.2.0', \
					'incubator-dubbo-dubbo-2.3.0', \
					'incubator-dubbo-dubbo-2.4.0', \
					'jakarta-ant-1.1', \
					'jakarta-ant-1.2-src', \
					'jakarta-ant-1.3-src', \
					'jakarta-ant-1.4-src', \
					'jakarta-ant-1.5-src', \
					'jedit30source', \
					'jedit31source', \
					'jedit32source', \
					'jedit40source', \
					'jedit41source', \
					'jfreechart-0.5.6', \
					'jfreechart-0.6.0', \
					'jfreechart-0.7.0', \
					'jfreechart-0.8.0', \
					'jfreechart-0.9.0', \
					'jruby-src-1.0.1', \
					'jruby-src-1.1.1', \
					'jruby-src-1.1.4', \
					'jruby-src-1.2.0', \
					'jruby-src-1.3.0', \
					'skywalking-1.0-Final', \
					'skywalking-2.0-2016', \
					'skywalking-3.0-2017', \
					'skywalking-3.2.6', \
					'skywalking-5.0.0-alpha']

	#print(PROJECT_NAMES)
	#words_and_dict(PROJECT_NAMES)
	class_output(PROJECT_NAMES)
