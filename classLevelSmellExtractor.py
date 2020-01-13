from statisticUtil import getQuartile, getMean, getCumulativeZ
from classLevelMetricsUtil import ClassLevelMetricsUtil
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
        self.__classMetrics = ClassLevelMetricsUtil(classEnts).generateMetrics()

    def getSmells(self):
        classSmells = {}
        for longName, metrics in self.__classMetrics.items():
            classSmells[longName] = {"God_Class": self.isGodClass(metrics),
                                     "Lazy_Class": self.isLazyClass(metrics),
                                     "Complex_Class": self.isComplexClass(metrics),
                                     "Long_Class": self.isLongClass(metrics),
                                     "Refused_Request": self.isRefusedBequest(metrics),
                                     "Data_Class": self.isDataClass(metrics),
                                     "Feature_Envy": self.isFeatureEnvy(metrics),
                                     "Brain_Class": self.isBrainClass(metrics)}

        return classSmells

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
