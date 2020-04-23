import src
import os
import csv
import argparse
import understand
from src.common.statisticUtil import printProgress


def main(udbFile, rawData):
    """
    Processor for Android vulnerability data only.
    The motivation is that original Android vulnerability data only talks about file instead of classes.
    This function maps each file path to classes (assume all classes in a file is vulnerable)
    :param udbFile: udb file created in src.app
    :param rawData: Android data contains column "Files"
    :return:
    """
    db = understand.open(udbFile)
    outPath = f"{os.path.splitext(rawData)[0]}-processed.csv"

    with open(rawData, 'r') as inf, open(outPath, 'w') as outf:
        reader = csv.DictReader(inf)
        rows = list(reader)

        columnNames = reader.fieldnames + ['class']
        writer = csv.DictWriter(outf, fieldnames=columnNames, delimiter=",")
        writer.writeheader()

        for idx, row in enumerate(rows):
            printProgress(idx, len(rows))
            filename = row['Files']
            fileEnts = db.lookup(filename)

            if not len(fileEnts):
                print(f'WARNING: {filename} does not exist in DB.')
                continue
            if len(fileEnts) > 1:
                print(f'WARNING: more than one {filename} in DB.')
                continue

            for classRef in fileEnts[0].refs("Define", "Class"):
                row['class'] = classRef.ent().longname()
                writer.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="python3 androidVulProcessor xxx/android-6.0.0-r41.udb xxx/android-6.0.0.csv")
    parser.add_argument("udbFile", help="The path to the Android udb file")
    parser.add_argument("rawData", help="The path to the Android data file containing Files column.")
    args = parser.parse_args()
    main(args.udbFile, args.rawData)
