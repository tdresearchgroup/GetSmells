import sys
import platform
import os
import csv
from src.methodLevel.methodLevelSmellExtractor import MethodLevelSmellExtractor
from src.classLevel.classLevelSmellExtractor import ClassLevelSmellExtractor

if platform.system() == "Windows":
    sys.path.append('C:/Program Files/SciTools/bin/pc-win64/Python')
else:
    sys.path.append('/Applications/Understand.app/Contents/MacOS/Python')

# Relevant Understand API Documentation:
# https://scitools.com/sup/api-2/
# https://scitools.com/documents/manuals/python/understand.html
# help(understand)
import understand


def getSmellSummary(extractedSmells):
    # methodSmells = {longName: {"Long_Method": False,
    #                            "Long_Parameter_List": False,
    #                            "Shotgun_Surgery": False,
    #                            "Brain_Method": False}}
    smellSummary = {x: set() for x in next(iter(extractedSmells.values()))}
    for entName, smellDict in extractedSmells.items():
        for smellName, isSmell in smellDict.items():
            if isSmell:
                smellSummary[smellName].add(entName)
    return smellSummary


def generateSummaryReport(smells, outputTxtDir):
    smellSummary = getSmellSummary(smells)
    for smellName, entNames in smellSummary.items():
        outputFileName = os.path.join(outputTxtDir, smellName + ".txt")
        with open(outputFileName, "w") as outputFile:
            outputFile.writelines(list(entNames))


def generateDetailReport(outputCsvFileName, smells, metrics):
    fieldnames = ['Name'] + [x for x in next(iter(smells.values()))] + \
                 ([x for x in next(iter(metrics.values()))] if metrics else [])

    with open(outputCsvFileName, 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter=",")
        for longName, smellDict in smells.items():
            row = {'Name': longName}
            row.update(smellDict)
            row.update(metrics[longName] if metrics else {})
            writer.writerow(row)


def extractSmells(projectPath, outputPath, runName, log, includeMetricsInCsv=True):
    outputCsvFileClasses = os.path.join(outputPath, runName + "-smells-classes.csv")
    outputCsvFileMethods = os.path.join(outputPath, runName + "-smells-methods.csv")
    outputTxtDirClasses = os.path.join(outputPath, runName + "-smelly-classes")
    outputTxtDirMethods = os.path.join(outputPath, runName + "-smelly-methods")

    if not os.path.exists(outputTxtDirClasses):
        os.makedirs(outputTxtDirClasses)
    if not os.path.exists(outputTxtDirMethods):
        os.makedirs(outputTxtDirMethods)

    db = understand.open(projectPath)
    classEnts = db.ents("Class ~Unresolved ~Unknown")
    methodEnts = db.ents("Method ~Unresolved ~Unknown")

    methodSmellExtractor = MethodLevelSmellExtractor(methodEnts)
    methodSmells = methodSmellExtractor.getSmells()
    generateSummaryReport(methodSmells, outputTxtDirMethods)
    generateDetailReport(outputCsvFileMethods,
                         methodSmells,
                         methodSmellExtractor.getMethodMetrics() if includeMetricsInCsv else {})

    classSmellExtractor = ClassLevelSmellExtractor(classEnts)
    classSmells = classSmellExtractor.getSmells(methodSmells)
    generateSummaryReport(classSmells, outputTxtDirClasses)
    generateDetailReport(outputCsvFileClasses,
                         classSmells,
                         classSmellExtractor.getClassMetrics() if includeMetricsInCsv else {})





if __name__ == '__main__':
    print("Running code smell extraction on an Understand project standalone using defaults")

    # Default project and output path
    if platform.system() == "Windows":
        logFile = open("C:/Users/cb1782/getsmells-test-output/understandapi-log.txt", "w+")
        extractSmells("C:/Users/cb1782/MyUnderstandProject.udb",
                      "C:/Users/cb1782/getsmells-test-output/",
                      "default",
                      logFile)
        logFile.close()
    else:
        logFile = open("/Users/charles/Documents/DIS/getsmells-test-output/understandapi-log.txt", "w+")
        extractSmells("/Users/charles/Documents/DIS/understandproject.udb",
                      "/Users/charles/Documents/DIS/getsmells-test-output/",
                      "default",
                      logFile)
        logFile.close()
