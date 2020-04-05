from src.common.dfs import getCyclicVertex
from packageLevel.packageLevelMetricsUtil import PackageLevelMetricsUtil


class PackageSmellExtractor:

    def __init__(self, classEnts, clsPkMap):
        self.__packageMetrics = PackageLevelMetricsUtil(classEnts, clsPkMap).generateMetrics()

    def getCyclicDepSmells(self, pkDependsOnPk):
        return getCyclicVertex(pkDependsOnPk)

    def isUnstableDependency(self, metrics):
        unstableSet = set()
        for dependsOnPk in metrics["dependsOnPk"]:
            if metrics["instability"] < self.__packageMetrics[dependsOnPk]["instability"]:
                unstableSet.add(dependsOnPk)
        metrics["unstableOn"] = unstableSet
        return unstableSet

    def getSmells(self):
        print(f"\tExtracting smells for {len(self.__packageMetrics)} packages...")
        packageSmells = {}
        cyclicDepSmells = self.getCyclicDepSmells({k: v["dependsOnPk"] for k, v in self.__packageMetrics.items()})
        for pkName, metrics in self.__packageMetrics.items():
            packageSmells[pkName] = {"Unstable_Dependency": len(self.isUnstableDependency(metrics)),
                                     "Package_Cyclic_Dependency": int(pkName in cyclicDepSmells)}
        return packageSmells

    def getPackageMetrics(self):
        return self.__packageMetrics

