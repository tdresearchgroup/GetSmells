import src
import os
import csv
import argparse
import understand
from src.common.statisticUtil import printProgress


def main(udbDir, projectName, rawData):
    """
    The motivation is that original Android vulnerability data only talks about file instead of classes.
    This function maps each file path to classes (assume all classes in a file is vulnerable)
    :param udbDir: udb files created in main.app
    :param rawData: Android data contains column "file" and "version"
    :return:
    """
    outPath = rawData.replace('.csv', '-processed.csv')
    dbs = readDbs(udbDir, projectName)

    with open(rawData, 'r') as inf, open(outPath, 'w') as outf:
        reader = csv.DictReader(inf)
        rows = list(reader)

        columnNames = reader.fieldnames + ['class']
        writer = csv.DictWriter(outf, fieldnames=columnNames, delimiter=",")
        writer.writeheader()

        versionNotInDbs = set()

        for idx, row in enumerate(rows):
            printProgress(idx, len(rows))
            filename, version = row['file'], row['version']

            if version not in dbs:
                versionNotInDbs.add(version)
                continue

            fileEnts = dbs[version].lookup(filename, "File")

            if not len(fileEnts):
                print(f'WARNING: {filename} does not exist in DB {version}.')
                continue

            for classRef in fileEnts[0].refs("Define", "Class"):
                row['class'] = classRef.ent().longname()
                writer.writerow(row)

        print(f'WARNING: following versions {versionNotInDbs} not in DB. Remove related rows.')


def getVersion(filename, projectName):
    removeProjName = filename.replace(projectName + "-", "")
    version = "-".join(removeProjName.split("-")[:-1])
    return version


def readDbs(udbDir, projectName):
    dbs = {}
    filesInProj = [x for x in os.listdir(udbDir) if x.startswith(projectName)]

    print("Start reading database")
    for idx, filename in enumerate(filesInProj, start=1):
        print(f"Reading database {idx}/{len(filesInProj)}")
        version = getVersion(filename, projectName)
        dbs[version] = understand.open(os.path.join(udbDir, filename))
    print("Reading database done")
    return dbs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="python3 mapFileToClass udbDir tomcat-apache xx/xxx.csv")
    parser.add_argument("udbDir", help="The directory contains the udb files")
    parser.add_argument("projectName", help="The project name used to find udb files in udbFilePath.")
    parser.add_argument("rawData", help="The path to the data file containing 'file' and 'version' column.")
    args = parser.parse_args()
    main(args.udbDir, args.projectName, args.rawData)
