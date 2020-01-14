from src.common.statisticUtil import getQuartile, getMean, getCumulativeZ, getMedian
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

    def getSmells(self):
        classSmells = {}
        cyclicDepSmells = self.getCyclicDepSmells()
        unhealthyInheritanceSmells = self.getUnhealthyInheritanceSmells()

        for longName, metrics in self.__classMetrics.items():
            classSmells[longName] = {"God_Class": self.isGodClass(metrics),
                                     "Lazy_Class": self.isLazyClass(metrics),
                                     "Complex_Class": self.isComplexClass(metrics),
                                     "Long_Class": self.isLongClass(metrics),
                                     "Refused_Request": self.isRefusedBequest(metrics),
                                     "Data_Class": self.isDataClass(metrics),
                                     "Feature_Envy": self.isFeatureEnvy(metrics),
                                     "Brain_Class": self.isBrainClass(metrics),
                                     "Hub_Like_Dependency": self.isHubLikeDependency(metrics),
                                     "Cyclic_Dependency": longName in cyclicDepSmells,
                                     "Unhealthy_Inheritance_Hierarchy": longName in unhealthyInheritanceSmells}

        return classSmells

    def __getClassDependsGraph(self):
        graph = {}
        for classEnt in self.__classEnts:
            graph[classEnt.longname()] = {x.longname() for x in classEnt.dependsby().keys()}
        return graph

    def getUnhealthyInheritanceSmells(self):
        # a parent class depends on one of its children or
        # a class depends on a parent class and all its children
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

    def isHubLikeDependency(self, metrics):
        # Hub_In > Median(Hub_In) and Hub_Out > Median(Hub_Out)
        # |Hub_In - Hub_Out| < 1/4 *  (Hub_In + Hub_Out)
        dataListHubIn = self.getMetricDistribution("Hub_In")
        dataListHubOut = self.getMetricDistribution("Hub_Out")

        medianHubIn = getMedian(dataListHubIn)
        medianHubOut = getMedian(dataListHubOut)

        return metrics["Hub_In"] > medianHubIn and metrics["Hub_Out"] > medianHubOut and \
               abs(metrics["Hub_In"] - metrics["Hub_Out"]) < 1/4 * (metrics["Hub_In"] + metrics["Hub_Out"])

    def getCyclicDepSmells(self):
        graph = self.__getClassDependsGraph()
        return getCyclicVertex(graph)

    def getClassMetrics(self):
        return self.__classMetrics

    def getMetricDistribution(self, metricName):
        return [x[metricName] for x in self.__classMetrics.values()]

    def isGodClass(self, metrics):
        dataListWMC = self.getMetricDistribution("WMC")
        veryHigh = getCumulativeZ(dataListWMC, 1.5)

        return metrics["ATFD"] > GOD_CLASS_AFTD_FEW and \
               metrics["WMC"] >= veryHigh and \
               metrics["TCC"] < ONE_THIRD

    def isLazyClass(self, metrics):
        # Lazy Class
        # - LOC (Lines of Code) < 1st quartile of system
        dataListLOC = self.getMetricDistribution("LOC")
        firstQuatileLOC = getQuartile(dataListLOC, 1)
        return metrics["LOC"] < firstQuatileLOC

    def isComplexClass(self, metrics):
        # - CMC (Complex Method Count; number of methods with complexity > HIGH_METHOD_COMPLEXITY) >= 1
        return metrics["CMC"] >= 1

    def isLongClass(self, metrics):
        dataListLOC = self.getMetricDistribution("LOC")
        meanLOC = getMean(dataListLOC)
        return metrics["LOC"] > meanLOC

    def isRefusedBequest(self, metrics):
        return metrics["LMC"] > .5 * metrics["TMC"] and \
               metrics["LMC"] != metrics["TMC"]

    def isDataClass(self, metrics):
        return (metrics["WMC"] <= HIGH_WMC and metrics["NOPA"] >= HIGH_NOPA) or \
               (metrics["WMC"] <= VERY_HIGH_WMC and metrics["NOPA"] >= VERY_HIGH_NOPA)

    def isFeatureEnvy(self, metrics):
        return metrics["LCOM"] > HIGH_LCOM

    def isBrainClass(self, metrics):
        return not self.isGodClass(metrics) and \
               metrics["WMC"] >= 47 and \
               metrics["TCC"] < 0.5 and \
               ((metrics["numberOfBrainMethod"] > 1 and metrics["LOC"] >= 197) or
                (metrics["numberOfBrainMethod"] == 1 and metrics["LOC"] >= 2*197 and metrics["WMC"] >= 2*47))
