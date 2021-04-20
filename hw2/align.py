import sys 

def alignSequences(first, second, scoringMatrix, penaltyScore, semiOrGlobal):
    #Read first sequence
    f = open(first, "r")
    f.readline()
    firstSequence = ""
    for line in f:
        line = line.strip()
        line = line.strip("\n")
        firstSequence += line

    #Read second sequence
    f = open(second, "r")
    f.readline()
    secondSequence = ""
    for line in f:
        line = line.strip()
        line = line.strip("\n")
        secondSequence += line

    xAxis, yAxis = "", ""

    #Make longer sequence the x axis
    if len(firstSequence) > len(secondSequence):
        xAxis = firstSequence
        yAxis = secondSequence
    else:
        xAxis = secondSequence
        yAxis = firstSequence 

    cols = len(xAxis) + 1
    rows = len(yAxis) + 1

    matrix = [[0 for i in range(cols) ] for j in range(rows)]
    pathDictionary = {}
    
    sequence = ""
    for item in scoringMatrix[0]:
        sequence += item

    #used to offset the string length and matrix length
    colAcc = -1
    rowAcc = -1

    #Match all letters of shorter sequence to longer sequence
    for i in range (rows):
        yCoord = sequence.find(yAxis[rowAcc])

        for j in range (cols):
            if i == 0:
                if j != 0:
                    pathDictionary[str(0) + "," + str(j)] = str(0) + "," + str(j - 1)

                #If global apply gap penalty
                if semiOrGlobal == "g":
                    matrix[0][j] = int(penaltyScore) * j
            else:
                if j == 0:
                    pathDictionary[str(i) + "," + str(j)] = str(i - 1) + "," + str(j)

                    #If global apply gap penalty
                    if semiOrGlobal == "g":
                        matrix[i][j] = int(penaltyScore) * i
                else:
                    match, gapPenalty1, gapPenalty2 = 0, 0, 0
                    xCoord = sequence.find(xAxis[colAcc])

                    #Compare letter of sequence 1 and 2
                    if xAxis[colAcc] == yAxis[rowAcc]:
                        match = matrix[i - 1][j - 1] + int(scoringMatrix[xCoord + 1][yCoord + 1])
                    else:
                        match = matrix[i - 1][j - 1] + int(scoringMatrix[xCoord + 1][yCoord + 1])

                    gapPenalty1 = matrix[i - 1][j] + int(penaltyScore) 
                    if semiOrGlobal == "s" and i == rows - 1:
                        gapPenalty1 = matrix[i - 1][j]

                    gapPenalty2 = matrix[i][j - 1] + int(penaltyScore) 
                    if semiOrGlobal == "s" and j == cols - 1:
                        gapPenalty2 = matrix[i][j - 1]

                    #If doing local make values 0 if less than 0
                    if semiOrGlobal == "l":
                        if match < 0:
                            match = 0
                        if gapPenalty1 < 0:
                            gapPenalty1 = 0
                        if gapPenalty2 < 0:
                            gapPenalty2 = 0

                    #Choose highest value to assign to matrix and add to dictioanry
                    if match >= gapPenalty1 and match >= gapPenalty2:
                        matrix[i][j] = match
                        #dictionary[currX, currY] = [prevX, prevY]
                        pathDictionary[str(i) + "," + str(j)] = str(i - 1) + "," + str(j - 1)
                    elif gapPenalty2 >= gapPenalty1 and gapPenalty2 >= match:
                        matrix[i][j] = gapPenalty2
                        pathDictionary[str(i) + "," + str(j)] = str(i) + "," + str(j - 1)
                    elif gapPenalty1 >= gapPenalty2 and gapPenalty1 >= match:
                        matrix[i][j] = gapPenalty1
                        pathDictionary[str(i) + "," + str(j)] = str(i - 1) + "," + str(j)
                    #move a char forward on xAxis
                    colAcc += 1
        #move a char forward on y axis, and restart x axis
        rowAcc += 1
        colAcc = 0
    return xAxis, yAxis, matrix, pathDictionary

def createScoreMatrix(fileInput):
    scoringMatrix = []
    newMatrix = []
    penaltyScore = 0
    rowMax = 0

    f = open(fileInput, "r")

    #Read each line and split at spaces to get numbers ar each line
    for line in f: 
        if "#" not in line:
            line = line.split()
            
            #append item to temporary list 
            for item in line:
                newMatrix.append(item)

            #append temporary list to final list
            scoringMatrix.append(newMatrix)
            newMatrix = []
    #Get penalty score from last pos and remove it from list
    penaltyScore = scoringMatrix[len(scoringMatrix) - 1][0]
    scoringMatrix.remove(scoringMatrix[len(scoringMatrix) - 1])

    return scoringMatrix, penaltyScore

