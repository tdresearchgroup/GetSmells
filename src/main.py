import argparse
import datetime
import os.path

from app import App

DEFAULT_OUTPUT = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "getsmells-output")


def main(sourcePaths, outputPath):
    for sourcePath in sourcePaths:
        projectName = os.path.split(sourcePath)[-1]
        sourcePath = os.path.normcase(sourcePath)
        outputPath = os.path.normcase(outputPath or DEFAULT_OUTPUT)

        if not os.path.isdir(sourcePath):
            print("Error: The specified source path either does not exist or is not a directory")
            continue

        app = App(sourcePath, outputPath)

        print(f"{datetime.datetime.now()}\nStarting GetSmells on '{sourcePath}' (output at '{outputPath})\n")
        print(f"Step 1/2: Creating an Understand Project for '{projectName}'")
        app.analyzeCode()

        print(f"Step 2/2: Extracting code smells from metrics on '{projectName}'")
        app.extractSmells()

        print("GetSmells complete!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Usage: python3 main.py -d xxx/projects/android\n"
                                                 "Or usage: python3 main.py xx/android6 xx/android7 xx/andoid8\n"
                                                 "Or usage: python3 main.py -d xxx/projects/android xx/tomcat6.0.1 xxx/tomcat6.0.2")
    parser.add_argument("sourcePaths", nargs="*", help="The path to the directory with a single project's code")
    parser.add_argument("-o", "--outputPath", help="The directory to output the CSVs with code smells")
    parser.add_argument("-d", "--projDir", help="The direct parent directory contains all projects")
    args = parser.parse_args()
    projDir = [f.path for f in os.scandir(args.projDir) if f.is_dir()] if args.projDir else []

    main(args.sourcePaths + projDir, args.outputPath)

