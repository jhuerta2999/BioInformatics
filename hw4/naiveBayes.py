import sys

def createDictioanry(dataSet):
    f = open(dataSet, "r")
    line = f.readline()
    while "@attribute" not in line:
        line = f.readline()

    attributeList = []
    while "@attribute" in line:
        acc = 0
        for i in range (len(line) - 1):
            if line[i] == "{":
                line = line[i:]
                break

        line = line[1:len(line) - 2]
        line = line.split(",")

        for i in range (len(line)):
            line[i] = line[i].strip()

        attributeList.append(line)
        line = f.readline()

    while "@data" not in line:
        line = f.readline()

    line = f.readline()

    contactType = {}
    currType = ""
    numTrain = 0
    while line != "":
        line = line.strip("\n")
        line = line.split(",")
        line = line[::-1]

        for i in range(len(line)):
            if i == 0:
                if line[i] not in contactType:
                    contactType[line[i]] = {}
                currType = line[i]
            if line[i] not in contactType[currType].keys():
                contactType[currType][line[i]] = 1
            else:
                contactType[currType][line[i]] = contactType[currType][line[i]] + 1

        line = f.readline()
        numTrain += 1
    return attributeList, contactType, numTrain

def calculateProb(testSet, attributeList, contactType, trainSize, outFile):
    f = open(testSet, "r")
    out = open(outFile, "a")
    line = f.readline()

    while "@data" not in line:
        line = f.readline()

    line = f.readline()

    attributeList = attributeList[::-1]

    while line != "":
        line = line.strip("\n")
        line = line.split(",")
        line = line[::-1]

        probArray = [1] * len(attributeList[0])
        totalArray = [0] * len(attributeList[0])
        pseudoProb = 1
        for i in range(len(line)):
            for j in range(len(attributeList[0])):
                currType = attributeList[0][j]
                if i == 0:
                    probArray[j] = (contactType[currType][currType] / trainSize)
                    totalArray[j] = probArray[j]
                elif line[i] in contactType[currType]:
                    probArray[j] *= (contactType[currType][line[i]] / contactType[currType][currType])
                    totalArray[j] += probArray[j]
                else:
                    probArray[j] = 0

        classified = 0
        pos = 0
        probSum = sum(probArray)
        for i in range(len(probArray)):
            probArray[i] /= probSum
            if probArray[i] > classified:
                classified = probArray[i]
                pos = i
            probArray[i] = attributeList[0][i] + " probability: " + str(probArray[i])
        out.write("Classified as: " + str(attributeList[0][pos]) + " " + str(probArray) + "\n")

        line = f.readline()

def main():
    trainingSet = createDictioanry(sys.argv[1])
    testSet = calculateProb(sys.argv[2], trainingSet[0], trainingSet[1], trainingSet[2], sys.argv[3])
main()
