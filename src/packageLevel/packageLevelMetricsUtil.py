from src.common.dfs import getCyclicVertex


class PackageLevelMetricsUtil:

    def __init__(self, classEnts):
        self.classEnts = classEnts

    def getPackageName(self, classEnt):
        return '.'.join(classEnt.longname().split('.')[:-1])

    def generateMetrics(self):
        packageLib = {}
        print("\tCalculating metrics for packages...")

        for classEnt in self.classEnts:
            packageName = self.getPackageName(classEnt)

            if packageName not in packageLib:
                packageLib[packageName] = ({"dependsOnPk": set(),
                                            "dependsOnClass": set(),
                                            "dependsByClass": set(),
                                            "instability": 0})

            packageLib[packageName]["dependsOnClass"].update({x.longname() for x in classEnt.depends().keys()
                                                              if packageName != self.getPackageName(x) and x in self.classEnts})

            packageLib[packageName]["dependsByClass"].update({x.longname() for x in classEnt.dependsby().keys()
                                                              if packageName != self.getPackageName(x) and x in self.classEnts})

            packageLib[packageName]["dependsOnPk"].update({self.getPackageName(x) for x in classEnt.depends().keys()
                                                           if packageName != self.getPackageName(x) and x in self.classEnts})

        self.__addPkInstabilityInfo(packageLib)

        return packageLib

    def __addPkInstabilityInfo(self, packageLib):
        for metrics in packageLib.values():
            ce = len(metrics["dependsOnClass"])
            ca = len(metrics["dependsByClass"])
            metrics["instability"] = (ce / (ca + ce or 1))
