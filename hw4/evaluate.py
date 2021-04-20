import os
import sys

def main():
    dataFile = open(sys.argv[1], "r")
    f = open("result.txt", "w")
    f.close()

    importantData = []
    
    line = dataFile.readline()
    while "@attribute" not in line:
        line = dataFile.readline()

    while "@attribute" in line:
        importantData.append(line)
        line = dataFile.readline()
    importantData.append("\n")

    line = dataFile.readline()
    while "@data" not in line:
        line = dataFile.readline()

    importantData.append(line)

    line = dataFile.readline()
    while "%" in line:
        line = dataFile.readline()

    dataInputs = []
    while line != "":
        line = line.strip("\n")
        dataInputs.append(line)
        line = dataFile.readline()
    

    for i in range(len(dataInputs)):
        test = open("test.txt", "w")
        train = open("training.txt", "w")

        for item in importantData:
            test.write(item)
            train.write(item)

        test.write(dataInputs[i])
        before = dataInputs[:i]
        after = dataInputs[i + 1:]

        for item in before:
            train.write(item + "\n")
        for item in after:
            train.write(item + "\n")
        test.close()
        train.close()
        os.system("python naiveBayes.py training.txt test.txt result.txt")
    
    trueClass = {}
    for i in range(len(dataInputs)):
        dataInputs[i] = dataInputs[i].split(",")
        dataInputs[i] = dataInputs[i][::-1]
        dataInputs[i] = dataInputs[i][0]

        if dataInputs[i] not in trueClass:
            trueClass[dataInputs[i]] = 1
        else:
            trueClass[dataInputs[i]] += 1

    classifiedArray = []
    f = open("result.txt", "r")
    for line in f:
        line = line.split(":")
        line = line[1].split("[")
        classifiedArray.append(line[0].strip())
    
    confusionMatrix = [[0 for i in range(len(trueClass) + 1) ] for j in range(len(trueClass) + 1)]
    
    confusionMatrix[0][0] = "   "
    confusionAcc = 1
    confusionOrder = []
    for contact in trueClass:
        confusionMatrix[0][confusionAcc], confusionMatrix[confusionAcc][0] = contact, contact
        confusionOrder.append(contact)
        confusionAcc += 1

    for i in range(len(dataInputs)):
        xCoord = confusionOrder.index(dataInputs[i]) + 1
        yCoord = confusionOrder.index(classifiedArray[i]) + 1
        currVal = int(confusionMatrix[xCoord][yCoord])
        currVal += 1
        confusionMatrix[xCoord][yCoord] = currVal

    correctPredictions = 0
    for i in range(1, len(confusionMatrix)):
        correctPredictions += int(confusionMatrix[i][i])

    f = open("result.txt", "a")
    f.write("\n")
    for i in range(len(confusionMatrix)):
        for j in range(len(confusionMatrix[i])):
            if i == 0 or j == 0:
                f.write("  " + str(confusionMatrix[i][j]))
            else:
                f.write("   " + str(confusionMatrix[i][j]))

        f.write("\n")

    f.write("\n")
    f.write("Classification Accuracy: " + str(correctPredictions) + " / " + str(len(classifiedArray)) + " = " + str(correctPredictions/len(classifiedArray)))
main()