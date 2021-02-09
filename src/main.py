import datetime
import os.path
import configparser
from src import DEFAULT_OUTPUT, PROJECT_PATH
import shutil
import sys
from app import App


def main(nameDirPairs):
    # print(f"{datetime.datetime.now()}\nStarting GetSmells, output at '{DEFAULT_OUTPUT})\n")

    for projName, projDir in nameDirPairs:
        cleanSmellOutput(projName)
        projDirs = [f.path for f in os.scandir(projDir) if f.is_dir()] if projDir else []

        l = len(projDirs)
        i=0
        printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        for sourcePath in projDirs:
            version = getVersion(os.path.split(sourcePath)[-1], projName)

            if not os.path.isdir(sourcePath):
                print("Error: The specified source path either does not exist or is not a directory")
                continue

            # print(f"{datetime.datetime.now()}\nStarting GetSmells on '{projName}' with version '{version}'\n")
            app = App(sourcePath, DEFAULT_OUTPUT, projName, version)

            # print(f"Step 1/2: Creating an Understand Project'")
            app.analyzeCode()

            # print(f"Step 2/2: Extracting code smells from metrics'")
            sys.stdout.flush()
            app.extractSmells()
            
            i += 1
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
            # print("GetSmells complete!")
        break

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    sys.stdout.flush()
    # Print New Line on Complete
    if iteration == total: 
        print()

def cleanSmellOutput(projName):
    outputDir = f'{DEFAULT_OUTPUT}/smells/{projName}'
    outputOverall = f'{DEFAULT_OUTPUT}/smells/{projName}.csv'

    # print(f"Clean existing smell output at '{outputDir}' & '{outputOverall}')\n")
    shutil.rmtree(outputDir, ignore_errors=True)
    if os.path.isfile(outputOverall):
        os.remove(outputOverall)


def getVersion(filename, projectName):
    removeProjName = filename.replace(projectName + "-", "")
    version = "-".join(removeProjName.split("-")[:-1])
    return version


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(os.path.join(PROJECT_PATH, 'config.ini'))
    main(config.items('main.projPaths'))
