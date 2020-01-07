from statisticUtil import getQuartile, getMean, getCumulativeZ
GOD_CLASS_AFTD_FEW = 4
ONE_THIRD = 1/3
HIGH_LCOM = 73 #0.725

#for use with PMD style data class methodology
HIGH_NOPA = 5
VERY_HIGH_NOPA = 3
HIGH_WMC = 30
VERY_HIGH_WMC = 45


class ClassLevelSmellExtractor:
    def __init__(self, metrics):
        self.metrics = metrics

    def getSmells(self):
        classSmells = {'god': set(),
                       'lazy': set(),
                       'complex': set(),
                       'long': set(),
                       'refusedBequest': set(),
                       'dataClass': set(),
                       'featureEnvy': set(),
                       'brainClass': set()}

        for longName, metrics in self.metrics.items():
            if self.isGodClass(metrics):
                classSmells['god'].add(longName)
            if self.isLazyClass(metrics):
                classSmells['lazy'].add(longName)
            if self.isComplexClass(metrics):
                classSmells['complex'].add(longName)
            if self.isLongClass(metrics):
                classSmells['long'].add(longName)
            if self.isRefusedBequest(metrics):
                classSmells['refusedBequest'].add(longName)
            if self.isDataClass(metrics):
                classSmells['dataClass'].add(longName)
            if self.isFeatureEnvy(metrics):
                classSmells['featureEnvy'].add(longName)
            if self.isBrainClass(metrics):
                classSmells['brainClass'].add(longName)

    def getMetricDistribution(self, metrics, metricName):
        return [x[metricName] for x in metrics.values()]

    def isGodClass(self, metrics):
        dataListWMC = self.getMetricDistribution(metrics, "WMC")
        veryHigh = getCumulativeZ(dataListWMC, 1.5)

        return metrics["ATFD"] > GOD_CLASS_AFTD_FEW and \
               metrics["WMC"] >= veryHigh and \
               metrics["TCC"] < ONE_THIRD

    def isLazyClass(self, metrics):
        # Lazy Class
        # - LOC (Lines of Code) < 1st quartile of system
        dataListLOC = self.getMetricDistribution(metrics, "LOC")
        firstQuatileLOC = getQuartile(dataListLOC, 1)
        return metrics["LOC"] < firstQuatileLOC

    def isComplexClass(self, metrics):
        # - CMC (Complex Method Count; number of methods with complexity > HIGH_METHOD_COMPLEXITY) >= 1
        return metrics["CMC"] >= 1

    def isLongClass(self, metrics):
        dataListLOC = self.getMetricDistribution(metrics, "LOC")
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
