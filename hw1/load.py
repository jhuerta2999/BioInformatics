def loadSeq(fileName):
    f = open(fileName, "r")
    f.readline()
    
    dnaString = ""

    for line in f:
        line = line.rstrip("\n")
        dnaString += line

    return dnaString
