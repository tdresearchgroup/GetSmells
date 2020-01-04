import sys
import platform
import statistics
import os
import numpy as np

if platform.system() == "Windows":
    sys.path.append('C:/Program Files/SciTools/bin/pc-win64/Python')
else:
    sys.path.append('/Applications/Understand.app/Contents/MacOS/Python')

# Relevant Understand API Documentation:
# https://scitools.com/sup/api-2/
# https://scitools.com/documents/manuals/python/understand.html
# help(understand)
import understand


# -------------------------
#       METRICS
# -------------------------

# ATFD (Access to Foreign Data)
# Class-Level Metric
def getATFD(classObj):
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
# Class-Level Metric
# = SumCyclomaticModified
def getWMC(classObj):
    return classObj.metric(["SumCyclomaticModified"])['SumCyclomaticModified'] or 0

#LMC (Local Method Count)
#Class-Level Metric
def getLMC(classObj):
    return classObj.metric(["CountDeclMethod"])['CountDeclMethod'] or 0

#TMC (Total Method Count)
#Class-Level Metric
#Includes all inherited methods as well as local
def getTMC(classObj):
    return classObj.metric(["CountDeclMethodAll"])['CountDeclMethodAll'] or 0

#Inputs
#Method-Level Metric
#Includes parameters and global variables read
def getInputs(methodObj):
    return methodObj.metric(["CountInput"])['CountInput'] or 0

# TCC (Tight Class Cohesion)
# Class-Level Metric
def getTCC(classObj):
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

def getCM(methodObj):
    return len(methodObj.refs("Callby", "Method", True))

def getCC(methodObj):
    return len({x.ent().ref("Definein", "Class").ent() for x in methodObj.refs("Callby", "Method", True)})

# LOC (Lines of Code)
# Class- or method-level metric
def getLOC(classOrMethodObj):
    return classOrMethodObj.metric(["CountLineCode"])['CountLineCode'] or 0

# CMC (Complex Method Count)
# Returns number of methods in class with complexity greater than the threshold
# Original, custom metric (used to determine Complex Class smell)
# Class-level metric
def getCMC(classObj, complexityThreshold):
    count = 0
    for amethod in classObj.ents("Define", "Method"):
        if getCyclomatic(amethod) > complexityThreshold:
            count += 1
    return count

# Cyclomatic Complexity
# Class- or metric-level metric
def getCyclomatic(methodObj):
    return methodObj.metric(["Cyclomatic"])['Cyclomatic'] or 0

# Number of Public Methods
# Class level metric
def getNOPA(classObj):
    return classObj.metric(["CountDeclMethodPublic"])['CountDeclMethodPublic'] or 0

# Lack of Cohesion of Methods
# Method Level metric
def getLCOM(classObj):
    return classObj.metric(["PercentLackOfCohesion"])['PercentLackOfCohesion'] or 0

# -------------------------
#       SMELLS
# -------------------------

