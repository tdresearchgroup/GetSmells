import pickle


PROJECT_NAMES = ['ant', 'argouml', 'columba', 'jEdit', 'jfreechart', 'jmeter', \
				'jruby', 'incubator_dubbo', 'spring_boot', 'seata', 'skywalking', \
				'eclipse', 'titan']

spring_boot_versions = ['1.4.0.M3', '1.3.0.M3', '1.2.0.M2', '1.1.0.RELEASE', '0.5.0.M2']
seata_versions = ['0.5.0', '0.4.0', '0.3.1', '0.2.0', '0.1.0']
titan_versions = ['0.9.0-M2', '0.5.1', '0.4.1', '0.3.1', '0.2.1']
spring_boot_project_names = [('spring-boot-' + version) for version in spring_boot_versions]
seata_project_names = [('seata-' + version) for version in seata_versions]
titan_project_names = [('titan-' + version) for version in titan_versions]

ADDITIONAL_PROJECTS = ['apache-jmeter-5.0_src', \
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

PROJECT_NAMES.extend(spring_boot_project_names)
PROJECT_NAMES.extend(seata_project_names)
PROJECT_NAMES.extend(titan_project_names)
PROJECT_NAMES.extend(ADDITIONAL_PROJECTS)

OUTPUT_FILENAME = "combined_project_4"

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
