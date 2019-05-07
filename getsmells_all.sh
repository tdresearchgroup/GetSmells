DIR_PATTERN="_flattened_src"

for i in $(ls -d *$DIR_PATTERN/); do python getsmells.py $i; done
