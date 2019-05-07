# Instructions

1. Drop the source code zip and tar.gz files into this repository
2. Run ```flatten.sh``` - looks for zip and tar.gz files, and extract the java files to directories for each projection and specific version. Each directory has the name pattern "{PROJECT_NAME_WITH_VERSION}_flattened_src". Every zip file is moved into the archived source code zip files directory. Preprocessing files are deleted.


```
chmod u+x flatten.sh # only necessary if user doesn't already have execute permissions
./flatten.sh
```

3. Run ```getsmells_all.sh``` - runs getsmells.py on all of extracted file directories (i.e, the directories with suffix "-flattened_src")


```
# activate environment
source {ENV_NAME}/bin/activate

# install prerequisites
pip install -r requirements.txt

chmod u+x getsmells_all.sh # again, only necessary is user doesn't already have execute permissions
./getsmells_all.sh
```

4. Generate class_output, class_dict, and all_sources_words for each file

class_output -- converts the labels from the csv file from the getsmells -clases.csv file

class_dict -- dictionary of class and class source code

all_sources_words -- list of all words in the project

```
Move the "-smells-classes.csv" and "-flattened_src" directories into the ```rnn/data/``` directory

# activate environment - use conda install if on Windows
source env/bin/activate

# install requirements
pip install -r requirments.txt
```

Use the project_name_with_version_list.txt to make a list of projects to preprocess and edit the preprocessing.py and combine_all_classes.py so that PROJECT_NAMES = {list of projects}

Change the OUTPUT_NAME for combine_all_classes and edit the convert_to_sequence_and_labels.py and balance_data.py accordingly
```
python preprocessing.py
python combine_all_classes.py
```

5. You should now have the combined projects OUTPUT_NAME files for class_output, class_dict, and all_sources_words. Convert this to sequence and labels, and then balance the dataset to have an equal number of ones and zeros in the labels

```
python convert_to_sequence_and_labels.py
python balance_data.py
```

6. You should have ```{OUTPUT_NAME}_balanced_sequences``` and ```{OUTPUT_NAME}_balanced_labels```. Edit the PROJECT_NAME in model.py so that it has the same name. Run the model.

```
python model.py
```