def extractSmells(projectPath, outputPath, runName, log, includeMetricsInCsv = True):
    delm = ","
    #includeMetricsInCsv = True

    FEW = 4
    ONE_THIRD = 1/3
    HIGH_METHOD_COMPLEXITY = 10
    HIGH_LCOM = 73 #0.725

    #for use with PMD style data class methodology
    HIGH_NOPA = 5
    VERY_HIGH_NOPA = 3
    HIGH_WMC = 30
    VERY_HIGH_WMC = 45

    classStatusUpdateInterval = 200
    methodStatusUpdateInterval = 5000

    outputCsvFileClasses = os.path.join(outputPath, runName + "-smells-classes.csv")
    outputCsvFileMethods = os.path.join(outputPath, runName + "-smells-methods.csv")
    outputTxtDirClasses = os.path.join(outputPath, runName + "-smelly-classes")
    outputTxtDirMethods = os.path.join(outputPath, runName + "-smelly-methods")
    if not os.path.exists(outputTxtDirClasses):
        os.makedirs(outputTxtDirClasses)
    if not os.path.exists(outputTxtDirMethods):
        os.makedirs(outputTxtDirMethods)

    db = understand.open(projectPath)

    totalClassesCount = len(db.ents("Class"))
    totalMethodsCount = len(db.ents("Method"))

    print("\tCalculating complex metrics for "+str(totalClassesCount) + " classes...")

    classLib = list()
    methodLib = list()

    allClassLOC = list()
    allClassWMC = list()
    allMethodLOC = list()
    allMethodPLL = list()
    allMethodInputs = list()

    for aclass in db.ents("Class"):
        if (len(classLib)+1) % classStatusUpdateInterval == 0:
            print("\t\t" + str(round((len(classLib)/totalClassesCount)*100)) + "% complete" )

        classLongName = aclass.longname()

        classMetricATFD = getATFD(aclass)
        classMetricWMC = getWMC(aclass)
        classMetricTCC = getTCC(aclass)
        classMetricLOC = getLOC(aclass)
        classMetricCMC = getCMC(aclass, HIGH_METHOD_COMPLEXITY)

        classMetricTMC = getTMC(aclass)
        classMetricLMC = getLMC(aclass)
        classMetricNOPA = getNOPA(aclass)
        classMetricLCOM = getLCOM(aclass)

        allClassWMC.append(classMetricWMC)
        allClassLOC.append(classMetricLOC)

        classLib.append({"name": classLongName, "ATFD": classMetricATFD, "WMC": classMetricWMC, "TCC": classMetricTCC,
            "LOC": classMetricLOC, "CMC": classMetricCMC, "TMC": classMetricTMC, "LMC": classMetricLMC, "NOPA": classMetricNOPA, "LCOM": classMetricLCOM})

    print("\tCalculating complex metrics for "+str(totalMethodsCount) + " methods...")

    for amethod in db.ents("Method ~unresolved ~unknown"):
        if (len(methodLib)+1) % methodStatusUpdateInterval == 0:
            print("\t\t" + str(round((len(methodLib)/totalMethodsCount)*100)) + "%% complete" )

        methodLongName = amethod.name()

        methodMetricLOC = getLOC(amethod)
        allMethodLOC.append(methodMetricLOC)

        methodMetricInputs = getInputs(amethod)
        allMethodInputs.append(methodMetricInputs)

        methodMetricCM = getCM(amethod)
        methodMetricCC = getCC(amethod)

        methodLib.append({"name": methodLongName,
                          "LOC": methodMetricLOC,
                          "inputs": methodMetricInputs,
                          "CM": methodMetricCM,
                          "CC": methodMetricCC})

    print("\tCalculating system-wide averages and metrics")

    meanClassWMC = statistics.mean(allClassWMC)
    devClassWMC = statistics.pstdev(allClassWMC)
    veryHighClassWMC = meanClassWMC + (1.5 * devClassWMC) # 1.5 std. dev. above the mean (upper ~15%)
    # TODO(performance improvement): Improve such that 1st quartile LOC can be cacluated without storing all
    # observations (see http://www.cs.wustl.edu/~jain/papers/ftp/psqr.pdf) for "Lazy Class"
    firstQuartileClassLOC = np.percentile(allClassLOC, 25) # Get the 1st quartitle
    meanClassLOC = statistics.mean(allClassLOC)
    meanMethodLoc = statistics.mean(allMethodLOC)
    meanMethodInputs = statistics.mean(allMethodInputs)

    log.write("Class WMC: mean = " + str(meanClassWMC) + ", pstdev = " + str(devClassWMC) + ", VERY_HIGH = " + str(veryHighClassWMC) + "\n")
    log.write("Class LOC: 1st Quartile = " + str(firstQuartileClassLOC) + "\n")
    log.write("Class LOC: mean = " + str(meanClassLOC) + "\n")
    log.write("Method LOC: mean = " + str(meanMethodLoc) + "\n")
    log.write("Method Inputs: mean = " + str(meanMethodInputs) + "\n")
    log.write("M")

    print("\tApplying code smell thresholds")

    # Apply Class-Level Smells
    classSmells = {'god': set(), 'lazy': set(), 'complex': set(), 'refusedBequest': set(), 'long': set(), 'dataClass': set(), 'featureEnvy': set()}

    outputFile = open(outputCsvFileClasses, "w")
    outputData = delm.join(["Class", "God Class", "Lazy Class", "Complex Class", "Long Class", "Refused Bequest", "Data Class", "Feature Envy"])
    if includeMetricsInCsv:
            outputData += delm + delm.join(["Metric: ATFD", "Metric: WMC", "Metric: TCC", "Metric: LOC", "Metric: CMC", "Metric: TMC", "Metric: LMC", "Metric: NOPA", "Metric: LCOM (%)"])
    outputFile.write(outputData + "\n")

    for aclass in classLib:
        # God Class
        # - ATFD (Access to Foreign Data) > Few
        # - WMC (Weighted Method Count) >= Very High
        # - TCC (Tight Class Cohesion) < 1/3
        classSmellGod = (aclass["ATFD"] > FEW) and (aclass["WMC"] >= veryHighClassWMC) and (aclass["TCC"] < ONE_THIRD)

        # Lazy Class
        # - LOC (Lines of Code) < 1st quartile of system
        classSmellLazy = (aclass["LOC"] < firstQuartileClassLOC)

        # Complex Class
        # - CMC (Complex Method Count; number of methods with complexity > HIGH_METHOD_COMPLEXITY) >= 1
        classSmellComplex = (aclass["CMC"] >= 1)

        classSmellLong = (aclass["LOC"] > meanClassLOC)

        classSmellRefusedBequest = (aclass["LMC"] > (.5 * aclass["TMC"])) and (aclass["LMC"] != aclass["TMC"])

        classSmellDataClass = ( (aclass["WMC"] <= HIGH_WMC and aclass["NOPA"] >= HIGH_NOPA) or (aclass["WMC"] <= VERY_HIGH_WMC and aclass["NOPA"] >= VERY_HIGH_NOPA) )

        classSmellFeatureEnvy = (aclass["LCOM"] > HIGH_LCOM)

        if classSmellGod:
            classSmells['god'].add(aclass["name"])
        if classSmellLazy:
            classSmells['lazy'].add(aclass["name"])
        if classSmellComplex:
            classSmells['complex'].add(aclass["name"])
        if classSmellLong:
            classSmells['long'].add(aclass["name"])
        if classSmellRefusedBequest:
            classSmells['refusedBequest'].add(aclass["name"])
        if classSmellDataClass:
            classSmells['dataClass'].add(aclass["name"])
        if classSmellFeatureEnvy:
            classSmells['featureEnvy'].add(aclass["name"])

        csvLine = delm.join([aclass["name"], str(classSmellGod), str(classSmellLazy), str(classSmellComplex), str(classSmellLong), str(classSmellRefusedBequest), str(classSmellDataClass), str(classSmellFeatureEnvy)])
        if includeMetricsInCsv:
            csvLine += delm + delm.join([str(aclass["ATFD"]), str(aclass["WMC"]), str(aclass["TCC"]), str(aclass["LOC"]), str(aclass["CMC"]), str(aclass["LMC"]), str(aclass["TMC"]), str(aclass["NOPA"]), str(aclass["LCOM"])])
        outputFile.write(csvLine + "\n")

    outputFile.close()

    # Apply Method-Level Smells
    methodSmells = {'long': set(), 'lpl': set(), 'shotgunSurgery': set()}

    outputFile = open(outputCsvFileMethods, "w")
    outputData = delm.join(["Method", "Long Method", "Long Parameter List"])
    if includeMetricsInCsv:
            outputData += delm + delm.join(["Metric: LOC", "Metric: inputs"])
    outputFile.write(outputData + "\n")

    for amethod in methodLib:
        # Long Method
        # - LOC (Lines of Code) > mean of system
        # methodSmellLong = (amethod["LOC"] > meanMethodLoc)

        # - LOC (Lines of Code) > 20 - Zadia
        methodSmellLong = (amethod["LOC"] > 20)

        methodSmellLongParameterList = (amethod["inputs"] > meanMethodInputs)

        # Shotgun Surgery
        # - CM (Changing Methods) > 10
        # - CC (Changing Classes) > 5
        methodSmellShotGunSurgery = (amethod["CM"] > 10 and amethod["CC"] > 5)

        if methodSmellLong:
            methodSmells['long'].add(amethod["name"])
        if methodSmellLongParameterList:
            methodSmells['lpl'].add(amethod["name"])
        if methodSmellShotGunSurgery:
            methodSmells['shotgunSurgery'].add(amethod["name"])

        csvLine = delm.join([amethod["name"], str(methodSmellLong), str(methodSmellLongParameterList)])
        if includeMetricsInCsv:
            csvLine += delm + delm.join([str(amethod["LOC"]), str(amethod["inputs"])])
        outputFile.write(csvLine + "\n")

    outputFile.close()

    print("\tWriting list of smelly classes/methods")

    summaryData = "\tCode smell extraction complete"
    summaryData = "\tNumber of Class-Level Smells:"
    for smellName, classes in classSmells.items():
        outputFileName = os.path.join(outputTxtDirClasses, smellName + ".txt")
        outputFile = open(outputFileName, "w")
        for className in classes:
            outputFile.write(className + "\n")
        outputFile.close()
        summaryData += "\n\t\t" + smellName +"  = " + str(len(classes))
    summaryData += "\n\tNumber of Method-Level Smells:"
    for smellName, methods in methodSmells.items():
        outputFileName = os.path.join(outputTxtDirMethods, smellName + ".txt")
        outputFile = open(outputFileName, "w")
        for methodName in methods:
            outputFile.write(methodName + "\n")
        outputFile.close()
        summaryData += "\n\t\t" + smellName +" = " + str(len(methods))

    log.write("\n" + summaryData)
    print(summaryData + "\n")


if __name__ == '__main__':
    print("Running code smell extraction on an Understand project standalone using defaults")

    # Default project and output path
    if platform.system() == "Windows":
        logFile = open("C:/Users/cb1782/getsmells-test-output/understandapi-log.txt", "w+")
        extractSmells("C:/Users/cb1782/MyUnderstandProject.udb",
                      "C:/Users/cb1782/getsmells-test-output/",
                      "default",
                      logFile)
        logFile.close()
    else:
        logFile = open("/Users/charles/Documents/DIS/getsmells-test-output/understandapi-log.txt", "w+")
        extractSmells("/Users/charles/Documents/DIS/understandproject.udb",
                    "/Users/charles/Documents/DIS/getsmells-test-output/",
                    "default",
                    logFile)
        logFile.close()
