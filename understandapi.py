import sys
import platform
import statistics
import os
import numpy as np
import csv
from packageSmellUtil import PackageSmellUtil
from methodLevelMetricsUtil import MethodLevelMetricsUtil
from classLevelMetricsUtil import ClassLevelMetricsUtil
from methodLevelSmellExtractor import MethodLevelSmellExtractor
from classLevelSmellExtractor import ClassLevelSmellExtractor

if platform.system() == "Windows":
    sys.path.append('C:/Program Files/SciTools/bin/pc-win64/Python')
else:
    sys.path.append('/Applications/Understand.app/Contents/MacOS/Python')

# Relevant Understand API Documentation:
# https://scitools.com/sup/api-2/
# https://scitools.com/documents/manuals/python/understand.html
# help(understand)
import understand




# -------------------------
#       SMELLS
# -------------------------

# def extractSmells(projectPath, outputPath, runName, log, includeMetricsInCsv = True):
#     delm = ","
#     #includeMetricsInCsv = True
#
#     FEW = 4
#     ONE_THIRD = 1/3
#     HIGH_METHOD_COMPLEXITY = 10
#     HIGH_LCOM = 73 #0.725
#
#     #for use with PMD style data class methodology
#     HIGH_NOPA = 5
#     VERY_HIGH_NOPA = 3
#     HIGH_WMC = 30
#     VERY_HIGH_WMC = 45
#
#
#     outputCsvFileClasses = os.path.join(outputPath, runName + "-smells-classes.csv")
#     outputCsvFileMethods = os.path.join(outputPath, runName + "-smells-methods.csv")
#     outputTxtDirClasses = os.path.join(outputPath, runName + "-smelly-classes")
#     outputTxtDirMethods = os.path.join(outputPath, runName + "-smelly-methods")
#     if not os.path.exists(outputTxtDirClasses):
#         os.makedirs(outputTxtDirClasses)
#     if not os.path.exists(outputTxtDirMethods):
#         os.makedirs(outputTxtDirMethods)
#
#     db = understand.open(projectPath)
#     classEnts = db.ents("Class ~Unresolved ~Unknown")
#     methodEnts = db.ents("Method ~Unresolved ~Unknown")
#
#     packageSmellUtil = PackageSmellUtil(classEnts)
#     packageSmellUtil.getUnstableDepSmell()
#
#     print("\tCalculating complex metrics for", len(classEnts), " classes...")
#
#
#     print("\tCalculating complex metrics for", len(methodEnts), " methods...")
#
#
#
#     print("\tCalculating system-wide averages and metrics")
#
#     meanClassWMC = statistics.mean(allClassWMC)
#     devClassWMC = statistics.pstdev(allClassWMC)
#     # TODO(performance improvement): Improve such that 1st quartile LOC can be cacluated without storing all
#     # observations (see http://www.cs.wustl.edu/~jain/papers/ftp/psqr.pdf) for "Lazy Class"
#     firstQuartileClassLOC = np.percentile(allClassLOC, 25) # Get the 1st quartitle
#     meanClassLOC = statistics.mean(allClassLOC)
#     meanMethodLoc = statistics.mean(allMethodLOC)
#     meanMethodInputs = statistics.mean(allMethodInputs)
#
#     log.write("Class WMC: mean = " + str(meanClassWMC) + ", pstdev = " + str(devClassWMC) + ", VERY_HIGH = " + str(veryHighClassWMC) + "\n")
#     log.write("Class LOC: 1st Quartile = " + str(firstQuartileClassLOC) + "\n")
#     log.write("Class LOC: mean = " + str(meanClassLOC) + "\n")
#     log.write("Method LOC: mean = " + str(meanMethodLoc) + "\n")
#     log.write("Method Inputs: mean = " + str(meanMethodInputs) + "\n")
#     log.write("M")
#
#     print("\tApplying code smell thresholds")
#
#     # Apply Class-Level Smells
#     classSmells = {'god': set(),
#                    'lazy': set(),
#                    'complex': set(),
#                    'refusedBequest': set(),
#                    'long': set(),
#                    'dataClass': set(),
#                    'featureEnvy': set(),
#                    'brainClass': set()}
#
#     outputFile = open(outputCsvFileClasses, "w")
#     outputData = delm.join(["Class", "God Class", "Lazy Class", "Complex Class", "Long Class", "Refused Bequest", "Data Class", "Feature Envy"])
#     if includeMetricsInCsv:
#         outputData += delm + delm.join(["Metric: ATFD", "Metric: WMC", "Metric: TCC", "Metric: LOC", "Metric: CMC", "Metric: TMC", "Metric: LMC", "Metric: NOPA", "Metric: LCOM (%)"])
#     outputFile.write(outputData + "\n")
#
#     for longName, metrics in classLib.items():
#         # God Class
#         # - ATFD (Access to Foreign Data) > Few
#         # - WMC (Weighted Method Count) >= Very High
#         # - TCC (Tight Class Cohesion) < 1/3
#         classSmellGod = (metrics["ATFD"] > FEW) and (metrics["WMC"] >= veryHighClassWMC) and (metrics["TCC"] < ONE_THIRD)
#
#         # Lazy Class
#         # - LOC (Lines of Code) < 1st quartile of system
#         classSmellLazy = (metrics["LOC"] < firstQuartileClassLOC)
#
#         # Complex Class
#         # - CMC (Complex Method Count; number of methods with complexity > HIGH_METHOD_COMPLEXITY) >= 1
#         classSmellComplex = (metrics["CMC"] >= 1)
#
#         classSmellLong = (metrics["LOC"] > meanClassLOC)
#
#         classSmellRefusedBequest = (metrics["LMC"] > (.5 * metrics["TMC"])) and (metrics["LMC"] != metrics["TMC"])
#
#         classSmellDatmetrics = ( (metrics["WMC"] <= HIGH_WMC and metrics["NOPA"] >= HIGH_NOPA) or (metrics["WMC"] <= VERY_HIGH_WMC and metrics["NOPA"] >= VERY_HIGH_NOPA) )
#
#         classSmellFeatureEnvy = (metrics["LCOM"] > HIGH_LCOM)
#
#         classSmellBrainClass = (not classSmellGod and
#                                 metrics["WMC"] >= 47 and
#                                 metrics["TCC"] < 0.5 and
#                                 ((metrics["numberOfBrainMethod"] > 1 and metrics["LOC"] >= 197) or
#                                  (metrics["numberOfBrainMethod"] == 1 and metrics["LOC"] >= 2*197 and metrics["WMC"] >= 2*47)))
#
#         if classSmellGod:
#             classSmells['god'].add(longName)
#         if classSmellLazy:
#             classSmells['lazy'].add(longName)
#         if classSmellComplex:
#             classSmells['complex'].add(longName)
#         if classSmellLong:
#             classSmells['long'].add(longName)
#         if classSmellRefusedBequest:
#             classSmells['refusedBequest'].add(longName)
#         if classSmellDatmetrics:
#             classSmells['datmetrics'].add(longName)
#         if classSmellFeatureEnvy:
#             classSmells['featureEnvy'].add(longName)
#         if classSmellBrainClass:
#             classSmells['brainClass'].add(longName)
#
#         csvLine = delm.join([longName, str(classSmellGod), str(classSmellLazy), str(classSmellComplex), str(classSmellLong), str(classSmellRefusedBequest), str(classSmellDatmetrics), str(classSmellFeatureEnvy), str(classSmellBrainClass)])
#         if includeMetricsInCsv:
#             csvLine += delm + delm.join([str(metrics["ATFD"]), str(metrics["WMC"]), str(metrics["TCC"]), str(metrics["LOC"]), str(metrics["CMC"]), str(metrics["LMC"]), str(metrics["TMC"]), str(metrics["NOPA"]), str(metrics["LCOM"])])
#         outputFile.write(csvLine + "\n")
#
#     outputFile.close()
#
#     # Apply Method-Level Smells
#     methodSmells = {'long': set(),
#                     'lpl': set(),
#                     'shotgunSurgery': set(),
#                     'brainMethod': set()}
#
#     outputFile = open(outputCsvFileMethods, "w")
#     outputData = delm.join(["Method", "Long Method", "Long Parameter List"])
#     if includeMetricsInCsv:
#         outputData += delm + delm.join(["Metric: LOC", "Metric: inputs"])
#     outputFile.write(outputData + "\n")
#
#     for amethod in methodLib:
#         # Long Method
#         # - LOC (Lines of Code) > mean of system
#         # methodSmellLong = (amethod["LOC"] > meanMethodLoc)
#
#         # - LOC (Lines of Code) > 20 - Zadia
#         methodSmellLong = (amethod["LOC"] > 20)
#
#         methodSmellLongParameterList = (amethod["inputs"] > meanMethodInputs)
#
#         # Shotgun Surgery
#         # - CM (Changing Methods) > 10
#         # - CC (Changing Classes) > 5
#         methodSmellShotGunSurgery = (amethod["CM"] > 10 and amethod["CC"] > 5)
#
#         # Brain Method
#         # - LOC (Line of Code) > 65
#         # - CYCLO(Cyclomatic Complexity) / LOC(Line of Code) >= 0.24
#         # - MAXNESTING(Maximum Nesting Level) >= 5
#         # - NOAV(Number of Accessed Variables) > 8
#         methodSmellBrainMethod = (amethod["LOC"] > 65 and amethod["CYCLO"] >= 0.24 and
#                                   amethod["MAXNESTING"] >= 5 and amethod["NOAV"] > 8)
#
#         if methodSmellLong:
#             methodSmells['long'].add(amethod["name"])
#         if methodSmellLongParameterList:
#             methodSmells['lpl'].add(amethod["name"])
#         if methodSmellShotGunSurgery:
#             methodSmells['shotgunSurgery'].add(amethod["name"])
#         if methodSmellBrainMethod:
#             methodSmells['brainMethod'].add(amethod["name"])
#
#         csvLine = delm.join([amethod["name"], str(methodSmellLong), str(methodSmellLongParameterList)])
#         if includeMetricsInCsv:
#             csvLine += delm + delm.join([str(amethod["LOC"]), str(amethod["inputs"])])
#         outputFile.write(csvLine + "\n")
#
#     outputFile.close()
#
#     print("\tWriting list of smelly classes/methods")
#
#     summaryData = "\tCode smell extraction complete"
#     summaryData = "\tNumber of Class-Level Smells:"
#     for smellName, classes in classSmells.items():
#         outputFileName = os.path.join(outputTxtDirClasses, smellName + ".txt")
#         outputFile = open(outputFileName, "w")
#         for className in classes:
#             outputFile.write(className + "\n")
#         outputFile.close()
#         summaryData += "\n\t\t" + smellName +"  = " + str(len(classes))
#
#
#     summaryData += "\n\tNumber of Method-Level Smells:"
#     for smellName, methods in methodSmells.items():
#         outputFileName = os.path.join(outputTxtDirMethods, smellName + ".txt")
#         outputFile = open(outputFileName, "w")
#         for methodName in methods:
#             outputFile.write(methodName + "\n")
#         outputFile.close()
#         summaryData += "\n\t\t" + smellName +" = " + str(len(methods))
#
#     log.write("\n" + summaryData)
#     print(summaryData + "\n")



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
    fieldnames = ['Name'] + [x for x in next(iter(smells.values()))] + [x for x in next(iter(metrics.values()))] if metrics else []
    with open(outputCsvFileName, 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter=",")
        for longName, smellDict in smells.items():
            row = {'Name': longName}
            row.update(smellDict)
            row.update(metrics[longName])
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
    classSmells = classSmellExtractor.getSmells()
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
