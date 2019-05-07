# Instructions

1. Drop the source code zip and tar.gz files into this repository
2. Run ```flatten.sh``` - looks for zip and tar.gz files, and extract the java files to directories for each projection and specific version. Each directory has the name pattern "{PROJECT_NAME_WITH_VERSION}_flattened_src". Every zip file is moved into the archived source code zip files directory. Preprocessing files are deleted.


```
chmod u+x flatten.sh # only necessary if user doesn't already have execute permissions
./flatten.sh
```

3. Run ```getsmells_all.sh``` - runs getsmells.py on all of extracted file directories (i.e, the directories with suffix "-flattened_src")


```
chmod u+x getsmells_all.sh # again, only necessary is user doesn't already have execute permissions
./getsmells_all.sh
```
