import os
import csv
import argparse


def main(projects, fileDir):
    """
    After vulIntegration, we got one file per version*project
    This function is responsible for combining all versions together and generate one file per project
    :param projects: a list of string indicating projects to be combined
    :param fileDir: the directory contained these "one file per version*project"
    :return:
    """
    for project in projects:
        print(f"Start {project} version combination...")
        files = [os.path.join(fileDir, f) for f in os.listdir(fileDir)
                 if os.path.isfile(os.path.join(fileDir, f)) and project in f]

        if not files:
            print(f"WARNING: cannot find csv file for {project}")
            continue

        with open(files[0], 'r') as f:
            header = csv.DictReader(f).fieldnames

        out = os.path.join(fileDir, f'{project}-allversions.csv')
        with open(out, 'w') as outf:
            writer = csv.DictWriter(outf, fieldnames=header, delimiter=",")
            writer.writeheader()

            for file in files:
                with open(file, 'r') as inf:
                    reader = csv.DictReader(inf)
                    writer.writerows(reader)
        print(f"Finish {project} version combination...")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='example: python3 oneFileForOneProj apache-cxf apache-tomcat android -d dir/smell&vul')
    parser.add_argument("projects", nargs="*", help="List of projects to be combined.")
    parser.add_argument("-d", "--fileDir", help="The directory contains all outputs from vulIntegration.py.")
    args = parser.parse_args()
    main(args.projects, args.fileDir)