def writeFile(seq1, seq2, matrix, path, outFile, globalAlign):
    newSeq1 = ""
    newSeq2 = ""
    yCoord = len(seq2)
    lastY = yCoord
    xCoord = len(seq1)
    lastX = xCoord
    identities = 0

    #Loop htrough our dictionary until we have completed our sequences
    while (xCoord != 0 and yCoord != 0):  
        #Find prev position based on current x and y coordinate 
        if (str(xCoord) + "," + str(yCoord)) in path.keys():
            prev = path[(str(xCoord) + "," + str(yCoord))]
            prev = prev.split(",")

            #Append a character or a gap based on our movement
            if (int(prev[0]) < xCoord) and (int(prev[1]) < yCoord):
                newSeq1 = seq1[int(prev[0])] + newSeq1
                newSeq2 = seq2[int(prev[1])] + newSeq2
            elif (int(prev[0]) < xCoord and int(prev[1]) == yCoord):
                newSeq1 = seq1[int(prev[0])] + newSeq1
                newSeq2 = "_" + newSeq2
            elif (int(prev[0]) == xCoord and int(prev[1]) < yCoord):
                newSeq1 = "_" + newSeq1
                newSeq2 = seq2[int(prev[1])] + newSeq2

            if newSeq1[0] == newSeq2[0]:
                identities += 1
            
            #update x and y coordinate to be the values that we got
            xCoord = int(prev[0]) 
            yCoord = int(prev[1]) 
            
    #For some reason global does not end in 0, 0 so this is here to ensure that it does        
    if globalAlign == "G":
        if xCoord == 0 and yCoord != 0:
            while yCoord != 0:
                newSeq2 = "_" + newSeq2
                yCoord -= 1
        if xCoord != 0 and yCoord == 0:
            while xCoord != 0:
                newSeq1 = "_" + newSeq1
                xCoord -= 1

    line1 = "sequence 1: " + str(yCoord + 1) + " " + newSeq2 + " " + str(lastY)
    line2 = "sequence 2: " + str(xCoord + 1) + " " + newSeq1 + " " + str(lastX)

    f = open(outFile, "w")
    f.write(line1 + "\n")
    f.write(line2 + "\n")
    f.write("Score: " + str(matrix[len(seq1)][len(seq2)]) + "\n")
    f.write("Identities: " + str(identities) + "/" + str(len(newSeq1)) + "(" + str(identities / len(newSeq1)) + ")")
    return newSeq1, newSeq2

def main():
    first, second, align, globalAlign, outFile, matrixType = "", "", "", "", "", ""

    #Ensure that all parameters are valid
    for i in range(len(sys.argv) - 1):
        if "-i" in sys.argv[i]:
            first = sys.argv[i + 1]
            f = open(first, "r")
            line = f.readline()
            if ">" not in line:
                print("Not FASTA file")
                return None
        elif "-j" in sys.argv[i]:
            second = sys.argv[i + 1]
            f = open(second, "r")
            line = f.readline()
            if ">" not in line:
                print("Not FASTA file")
                return None
        elif "-p" in sys.argv[i]:
            align = sys.argv[i + 1]
            if "t" == align.lower() or "f" == align.lower():
                if align.lower() == "t":
                    matrixType = "BLOSUM45.txt"
                else:
                    matrixType = "dnaMatrix.txt"
            else:
                print("Align must be T or F")
                return None
        elif "-atype" in sys.argv[i]:
            globalAlign = sys.argv[i + 1]
            if "g" == globalAlign.lower() or "s" == globalAlign.lower() or "l" == globalAlign.lower():
                if globalAlign.lower() == "g":
                    print("Global Alignment")
                elif globalAlign.lower() == "s":
                    print("Semi-Global Alignment")
                else:
                    print("Local Alignment")
            else:
                print("Align must be G or S or L")
                return None
        elif "-o" in sys.argv[i]:
            outFile = sys.argv[i + 1]
    #Make matrix
    matrixPenalty = createScoreMatrix(matrixType)
    #Apply scoring matrix to sequences 
    array = (alignSequences(first, second, matrixPenalty[0], matrixPenalty[1], globalAlign))

    #Backtrack on matrix to generate to newly aligned sequences
    if len(first) > len(second):
        writeFile(array[0], array[1], array[2], array[3], outFile, globalAlign)
    else:
        writeFile(array[1], array[0], array[2], array[3], outFile, globalAlign)
main()