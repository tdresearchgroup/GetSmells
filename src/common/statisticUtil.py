import numpy as np


def getMean(dataList):
    return np.mean(dataList)


def getStdev(dataList):
    return np.std(dataList)


def getMedian(dataList):
    return np.median(dataList)


def getQuartile(dataList, quartile):
    return np.percentile(dataList, 25 * quartile)


def getCumulativeZ(dataList, z):
    # TODO 1.5 std. dev. above the mean (upper ~15%) wrong!!!
    mean = getMean(dataList)
    std = getStdev(dataList)
    return mean + z * std


def printProgress(count, total):
    statusUpdateInterval = round(total/10)
    if count % statusUpdateInterval == 0:
        print(f"\t\t{str(round(count/total*100))}% complete")
