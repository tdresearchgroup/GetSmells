import csv
import itertools
import operator
import dynet as dy
import numpy as np
import nltk
import sys
import os
import time
from datetime import datetime

import random
import pickle

PROJECT_NAME = "combined_project_4"

vocabulary_size = 8000
UNKNOWN_TOKEN = "UNKNOWN_TOKEN"

EMBED_SIZE = 1000

class LSTMAcceptor(object):
	def __init__(self, in_dim, lstm_dim, out_dim, model):
		self.builder = dy.VanillaLSTMBuilder(1, in_dim, lstm_dim, model)
		self.W = model.add_parameters((out_dim, lstm_dim))

	def __call__(self, sequence):
		lstm = self.builder.initial_state()
		W = self.W.expr()
		outputs = lstm.transduce(sequence)
		result = W*outputs[-1]

		return result

with open(PROJECT_NAME + "_balanced_sequences", 'rb') as fp:
	sequences = pickle.load(fp)
with open(PROJECT_NAME + "_balanced_labels", 'rb') as fp:
	labels = pickle.load(fp)

TEST_SET_PARTITION_START = 0.70

test_sequences = sequences[int(TEST_SET_PARTITION_START*len(sequences)):]
test_labels = labels[int(TEST_SET_PARTITION_START*len(sequences)):]
	
sequences = sequences[:int(TEST_SET_PARTITION_START*len(sequences))]
labels = labels[:int(TEST_SET_PARTITION_START*len(labels))]



print("Sequence size:", len(sequences))
print("Labels size:", len(labels))

m = dy.Model()
trainer = dy.AdamTrainer(m)
embeds = m.add_lookup_parameters((vocabulary_size, EMBED_SIZE))
acceptor = LSTMAcceptor(EMBED_SIZE, 100, 1, m)

sum_of_losses = 0.0
offset = 0

loss_output_file = open(PROJECT_NAME + "_loss_output.txt", 'a')

num_of_classes_per_epoch = 50

num_of_classes = len(sequences)

start_index = 0

for epoch in range(100):
	print("Epoch " + str(epoch) + ":")
	
	sum_of_losses_per_epoch = 0
	
	for training_example in range(num_of_classes_per_epoch):
		dy.renew_cg()
		sequence = sequences[(start_index + training_example) % num_of_classes]
		label = labels[(start_index + training_example) % num_of_classes]
		label_vec = dy.vecInput(1)
		label_vec.set([label])

		vecs = [embeds[i] for i in sequence]
		prediction = acceptor(vecs)

		prediction = dy.logistic(prediction)

		loss = dy.binary_log_loss(prediction, label_vec)
		
		# online/sequential learning
		loss.backward()
		trainer.update()
		
		# for monitoring
		sum_of_losses_per_epoch += loss.npvalue()
		
		# adjust start index
		start_index = start_index + num_of_classes_per_epoch
	
	average_loss = sum_of_losses_per_epoch/num_of_classes_per_epoch
	
	print(str(average_loss))
	
	
	loss_output_file.write("Epoch " + str(epoch) + ": " + str(average_loss) + "\n")
	



# Test the model

def recall(true_positive_count, false_negative_count):
	return 1.0*true_positive_count/(true_positive_count+false_negative_count)

def precision(true_positive_count, false_positive_count):
	return 1.0*true_positive_count/(true_positive_count+false_positive_count)

def f1_score(precision_value, recall_value):
	return 2.0*(precision_value*recall_value)/(precision_value + recall_value)


prediction_label_list = []
correct_label_list = []

true_positive_count = 0
false_positive_count = 0
false_negative_count = 0

sum_of_losses_of_test_examples = 0.0

for test_example_index in range(len(test_sequences)):
		dy.renew_cg()
		test_sequence = test_sequences[test_example_index]
		label = test_labels[test_example_index]
		label_vec = dy.vecInput(1)
		label_vec.set([label])

		vecs = [embeds[i] for i in test_sequence]
		prediction = acceptor(vecs)

		prediction = dy.logistic(prediction)
		if (prediction.npvalue() > 0.5):
			prediction_label = 1
			if (int(label_vec.npvalue()) == 1):
				true_positive_count += 1
			else:
				false_positive_count += 1
		
		else:
			prediction_label = 0

			if (int(label_vec.npvalue()) == 1):
				false_negative_count += 1
		
		prediction_label_list.append(prediction_label)
		correct_label_list.append(int(label_vec.npvalue()))
		
		loss = dy.binary_log_loss(prediction, label_vec)
		
		# for monitoring
		print("Loss for example:", loss.npvalue())
		sum_of_losses_of_test_examples += loss.npvalue()
		
average_loss = sum_of_losses_of_test_examples/len(test_sequences)
	
print("Test loss:", str(average_loss))
loss_output_file.write("Test loss: " + str(average_loss) + "\n")

loss_output_file.close()

with open(PROJECT_NAME + '_test_set_results.csv', 'a') as csvfile:
	fieldnames = ['prediction_label', 'correct_label']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	writer.writeheader()

	for example_index in range(len(prediction_label_list)):
		writer.writerow({'prediction_label': prediction_label_list[example_index], 'correct_label': correct_label_list[example_index]})

	# not actual entries
	writer.writerow({'prediction_label': '--END--', 'correct_label': '--END--'})

	writer.writerow({'prediction_label': 'True positive count', 'correct_label': true_positive_count})
	writer.writerow({'prediction_label': 'False positive count', 'correct_label': false_positive_count})
	writer.writerow({'prediction_label': 'False negative count', 'correct_label': false_negative_count})

	recall_value = recall(true_positive_count, false_negative_count)
	precision_value = precision(true_positive_count, false_positive_count)

	writer.writerow({'prediction_label': 'Recall', 'correct_label': recall_value})
	writer.writerow({'prediction_label': 'Precision', 'correct_label': precision_value})
	writer.writerow({'prediction_label': 'F1 Score', 'correct_label': f1_score(precision_value, recall_value)})
