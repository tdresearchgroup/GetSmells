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
        # Long Method
        # methodSmellLong = (amethod["LOC"] > meanMethodLoc)
        # - LOC (Lines of Code) > 20 - Zadia
        return metrics["LOC"] > 20

    def isLongParameterList(self, metrics):
        dataListInputs = self.getMetricDistribution("inputs")
        mean = getMean(dataListInputs)
        return metrics["inputs"] > mean

    def isShotgunSurgery(self, metrics):
        # Shotgun Surgery
        # - CM (Changing Methods) > 10
        # - CC (Changing Classes) > 5
        return metrics["CM"] > 10 and metrics["CC"] > 5

    def isBrainMethod(self, metrics):
        # Brain Method
        # - LOC (Line of Code) > 65
        # - CYCLO(Cyclomatic Complexity) / LOC(Line of Code) >= 0.24
        # - MAXNESTING(Maximum Nesting Level) >= 5
        # - NOAV(Number of Accessed Variables) > 8
        return metrics["LOC"] > 65 and \
               metrics["CYCLO"]/metrics["LOC"] >= 0.24 and \
               metrics["MAXNESTING"] >= 5 and \
               metrics["NOAV"] > 8
