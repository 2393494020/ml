from numpy import *
import operator

def createDataSet():
    group = array([[1.0, 1.1],[1.0, 1.0],[0, 0],[0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()

    # print(distances)
    # print(sortedDistIndicies)

    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    
    # print(classCount)

    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    returnMat = zeros((numberOfLines, 3))
    classLaberVector = []
    fr = open(filename)
    index = 0

    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLaberVector.append(int(listFromLine[-1]))
        index += 1
    
    return returnMat, classLaberVector

def autoNorm(dataSet):
    # 提取每一列的最小、最大值
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals

    # normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))

    return normDataSet, ranges, minVals

def dataingClassTest():
    hoRatio = 0.10
    matrixData, labels = file2matrix('../datingTestSet2.txt')

    normDataSet, ranges, minVals = autoNorm(matrixData)
    m = normDataSet.shape[0]
    numTestVecs = int( m * hoRatio )
    errorCount = 0.0
    for i in range( numTestVecs ):
        predict = classify0( normDataSet[i, :], normDataSet[numTestVecs:m, :], labels[numTestVecs:], 3 )
        if (predict != labels[i: i + 1][0]):
            errorCount += 1

    print(errorCount)
    print(numTestVecs)
    print(len(normDataSet))
    print(errorCount / numTestVecs)

import matplotlib
import matplotlib.pyplot as plt

def show(data, labels):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(data[:, 0], data[:, 1], 15.0*array(labels), 15.0*array(labels))
    plt.show()

if __name__ == "__main__":
    # group, labels = createDataSet()
    # print( classify0([1.1, 1.1], group, labels, 3) )

    # matrixData, labels = file2matrix('../datingTestSet2.txt')    
    # normMat, ranges, minVals = autoNorm(matrixData)
    # frequent flyier miles earned per year|percentage of time spent playing video games|liters of ice cream consumed per week
    # 1 did not like
    # liked in small doses
    # liked in large doses
    # show(normMat, labels)

    dataingClassTest()