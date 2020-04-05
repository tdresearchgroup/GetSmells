import csv
import os
import subprocess
from copy import deepcopy

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

    def extractSmells(self):
        outputDir = os.path.join(self.outputPath, self.projectName)
        outputCsvFileClasses = os.path.join(outputDir, "smells-classes.csv")
        outputCsvFileMethods = os.path.join(outputDir, "smells-methods.csv")
        outputCsvFilePackages = os.path.join(outputDir, "smells-packages.csv")
        outputCsvFileOverall = os.path.join(outputDir, self.projectName + "-overall.csv")

        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        db = understand.open(self.udbFile)
        classEnts = db.ents("Class ~Unresolved ~Unknown ~Anonymous ~Enum")
        methodEnts = db.ents("Method ~Unresolved ~Unknown")

        clsPkMap = self._getClsPkMap(classEnts)

        methodSmellExtractor = MethodLevelSmellExtractor(methodEnts)
        methodSmells = methodSmellExtractor.getSmells()
        self._generateDetailReport(outputCsvFileMethods,
                                   methodSmells,
                                   methodSmellExtractor.getMethodMetrics())

        classSmellExtractor = ClassLevelSmellExtractor(classEnts)
        classSmells = classSmellExtractor.getSmells(methodSmells)
        self._generateDetailReport(outputCsvFileClasses,
                                   classSmells,
                                   classSmellExtractor.getClassMetrics())

        packageSmellExtractor = PackageSmellExtractor(classEnts, clsPkMap)
        packageSmells = packageSmellExtractor.getSmells()
        self._generateDetailReport(outputCsvFilePackages,
                                   packageSmells,
                                   packageSmellExtractor.getPackageMetrics())

        self._generateOverallReport(methodSmells, classSmells, packageSmells, clsPkMap, outputCsvFileOverall)

    def _getSmellSummary(self, extractedSmells):
        smellSummary = {x: set() for x in next(iter(extractedSmells.values()))}
        for entName, smellDict in extractedSmells.items():
            for smellName, isSmell in smellDict.items():
                if isSmell:
                    smellSummary[smellName].add(entName)
        return smellSummary

    def _generateDetailReport(self, outputCsvFileName, smells, metrics):
        """
        Generate 2 reports. One with metrics, one doesn't
        :param outputCsvFileName: filename without metrics
        :param smells: smell dict. Format as {longName: {smell1: 1, smell2: 2}}
        :param metrics: metrics dict. Format as {longName: {metric1: 1, metric2: 2}}
        :return: None
        """
        data = deepcopy(smells)

        # detail without metrics
        fieldnames = ['Name'] + [x for x in next(iter(smells.values()))]
        for longName, smellDict in data.items():
            smellDict['Name'] = longName
        self._outputCsvFile(data.values(), outputCsvFileName, fieldnames)

        # detail with metrics
        filename, extension = os.path.splitext(outputCsvFileName)
        outputWithMetrics = filename + "-metrics" + extension
        fieldnames += [x for x in next(iter(metrics.values()))]
        for longName, smellDict in data.items():
            smellDict.update(metrics[longName])
        self._outputCsvFile(data.values(), outputWithMetrics, fieldnames)

    def _runCmd(self, args):
        args = args if IS_WINDOWS else " ".join(args)
        subprocess.run(args, shell=True, check=True, stdout=subprocess.DEVNULL)

    def _getClassName(self, methodName):
        return '.'.join(methodName.split('.')[:-1])

    def _generateOverallReport(self, methodSmells, classSmells, packageSmells, clsPkMap, outputCsvFileOverall):
        orderedColNames = ['Name'] + \
                          [x for x in next(iter(classSmells.values()))] + \
                          [x for x in next(iter(methodSmells.values()))] + \
                          [x for x in next(iter(packageSmells.values()))] + \
                          ["Total"] + \
                          ["Distinct_Count"]

        # integrate package smells
        for longName, smellDict in classSmells.items():
            packageName = clsPkMap[longName]
            if packageName not in packageSmells:
                print(f"WARNING: class: {longName} with packageName: {packageName} is not in package smell dict")
            else:
                smellDict.update(packageSmells[packageName])

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

        for longName, smellDict in classSmells.items():
            smellDict["Total"] = sum(smellDict.values())
            smellDict["Distinct_Count"] = len([1 for x in smellDict.values() if x > 0])
            smellDict["Name"] = longName

        self._outputCsvFile(classSmells.values(), outputCsvFileOverall, orderedColNames)

    def _outputCsvFile(self, data, fileName, orderedColNames):
        with open(fileName, 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=orderedColNames, delimiter=",")
            writer.writeheader()
            writer.writerows(data)

    def _getClsPkMap(self, classEnts):
        def getPkName(clsEnt):
            pkRef = clsEnt.ref("Containin", "Package")
            otherRef = clsEnt.ref("Definein")
            if pkRef:
                return pkRef.ent().longname()
            if otherRef:
                return getPkName(otherRef.ent())
            return ""

        pkClsDict = {}
        for classEnt in classEnts:
            pkName = getPkName(classEnt)
            if pkName:
                pkClsDict[classEnt.longname()] = pkName
            else:
                print(f"WARNING: class: {classEnt.longname()} not in any package")
        return pkClsDict

