from src.common.dfs import getCyclicVertex
from packageLevel.packageLevelMetricsUtil import PackageLevelMetricsUtil


class PackageSmellExtractor:

    def __init__(self, classEnts):
        self.__packageMetrics = PackageLevelMetricsUtil(classEnts).generateMetrics()

    def getCyclicDepSmells(self, pkDependsOnPk):
        return getCyclicVertex(pkDependsOnPk)

    def isUnstableDependency(self, metrics):
        for dependsOnPk in metrics["dependsOnPk"]:
            if metrics["instability"] < self.__packageMetrics[dependsOnPk]["instability"]:
                return dependsOnPk
        return ""

    def getSmells(self):
        print(f"\tExtracting smells for {len(self.__packageMetrics)} packages...")
        packageSmells = {}
        cyclicDepSmells = self.getCyclicDepSmells({k: v["dependsOnPk"] for k, v in self.__packageMetrics.items()})
        for pkName, metrics in self.__packageMetrics.items():
            packageSmells[pkName] = {"Unstable_Dependency": self.isUnstableDependency(metrics),
                                     "Cyclic_Dependency": pkName in cyclicDepSmells}
        return packageSmells

    def getPackageMetrics(self):
        return self.__packageMetrics

