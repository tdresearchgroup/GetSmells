from src.common import getQuartile, getMean, getCumulativeZ, getMedian, printProgress
from src.classLevel.classLevelMetricsUtil import ClassLevelMetricsUtil
from src.common.dfs import getCyclicVertex
GOD_CLASS_AFTD_FEW = 4
ONE_THIRD = 1/3
HIGH_LCOM = 73 #0.725

#for use with PMD style data class methodology
HIGH_NOPA = 5
VERY_HIGH_NOPA = 3
HIGH_WMC = 30
VERY_HIGH_WMC = 45


class ClassLevelSmellExtractor:
    def __init__(self, classEnts):
        self.__classEnts = classEnts
        self.__classMetrics = ClassLevelMetricsUtil(classEnts).generateMetrics()

    def getSmells(self, methodSmells):
        classSmells = {}
        totalClassCount = len(self.__classMetrics)
        print("\tExtracting smells for", totalClassCount, "classes...")

        firstQuatileLOC = getQuartile(self.getMetricDistribution("LOC"), 1)
        meanLOC = getMean(self.getMetricDistribution("LOC"))
        veryHighWMC = getCumulativeZ(self.getMetricDistribution("WMC"), 1.44)
        medianHubIn = getMedian(self.getMetricDistribution("Hub_In"))
        medianHubOut = getMedian(self.getMetricDistribution("Hub_Out"))

        cyclicDepSmells = self.getCyclicDepSmells()
        unhealthyInheritanceSmells = self.getUnhealthyInheritanceSmells()

        for methodLongName, smellDict in methodSmells.items():
            className = self.__methodName2className(methodLongName)
            if smellDict["Brain_Method"]:
                self.__classMetrics[className]["numberOfBrainMethod"] += 1

        for longName, metrics in self.__classMetrics.items():
            classSmells[longName] = {"God_Class": self.isGodClass(metrics, veryHighWMC),
                                     "Lazy_Class": self.isLazyClass(metrics, firstQuatileLOC),
                                     "Complex_Class": self.isComplexClass(metrics),
                                     "Long_Class": self.isLongClass(metrics, meanLOC),
                                     "Refused_Request": self.isRefusedBequest(metrics),
                                     "Data_Class": self.isDataClass(metrics),
                                     "Feature_Envy": self.isFeatureEnvy(metrics),
                                     "Brain_Class": self.isBrainClass(metrics, veryHighWMC),
                                     "Hub_Like_Dependency": self.isHubLikeDependency(metrics, medianHubIn, medianHubOut),
                                     "Class_Cyclic_Dependency": longName in cyclicDepSmells,
                                     "Unhealthy_Inheritance_Hierarchy": longName in unhealthyInheritanceSmells}
            printProgress(len(classSmells), totalClassCount)

        return classSmells

    def __methodName2className(self, methodName):
        return '.'.join(methodName.split('.')[:-1])

    def __getClassDependsGraph(self):
        graph = {}
        for classEnt in self.__classEnts:
            # dependsByEnts include [Class, Interface, Annotation]
            # However, by definition in paper, only includes class here
            graph[classEnt.longname()] = {x.longname() for x in classEnt.dependsby().keys()
                                          if x in self.__classEnts}
        return graph

    def getUnhealthyInheritanceSmells(self):
        smells = set()
        for classEnt in self.__classEnts:
            dependNames = self.__getDependNames(classEnt)

            childrenNames = self.__getChildrenNames(classEnt)
            if len(childrenNames.intersection(dependNames)) > 0:
                smells.add(classEnt.longname())
                continue

            for depend in classEnt.depends().keys():
                dChildrenNames = self.__getChildrenNames(depend)
                if dChildrenNames.issubset(dependNames):
                    smells.add(classEnt.longname())
                    break
        return smells

    def __getDependNames(self, classEnt):
        return {x.longname() for x in classEnt.depends().keys()}

    def __getChildrenNames(self, classEnt):
        return {x.ent().longname() for x in classEnt.refs("Extendby", "Class")}

    def isHubLikeDependency(self, metrics, medianHubIn, medianHubOut):
        return metrics["Hub_In"] > medianHubIn and metrics["Hub_Out"] > medianHubOut and \
               abs(metrics["Hub_In"] - metrics["Hub_Out"]) < 1/4 * (metrics["Hub_In"] + metrics["Hub_Out"])

    def getCyclicDepSmells(self):
        graph = self.__getClassDependsGraph()
        return getCyclicVertex(graph)

    def getClassMetrics(self):
        return self.__classMetrics

    def getMetricDistribution(self, metricName):
        return [x[metricName] for x in self.__classMetrics.values()]

    def isGodClass(self, metrics, veryHighWMC):
        return metrics["ATFD"] > GOD_CLASS_AFTD_FEW and \
               metrics["WMC"] >= veryHighWMC and \
               metrics["TCC"] < ONE_THIRD

    def isLazyClass(self, metrics, firstQuatileLOC):
        return metrics["LOC"] < firstQuatileLOC

    def isComplexClass(self, metrics):
        return metrics["CMC"] >= 1

    def isLongClass(self, metrics, meanLOC):
        return metrics["LOC"] > meanLOC

    def isRefusedBequest(self, metrics):
        return metrics["LMC"] > .5 * metrics["TMC"] and \
               metrics["LMC"] != metrics["TMC"]

    def isDataClass(self, metrics):
        return (metrics["WMC"] <= HIGH_WMC and metrics["NOPA"] >= HIGH_NOPA) or \
               (metrics["WMC"] <= VERY_HIGH_WMC and metrics["NOPA"] >= VERY_HIGH_NOPA)

    def isFeatureEnvy(self, metrics):
        return metrics["LCOM"] > HIGH_LCOM

    def isBrainClass(self, metrics, veryHighWMC):
        return not self.isGodClass(metrics, veryHighWMC) and \
               metrics["WMC"] >= 47 and \
               metrics["TCC"] < 0.5 and \
               ((metrics["numberOfBrainMethod"] > 1 and metrics["LOC"] >= 197) or
                (metrics["numberOfBrainMethod"] == 1 and metrics["LOC"] >= 2*197 and metrics["WMC"] >= 2*47))
