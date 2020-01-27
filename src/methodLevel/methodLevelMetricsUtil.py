from src.common import MetricsUtil, printProgress

METHOD_STATUS_UPDATE_INTERVAL = 200


class MethodLevelMetricsUtil(MetricsUtil):

    def __init__(self, methodEnts):
        self.methodEnts = methodEnts

    def generateMetrics(self):
        methodLib = {}
        totalMethodsCount = len(self.methodEnts)
        print("\tCalculating complex metrics for", totalMethodsCount, "methods...")

        for methodEnt in self.methodEnts:
            methodLongName = f"{methodEnt.longname()}@{methodEnt.id()}"

            methodLib[methodLongName] = ({"LOC": self._getLOC(methodEnt),
                                          "inputs": self.__getInputs(methodEnt),
                                          "CM": self.__getCM(methodEnt),
                                          "CC": self.__getCC(methodEnt),
                                          "NOAV": self.__getNOAV(methodEnt),
                                          "CYCLO": self._getCyclomatic(methodEnt),
                                          "MAXNESTING": self.__getMAXNESTING(methodEnt)})
            printProgress(len(methodLib), totalMethodsCount)
        return methodLib

    def __getInputs(self, methodObj):
        return methodObj.metric(["CountInput"])['CountInput'] or 0

    def __getNOAV(self, methodObj):
        lenOfParameters = len(methodObj.ents("Define", "Parameter"))
        lenOfVariables = len(methodObj.ents("Use, Set", "Variable ~unresolved ~unknown"))
        return lenOfParameters + lenOfVariables

    def __getCM(self, methodObj):
        return len(methodObj.refs("Callby", "Method", True))

    def __getCC(self, methodObj):
        return len({x.ent().ref("Definein", "Class").ent() for x in methodObj.refs("Callby", "Method", True)})

    def __getMAXNESTING(self, methodObj):
        return methodObj.metric(["MaxNesting"])["MaxNesting"] or 0

    def __getNINTERF(self, classObj):
        return len(classObj.refs("Implement", "Interface", True))
