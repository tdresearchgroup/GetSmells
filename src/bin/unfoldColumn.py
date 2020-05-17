import csv
import argparse


def unfoldColumn(defectInPath, columnToUnfold):
    """
    It recursively walk through smellsOutDir.
    For each [proj]-[version]-xxx-overall.csv, generate csv file that maps the counts of vulnerabilities and smells together.

    Pre-requisite: smellsOutDir should be the same as the "main.py -> main -> outputPath".
    Each vulnerability file should be named as [proj].csv and should contain at least "name" and "version" columns

    :param vulDir: the directory contains all vulnerability data.
    :param smellsOutDir: the directory contains "smells" dir
    :return: None
    """

    print("Start unfolding vulnerability data")
    defectOutPath = defectInPath.replace('.csv', '-processed.csv')

    with open(defectInPath, 'r') as defectIn, open(defectOutPath, 'w') as defectOut:

        defectReader = csv.DictReader(defectIn)
        defectWriter = csv.DictWriter(defectOut, fieldnames=defectReader.fieldnames)
        defectWriter.writeheader()

        for row in defectReader:
            if '  ' in row[columnToUnfold]:
                for v in row[columnToUnfold].strip().split('  '):
                    if not v.strip():
                        continue
                    row[columnToUnfold] = v.strip()
                    defectWriter.writerow(row)
            else:
                defectWriter.writerow(row)
    print("Unfolding vulnerability data done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("defectInPath", help="The file to process")
    parser.add_argument("columnToUnfold", help="The file to process")

    args = parser.parse_args()
    unfoldColumn(args.defectInPath, args.columnToUnfold)
