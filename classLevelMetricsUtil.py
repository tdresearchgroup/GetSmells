from metricsUtil import MetricsUtil

CLASS_STATUS_UPDATE_INTERVAL = 200
HIGH_METHOD_COMPLEXITY = 10


class ClassLevelMetricsUtil(MetricsUtil):

    def __init__(self, classEnts):
        self.classEnts = classEnts

    def generateMetrics(self):
        classLib = {}
        totalClassesCount = len(self.classEnts)
        print("\tCalculating complex metrics for", totalClassesCount, "classes...")

        for classEnt in self.classEnts:
            if (len(classLib)+1) % CLASS_STATUS_UPDATE_INTERVAL == 0:
                print("\t\t" + str(round((len(classLib)/totalClassesCount)*100)) + "% complete")

            classLongName = classEnt.longname()

            classLib[classLongName] = {"numberOfBrainMethod": 0,
                                       "ATFD": self.__getATFD(classEnt),
                                       "WMC": self.__getWMC(classEnt),
                                       "TCC": self.__getTCC(classEnt),
                                       "LOC": self._getLOC(classEnt),
                                       "CMC": self.__getCMC(classEnt, HIGH_METHOD_COMPLEXITY),
                                       "TMC": self.__getTMC(classEnt),
                                       "LMC": self.__getLMC(classEnt),
                                       "NOPA": self.__getNOPA(classEnt),
                                       "LCOM": self.__getLCOM(classEnt),
                                       "Hub_In": self.__getHubIngoing(classEnt),
                                       "Hub_Out": self.__getHubOutgoing(classEnt)}
        return classLib

    def __getHubIngoing(self, classEnt):
        return len({x for x in classEnt.dependsby().keys()})

    def __getHubOutgoing(self, classEnt):
        return len({x for x in classEnt.depends().keys()})

    # ATFD (Access to Foreign Data)
    # Class-Level Metric
    def __getATFD(self, classObj):
        classATFD = 0
        for amethod in classObj.ents("Define", "Method"):
            # https://scitools.com/documents/manuals/html/understand_api/kindApp121.html
            # https://scitools.com/documents/manuals/html/understand_api/kindApp158.html
            # NOTE: Includes all foreign methods called, even if not a getter or setter
            for aent in amethod.ents("Call, Use, Set", "Method ~unresolved ~unknown, Variable ~unresolved ~unknown"):
                if classObj.longname() not in aent.longname():
                    classATFD += 1
        return classATFD


    # WMC (Weighted Method Count)
    # = SumCyclomaticModified
    def __getWMC(self, classObj):
        return classObj.metric(["SumCyclomaticModified"])['SumCyclomaticModified'] or 0

    #LMC (Local Method Count)
    def __getLMC(self, classObj):
        return classObj.metric(["CountDeclMethod"])['CountDeclMethod'] or 0

    #TMC (Total Method Count)
    #Class-Level Metric
    #Includes all inherited methods as well as local
    def __getTMC(self, classObj):
        return classObj.metric(["CountDeclMethodAll"])['CountDeclMethodAll'] or 0

    # TCC (Tight Class Cohesion)
    # Class-Level Metric
    def __getTCC(self, classObj):
        methods = classObj.ents("Define", "Method")
        numberOfPairs = 0
        numberOfShares = 0
        for x in range(0, len(methods)):
            for y in range(x + 1, len(methods)):
                numberOfPairs += 1
                atrrsAccessedInMethodX = methods[x].ents("Use, Set", "Variable ~unresolved ~unknown")
                atrrsAccessedInMethodY = methods[y].ents("Use, Set", "Variable ~unresolved ~unknown")
                atrrsAccessedInMethodXNames = set()
                atrrsAccessedInMethodYNames = set()
                for attr in atrrsAccessedInMethodX:
                    atrrsAccessedInMethodXNames.add(attr.longname())
                for attr in atrrsAccessedInMethodY:
                    atrrsAccessedInMethodYNames.add(attr.longname())
                commonAttrs = atrrsAccessedInMethodXNames.intersection(atrrsAccessedInMethodYNames)
                for atrrName in commonAttrs:
                    if classObj.longname() in atrrName:
                        numberOfShares += 1
                        break
        if numberOfPairs == 0:
            # NOTE: Default is currently 0.0
            return 0.0
        else:
            return (numberOfShares / numberOfPairs) * 1.0

    # CMC (Complex Method Count)
    # Returns number of methods in class with complexity greater than the threshold
    # Original, custom metric (used to determine Complex Class smell)
    # Class-level metric
    def __getCMC(self, classObj, complexityThreshold):
        count = 0
        for amethod in classObj.ents("Define", "Method"):
            if self._getCyclomatic(amethod) > complexityThreshold:
                count += 1
        return count

    # Number of Public Methods
    # Class level metric
    def __getNOPA(self, classObj):
        return classObj.metric(["CountDeclMethodPublic"])['CountDeclMethodPublic'] or 0

    # Lack of Cohesion of Methods
    # Method Level metric
    def __getLCOM(self, classObj):
        return classObj.metric(["PercentLackOfCohesion"])['PercentLackOfCohesion'] or 0