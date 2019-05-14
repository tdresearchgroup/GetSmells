# Model

LSTM Acceptor:
 * Vocabulary size of 8000
 * Embedding size of 1000
 * Supervision signal:
 	> 1. Sigmoid to normalize <br />
	> 2. Cross entropy loss (binary classification) <br />

Possible improvement(s) and extension(s):
 * RNN/CNN encoder before acceptor to gain 'context' (allows context-required code smell detection, e.g. 'Refused Bequest')
 * Different code smells classes (there are seven possible labels given by getsmells.py, e.g. 'God', 'Lazy', 'Complex',...)
 * Different embedding sizes (compare accuracy vs efficiency)

# Training/Testing

70-30 training-testing split

Possible improvement(s) and extension(s):
 * Completely separate sets of preprocessed files for training vs testing

# Setup Instructions

## Cloning the repository
```
git clone --single-branch --branch rnn https://github.com/tdresearchgroup/getsmells.git
cd getsmells # move into directory
```

## Virtual environments for python

### Install virtualenv
If you don't already have the python package ```virtualenv``` installed, you will need to install this so that you can create and activate/deactivate into environments
```
pip3 install virtualenv # install virtualenv for python 3
```

### Create virtual environment
```
virtualenv [ENVIRONMENT_NAME] # e.g, virtualenv venv
```

### Activate virtual environment
```
source [ENVIRONMENT_NAME]/bin/activate # You should see an '([ENVIRONMENT_NAME])' before your command line shell prompt
```

### Deactivate virtualenv environment
```
deactivate
```

### Install packages (locally) in virtual environment
```
source [ENVIRONMENT_NAME]/bin/activate # activate the environment
pip install [PACKAGE]
```

#### Install packages from requirements file
```
pip install -r requirements.txt
```

#### Export list of packages into requirements text file
```
pip freeze > requirements.txt
```

## Preprocess Source Code Zip Files for the Model

1. Drop the source code zip and tar.gz files into this repository
2. Run ```flatten.sh``` - looks for zip and tar.gz files, and extract the java files to directories for each projection and specific version. Each directory has the name pattern ```{PROJECT_NAME_WITH_VERSION}_flattened_src```. Every zip file is moved into the archived source code zip files directory. Preprocessing files are deleted.

```
chmod u+x flatten.sh # only necessary if user doesn't already have execute permissions
./flatten.sh
```

Alternatively,
```
python flatten.py
```

3. Run ```getsmells_all.sh``` - runs getsmells.py on all of extracted file directories (i.e, the directories with suffix "-flattened_src")

**You will need an Understand API license key.**


```
# create and activate environment
virtualenv [ENVIRONMENT_NAME]
source [ENVIRONMENT_NAME]/bin/activate

# install prerequisites
pip install -r requirements.txt

# run script
chmod u+x getsmells_all.sh # again, only necessary is user doesn't already have execute permissions
./getsmells_all.sh

# deactivate virtual environment
deactivate
```

Alternatively,

```
python getsmells_all.py
```

4. Generate class_output, class_dict, and all_sources_words for each file

class_output -- converts the labels from the csv file from the getsmells -clases.csv file

class_dict -- dictionary of class and class source code

all_sources_words -- list of all words in the project, used to generate the list of [VOCAB_SIZE] most common words that are used to convert each class' source code into an [VOCAB_SIZE]-length vector 

```
# move into 'rnn' directory
cd rnn

# create and activate environment
virtualenv [ENVIRONMENT_NAME] # If on Windows, you will need to create an Anaconda environment instead because the python package 'dynet' from pip is not compatible with Windows
source [ENVIRONMENT_NAME]/bin/activate 

# install requirements
pip install -r requirements.txt

# preprocess each individual project
python preprocess_individual_classes.py

# combine each project's classes' preprocessed files
python combine_all_classes.py [OUTPUT_NAME]
```

5. Convert the dictionaries for each class into sequences and labels with 50-50 positive negative ratio.
```
python convert_to_sequence_and_labels.py # convert to sequence and labels
python balance_data.py # randomly take 50-50 positive-negative sample of the full sequence to use as the training/testing set
```

## Running the model and the Results
```
python model.py
```

The results will be stored in the ```[OUTPUT_NAME]_test_set_results.csv``` file. This file has the actual predictions for each of the examples in the test set, as well as the recall, precision, and F1-score. 
