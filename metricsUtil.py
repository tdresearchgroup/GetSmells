class MetricsUtil:

    # LOC (Lines of Code)
    # Class- or method-level metric
    def _getLOC(self, classOrMethodObj):
        return classOrMethodObj.metric(["CountLineCode"])['CountLineCode'] or 0

    # Cyclomatic Complexity
    # Class- or metric-level metric
    def _getCyclomatic(self, methodObj):
        return methodObj.metric(["Cyclomatic"])['Cyclomatic'] or 0