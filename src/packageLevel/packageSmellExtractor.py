from src.common.dfs import getCyclicVertex


class PackageSmellUtil:

    def __init__(self, classEnts):
        self.caceInfo = {}
        self.classEnts = classEnts
        self.pkDependsClass = {}
        self.pkDependsOnPk = {}
        self.__generatePkDependsInfo()

    def getPackageName(self, classEnt):
        return '.'.join(classEnt.longname().split('.')[:-1])

    def __generatePkDependsInfo(self):
        if self.pkDependsClass or self.pkDependsOnPk:
            pass

        for classEnt in self.classEnts:
            packageName = self.getPackageName(classEnt)

            dependsOnClass = {x.longname() for x in classEnt.depends().keys() if packageName != self.getPackageName(x)}
            dependsByClass = {x.longname() for x in classEnt.dependsby().keys() if packageName != self.getPackageName(x)}
            dependsOnPk = {self.getPackageName(x) for x in classEnt.depends().keys() if packageName != self.getPackageName(x)}

            if packageName in self.pkDependsClass:
                self.pkDependsClass[packageName][0].update(dependsOnClass)
                self.pkDependsClass[packageName][1].update(dependsByClass)
                self.pkDependsOnPk[packageName].update(dependsOnPk)
            else:
                self.pkDependsClass[packageName] = (dependsOnClass, dependsByClass)
                self.pkDependsOnPk[packageName] = dependsOnPk

    def __getPkInstabilityInfo(self):
        pkInstabilityDict = {}
        for packageName, dependsInfo in self.pkDependsClass.items():
            ce = len(dependsInfo[0])
            ca = len(dependsInfo[1])
            pkInstabilityDict[packageName] = (ce / (ca + ce))

        return pkInstabilityDict

    def getUnstableDepSmell(self):
        smellPks = set()
        pkInstabilityDict = self.__getPkInstabilityInfo()

        for pk, dependsOnPkSet in self.pkDependsOnPk.items():
            pkInstability = pkInstabilityDict[pk]

            for dependsOnPk in dependsOnPkSet:
                if pkInstability < pkInstabilityDict[dependsOnPk]:
                    smellPks.add(dependsOnPk)

        return smellPks

    def getCyclicDepSmell(self):
        return getCyclicVertex(self.pkDependsOnPk)
