import datetime
import os.path
import configparser
from src import DEFAULT_OUTPUT
import shutil

from app import App


def main(nameDirPairs):
    print(f"{datetime.datetime.now()}\nStarting GetSmells, output at '{DEFAULT_OUTPUT})\n")

    for projName, projDir in nameDirPairs:
        cleanSmellOutput(projName)
        projDirs = [f.path for f in os.scandir(projDir) if f.is_dir()] if projDir else []
        for sourcePath in projDirs:
            version = getVersion(os.path.split(sourcePath)[-1], projName)

            if not os.path.isdir(sourcePath):
                print("Error: The specified source path either does not exist or is not a directory")
                continue

            print(f"{datetime.datetime.now()}\nStarting GetSmells on '{projName}' with version '{version}'\n")
            app = App(sourcePath, DEFAULT_OUTPUT, projName, version)

            print(f"Step 1/2: Creating an Understand Project'")
            app.analyzeCode()

            print(f"Step 2/2: Extracting code smells from metrics'")
            app.extractSmells()

            print("GetSmells complete!")


def cleanSmellOutput(projName):
    outputDir = f'{DEFAULT_OUTPUT}/smells/{projName}'
    outputOverall = f'{DEFAULT_OUTPUT}/smells/{projName}.csv'

    print(f"Clean existing smell output at '{outputDir}' & '{outputOverall}')\n")
    shutil.rmtree(outputDir, ignore_errors=True)
    if os.path.isfile(outputOverall):
        os.remove(outputOverall)


def getVersion(filename, projectName):
    removeProjName = filename.replace(projectName + "-", "")
    version = "-".join(removeProjName.split("-")[:-1])
    return version


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    main(config.items('main.projPaths'))


