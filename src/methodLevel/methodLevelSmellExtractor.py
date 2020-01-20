from src.common.statisticUtil import getMean
from src.methodLevel.methodLevelMetricsUtil import MethodLevelMetricsUtil


class MethodLevelSmellExtractor:

    def __init__(self, methodEnts):
        self.__methodMetrics = MethodLevelMetricsUtil(methodEnts).generateMetrics()

    def getSmells(self):
        methodSmells = {}
        for longName, metrics in self.__methodMetrics.items():
            methodSmells[longName] = {"Long_Method": self.isLongMethod(metrics),
                                      "Long_Parameter_List": self.isLongParameterList(metrics),
                                      "Shotgun_Surgery": self.isShotgunSurgery(metrics),
                                      "Brain_Method": self.isBrainMethod(metrics)}
        return methodSmells

    def getMethodMetrics(self):
        return self.__methodMetrics

    def getMetricDistribution(self, metricName):
        return [x[metricName] for x in self.__methodMetrics.values()]

    def isLongMethod(self, metrics):
        return metrics["LOC"] > 20

    def isLongParameterList(self, metrics):
        dataListInputs = self.getMetricDistribution("inputs")
        mean = getMean(dataListInputs)
        return metrics["inputs"] > mean

    def isShotgunSurgery(self, metrics):
        return metrics["CM"] > 10 and metrics["CC"] > 5

    def isBrainMethod(self, metrics):
        return metrics["LOC"] > 65 and \
               metrics["CYCLO"]/metrics["LOC"] >= 0.24 and \
               metrics["MAXNESTING"] >= 5 and \
               metrics["NOAV"] > 8
