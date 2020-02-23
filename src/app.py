import csv
import os
import subprocess

from classLevel import ClassLevelSmellExtractor
from methodLevel import MethodLevelSmellExtractor
from packageLevel import PackageSmellExtractor
from src import IS_WINDOWS, UND_PATH

import understand


class App:

    def __init__(self, sourcePath, outputPath):
        self.projectName = os.path.split(sourcePath)[-1]
        self.sourcePath = os.path.normcase(sourcePath)
        self.outputPath = os.path.normcase(outputPath or
                                           os.path.join(os.path.dirname(os.path.realpath(__file__)), "getsmells-output"))
        self.udbFile = os.path.join(outputPath, "udbs", self.projectName + ".udb")

    def analyzeCode(self):
        if os.path.isfile(self.udbFile):
            return

        dirPath = os.path.dirname(self.udbFile)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        self._runCmd([UND_PATH, 'version'])
        self._runCmd([UND_PATH, 'create', '-languages', 'Java', self.udbFile])
        self._runCmd([UND_PATH, 'add', self.sourcePath, self.udbFile])
        self._runCmd([UND_PATH, 'settings', '-metrics', 'all', self.udbFile]),
        self._runCmd([UND_PATH, 'analyze', self.udbFile]),

    def extractSmells(self, includeMetricsInCsv=True):
        outputDir = os.path.join(self.outputPath, self.projectName)
        outputCsvFileClasses = os.path.join(outputDir, "smells-classes.csv")
        outputCsvFileMethods = os.path.join(outputDir, "smells-methods.csv")
        outputCsvFilePackages = os.path.join(outputDir, "smells-packages.csv")
        outputCsvFileOverall = os.path.join(outputDir, self.projectName + "-overall.csv")

        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        db = understand.open(self.udbFile)
        classEnts = db.ents("Class ~Unresolved ~Unknown")
        methodEnts = db.ents("Method ~Unresolved ~Unknown")

        methodSmellExtractor = MethodLevelSmellExtractor(methodEnts)
        methodSmells = methodSmellExtractor.getSmells()
        self._generateDetailReport(outputCsvFileMethods,
                                   methodSmells,
                                   methodSmellExtractor.getMethodMetrics() if includeMetricsInCsv else {})

        classSmellExtractor = ClassLevelSmellExtractor(classEnts)
        classSmells = classSmellExtractor.getSmells(methodSmells)
        self._generateDetailReport(outputCsvFileClasses,
                                   classSmells,
                                   classSmellExtractor.getClassMetrics() if includeMetricsInCsv else {})

        packageSmellExtractor = PackageSmellExtractor(classEnts)
        packageSmells = packageSmellExtractor.getSmells()
        self._generateDetailReport(outputCsvFilePackages,
                                   packageSmells,
                                   packageSmellExtractor.getPackageMetrics() if includeMetricsInCsv else {})

        self._generateOverallReport(methodSmells, classSmells, packageSmells, outputCsvFileOverall)

    def _getSmellSummary(self, extractedSmells):
        smellSummary = {x: set() for x in next(iter(extractedSmells.values()))}
        for entName, smellDict in extractedSmells.items():
            for smellName, isSmell in smellDict.items():
                if isSmell:
                    smellSummary[smellName].add(entName)
        return smellSummary

    def _generateDetailReport(self, outputCsvFileName, smells, metrics):
        fieldnames = ['Name'] + [x for x in next(iter(smells.values()))] + \
                     ([x for x in next(iter(metrics.values()))] if metrics else [])

        with open(outputCsvFileName, 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter=",")
            writer.writeheader()
            for longName, smellDict in smells.items():
                row = {'Name': longName}
                row.update(smellDict)
                row.update(metrics[longName] if metrics else {})
                writer.writerow(row)

    def _runCmd(self, args):
        args = args if IS_WINDOWS else " ".join(args)
        subprocess.run(args, shell=True, check=True, stdout=subprocess.DEVNULL)

    def _getClassName(self, methodName):
        return '.'.join(methodName.split('.')[:-1])

    def _getPackageName(self, className):
        return '.'.join(className.split('.')[:-1])

    def _generateOverallReport(self, methodSmells, classSmells, packageSmells, outputCsvFileOverall):
        orderedColNames = ['Name'] + \
                          [x for x in next(iter(classSmells.values()))] + \
                          [x for x in next(iter(methodSmells.values()))] + \
                          [x for x in next(iter(packageSmells.values()))]

        # integrate package smells
        for longName, smellDict in classSmells.items():
            packageName = self._getPackageName(longName)
            if packageName not in packageSmells:
                print(f"WARNING: class: {longName} with packageName: {packageName} is not in package smell dict")
            else:
                smellDict.update(packageSmells[packageName])
            smellDict["Name"] = longName

        # integrate method smells
        for longName, smellDict in methodSmells.items():
            className = self._getClassName(longName)
            if className not in classSmells:
                # ignore interface methods
                # print(f"WARNING: method: {longName} with className: {className} is not in class smell dict")
                pass
            else:
                classSmellValue = classSmells[className]
                classSmellValue.update({key: classSmellValue.get(key, 0) + smellDict[key] for key in smellDict})

        self._outputCsvFile(classSmells.values(), outputCsvFileOverall, orderedColNames)

    def _outputCsvFile(self, data, fileName, orderedColNames):
        with open(fileName, 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=orderedColNames, delimiter=",")
            writer.writeheader()
            writer.writerows(data)
