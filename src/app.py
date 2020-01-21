import csv
import os
import subprocess

from classLevel import ClassLevelSmellExtractor
from methodLevel import MethodLevelSmellExtractor
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
        dirPath = os.path.dirname(self.udbFile)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        self._runCmd([UND_PATH, 'version'])
        self._runCmd([UND_PATH, 'create', '-languages', 'Java', self.udbFile])
        self._runCmd([UND_PATH, 'add', self.sourcePath, self.udbFile])
        self._runCmd([UND_PATH, 'settings', '-metrics', 'all', self.udbFile]),
        self._runCmd([UND_PATH, 'analyze', self.udbFile]),

    def extractSmells(self, includeMetricsInCsv=True):
        outputCsvFileClasses = os.path.join(self.outputPath, self.projectName + "-smells-classes.csv")
        outputCsvFileMethods = os.path.join(self.outputPath, self.projectName + "-smells-methods.csv")
        outputTxtDirClasses = os.path.join(self.outputPath, self.projectName + "-smelly-classes")
        outputTxtDirMethods = os.path.join(self.outputPath, self.projectName + "-smelly-methods")

        if not os.path.exists(outputTxtDirClasses):
            os.makedirs(outputTxtDirClasses)
        if not os.path.exists(outputTxtDirMethods):
            os.makedirs(outputTxtDirMethods)

        db = understand.open(self.udbFile)
        classEnts = db.ents("Class ~Unresolved ~Unknown")
        methodEnts = db.ents("Method ~Unresolved ~Unknown")

        methodSmellExtractor = MethodLevelSmellExtractor(methodEnts)
        methodSmells = methodSmellExtractor.getSmells()
        self._generateSummaryReport(methodSmells, outputTxtDirMethods)
        self._generateDetailReport(outputCsvFileMethods,
                                   methodSmells,
                                   methodSmellExtractor.getMethodMetrics() if includeMetricsInCsv else {})

        classSmellExtractor = ClassLevelSmellExtractor(classEnts)
        classSmells = classSmellExtractor.getSmells(methodSmells)
        self._generateSummaryReport(classSmells, outputTxtDirClasses)
        self._generateDetailReport(outputCsvFileClasses,
                                   classSmells,
                                   classSmellExtractor.getClassMetrics() if includeMetricsInCsv else {})

    def _getSmellSummary(self, extractedSmells):
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

    def _generateSummaryReport(self, smells, outputTxtDir):
        smellSummary = self._getSmellSummary(smells)
        for smellName, entNames in smellSummary.items():
            outputFileName = os.path.join(outputTxtDir, smellName + ".txt")
            with open(outputFileName, "w") as outputFile:
                outputFile.writelines(list(entNames))

    def _generateDetailReport(self, outputCsvFileName, smells, metrics):
        fieldnames = ['Name'] + [x for x in next(iter(smells.values()))] + \
                     ([x for x in next(iter(metrics.values()))] if metrics else [])

        with open(outputCsvFileName, 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter=",")
            for longName, smellDict in smells.items():
                row = {'Name': longName}
                row.update(smellDict)
                row.update(metrics[longName] if metrics else {})
                writer.writerow(row)

    def _runCmd(self, args):
        args = args if IS_WINDOWS else " ".join(args)
        subprocess.run(args, shell=True, check=True, stdout=subprocess.DEVNULL)


