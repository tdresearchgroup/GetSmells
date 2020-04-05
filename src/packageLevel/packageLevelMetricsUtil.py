class PackageLevelMetricsUtil:

    def __init__(self, classEnts, clsPkMap):
        self.classEnts = classEnts
        self.clsPkMap = clsPkMap

    def generateMetrics(self):
        packageLib = {}
        print("\tCalculating metrics for packages...")

        for classEnt in self.classEnts:
            packageName = self.clsPkMap[classEnt.longname()]

            if packageName not in packageLib:
                packageLib[packageName] = ({"dependsOnPk": set(),
                                            "dependsOnClass": set(),
                                            "dependsByClass": set(),
                                            "instability": 0})

                packageLib[packageName]["dependsOnClass"].update({x.longname() for x in classEnt.depends().keys()
                                                                  if x in self.classEnts and packageName != self.clsPkMap[x.longname()]})

                packageLib[packageName]["dependsByClass"].update({x.longname() for x in classEnt.dependsby().keys()
                                                                  if x in self.classEnts and packageName != self.clsPkMap[x.longname()]})

                packageLib[packageName]["dependsOnPk"].update({self.clsPkMap[x.longname()] for x in classEnt.depends().keys()
                                                              if x in self.classEnts and packageName != self.clsPkMap[x.longname()]})

        self.__addPkInstabilityInfo(packageLib)

        return packageLib

    def __addPkInstabilityInfo(self, packageLib):
        for metrics in packageLib.values():
            ce = len(metrics["dependsOnClass"])
            ca = len(metrics["dependsByClass"])
            metrics["instability"] = (ce / (ca + ce or 1))
