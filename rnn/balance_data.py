import pickle
import nltk
import random
import os
from convert_to_sequence_and_labels import CLASSES_OUTPUT_FILENAME, CLASS_DICT_FILENAME, ALL_SOURCES_WORDS_FILENAME

with open('OUTPUT_FILENAME.txt', 'r') as file:
	PROJECT_NAME = file.read()

with open(PROJECT_NAME + "_sequences", 'rb') as fp:
	sequences = pickle.load(fp)
with open(PROJECT_NAME + "_labels", 'rb') as fp:
	labels = pickle.load(fp)


total_number_of_classes_without_zeros = 0
for label in labels:
	if int(label) == 1:
		total_number_of_classes_without_zeros += 1
print("total_number_of_classes_without_zeros:", total_number_of_classes_without_zeros)

# partition into equal numbers of classes with and without god class (i.e., 0 or 1)
even_sequences = []
even_labels = []

number_of_classes_with_zeros = 0


for index in range(len(sequences)):
	if (int(labels[index]) == 0 and number_of_classes_with_zeros < total_number_of_classes_without_zeros):
		even_sequences.append(sequences[index])
		even_labels.append(labels[index])
		number_of_classes_with_zeros += 1

	elif (int(labels[index]) == 1):
		even_sequences.append(sequences[index])
		even_labels.append(labels[index])

# shuffle
sequence_label_combination = list(zip(even_sequences, even_labels))

random.shuffle(sequence_label_combination)

even_sequences, even_labels = zip(*sequence_label_combination)

print(even_labels)

with open(PROJECT_NAME + "_balanced_sequences", 'wb') as fp:
	pickle.dump(even_sequences, fp)
with open(PROJECT_NAME + "_balanced_labels", 'wb') as fp:
	pickle.dump(even_labels, fp)

# remove preprocessing files for combined
os.remove(CLASSES_OUTPUT_FILENAME)
os.remove(CLASS_DICT_FILENAME)
os.remove(ALL_SOURCES_WORDS_FILENAME)