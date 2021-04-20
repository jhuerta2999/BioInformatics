import sys

def reversalSort(sequence, outFile):
    permDistanceACC = 0
    seqLen = len(sequence)
    convertedSeq = []
    adjacentSeq = []
    tmpArray = []

    #Split the sequence into their starting breakpoints
    for i in range(len(sequence) - 1):
        tmpArray.append(sequence[i])
        if sequence[i] + 1 == sequence[i + 1] or sequence[i] - 1 == sequence[i + 1]:
            adjacentSeq.append(sequence[i])
        else:
            convertedSeq.append(tmpArray)
            tmpArray = []
            
    tmpArray.append(sequence[len(sequence) - 1])
    convertedSeq.append(tmpArray)    

    sequence = convertedSeq

    outFile.write("Permutatiton Distance: " + str(permDistanceACC) + "\n")
    outFile.write("Number of Breakpoints: " + str(len(sequence) - 1) + "\n")
    for segment in sequence:
        outFile.write(str(segment) + " ")
    outFile.write("\n ----------- \n")

    #Loop until the segments are all conencted, when there is only 1 segment length of the orginal sequence
    while len(sequence) != seqLen:
        #Create an array to know which sequences are increasing and decreasing
        decreasingArray = []
        for strip in sequence:
            if len(strip) == 1 or strip[0] > strip[1]:
                decreasingArray.append(True)
            else:
                decreasingArray.append(False)

        decreasingArray[0], decreasingArray[len(decreasingArray) - 1] = False, False

        #Checks if all segments are increasing
        allIncreasing = True
        for item in decreasingArray:
            if item == True:
                allIncreasing = False

        kVal = 0
        kValLoc = 0
        #If an decreasing segment exists, work with it
        if allIncreasing == False:
            #Searching for our K value in a decreasing segment
            for i in range (1,len(sequence) - 1):
                if (sequence[i][len(sequence[i]) - 1] < kVal or kVal == 0) and decreasingArray[i] == True:
                    kVal = sequence[i][len(sequence[i]) - 1]
                    kValLoc = i

            #Searching for our K-1 
            kMinusVal = kVal - 1
            kMinusLoc = 0
            for i in range (len(sequence) - 1):
                if sequence[i][len(sequence[i]) - 1] == kMinusVal:
                    kMinusLoc = i

            reversedSeq = []
            #Based on whether K-1 is on the left or right we will adjust our sequences 
            if kMinusLoc > kValLoc:
                seqBefore = sequence[:kValLoc + 1]
                seqAfter = sequence[kMinusLoc + 1:]
                for i in range(kValLoc + 1, kMinusLoc + 1):
                    segment = sequence[i]
                    segment = segment[::-1]
                    reversedSeq.insert(0, segment)
            else:
                seqBefore = sequence[:kMinusLoc + 1]
                seqAfter = sequence[kValLoc + 1:]
                for i in range(kMinusLoc + 1, kValLoc + 1):
                    segment = sequence[i]
                    segment = segment[::-1]
                    reversedSeq.insert(0, segment)

            combineBefore = seqBefore[len(seqBefore) - 1] + reversedSeq[0]
            combineAfter = []

            #If the length is 3 then we will always reduce breakpoints by 2 and this combines all sequences    
            if len(sequence) == 3:
                newSequence = combineBefore

                for segment in seqAfter:
                    for number in segment:
                        newSequence.append(number)
            #If not adjust sequences accordingly
            else:
                if seqAfter[0][0] == reversedSeq[len(reversedSeq) - 1][len(reversedSeq[len(reversedSeq) - 1]) - 1] + 1:
                    combineAfter = [reversedSeq[len(reversedSeq) - 1] + seqAfter[0]]
                    reversedSeq = reversedSeq[:len(reversedSeq) - 1]
                    seqAfter = seqAfter[1:]
                newSequence = seqBefore[:len(seqBefore) - 1] + [combineBefore] + reversedSeq[1:] + combineAfter + seqAfter
            sequence = newSequence
        #If all increasing just reverse the 2nd segment in the sequence
        else:
            sequence[1] = sequence[1][::-1]

        permDistanceACC +=1 
        outFile.write("Permutatiton Distance: " + str(permDistanceACC) + "\n")
        if seqLen != len(sequence):
            outFile.write("Number of Breakpoints: " + str(len(sequence) - 1) + "\n")
        else:
            outFile.write("Number of Breakpoints: 0\n")

        for segment in sequence:
            outFile.write(str(segment) + " ")

        outFile.write("\n ----------- \n")
    return("Check out file for information")

def main():
    sequenceFile = open(sys.argv[1], "r")

    line = sequenceFile.readline()
    line = line.split()
    sequence = [0]

    for number in line:
        sequence.append(int(number))
    
    sequence.append((len(sequence)))
    
    outFile = open(sys.argv[2], "w")
    outFile.write("Starting Sequence: \n" )

    for item in sequence:
        outFile.write(str(item) + "   ")
    outFile.write("\n ----------- \n")

    print(reversalSort(sequence, outFile))
main()