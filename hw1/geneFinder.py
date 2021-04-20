from load import*
from dna import*
import random

def oneFrame(DNA):
    startCodon = ""
    ORFArray = []
    ORFacc = 0

    codonArray = [""]
    codonAcc = 0

    for char in DNA:
        if len(codonArray[codonAcc]) % 3 != 0:
            codonArray[codonAcc] += char
        else:
            codonArray.append("")
            codonAcc += 1
            codonArray[codonAcc] += char
    codonArray.pop(0)
    
    for i in range(len(codonArray)):
        if codonArray[i] == "ATG":
            ORFArray.append("")
            codonAcc = i

            while codonArray[codonAcc] != "TAG" and codonArray[codonAcc] != "TAA" and codonArray[codonAcc] != "TGA" and codonAcc < len(codonArray):
                ORFArray[ORFacc] += codonArray[codonAcc]
                codonAcc += 1
                if codonAcc >= len(codonArray):
                    break

            if ORFArray[ORFacc] == "ATG":
                ORFArray.pop()
                ORFacc -= 1
            ORFacc += 1
    return ORFArray

def oneFrameV2(DNA):
    ORFArray = oneFrame(DNA)
    
    if ORFArray != None:
        if len(ORFArray) != 0:
            ORFacc = len(ORFArray)
            reducedArray = []

            while ORFacc > 1:
                if ORFArray[ORFacc - 1] not in ORFArray[ORFacc - 2]:
                    reducedArray.insert(0, ORFArray[ORFacc - 1])
                ORFacc -= 1

            reducedArray.insert(0, ORFArray[0])

            return reducedArray
        else:
            return None

def longestORF(DNA):
    longestORF = []
    longest = ""
    for i in range(3):
        newLongestORF = oneFrameV2(DNA[i:])
        if newLongestORF != None:
            for orf in newLongestORF:
                if orf != None:
                    longestORF.append(orf)
    
    for orf in longestORF:
        if len(orf) > len(longest):
            longest = orf
    return longest

def longestORFBothStrands(DNA):
    longest = longestORF(DNA)
    reverse = reverseComplement(DNA)
    revComplement = longestORF(reverse)
    if len(longest) > len(revComplement):
        return longest
    else:
        return revComplement

def longestORFNoncoding(DNA, numReps):
    aaArray = list(DNA)
    longest = ""

    for i in range(numReps):
        random.shuffle(aaArray)
        collapsed = collapse(aaArray)
        newLongest = longestORFBothStrands(collapsed)

        if len(newLongest) > len(longest):
            longest = newLongest

    return len(longest)

def collapse(L):
    collapsed = ""

    for char in L:
        collapsed += char

    return collapsed

def findORFs(DNA):
    ORFArray = []

    for i in range(3):
        newLongestORF = oneFrameV2(DNA[i:])
        if newLongestORF != None:
            for orf in newLongestORF:
                if orf != None:
                    ORFArray.append(orf)
    
    return ORFArray

def findORFsBothStrands(DNA):
    ORFArray = []
    ORFArray += findORFs(DNA)
    reverse = reverseComplement(DNA)
    ORFArray += findORFs(reverse)

    return ORFArray

def getCoordinates(orf, DNA):
    startCoord = DNA.find(orf)

    if startCoord == -1:
        reverseORF = reverseComplement(orf)
        startCoord = DNA.find(reverseORF)

    endCoord = len(orf) + startCoord 

    return [startCoord, endCoord]

def geneFinder(DNA, minLen):
    bothORFs = findORFsBothStrands(DNA)
    reducedArray = []
    arrayAcc = 0

    for orf in bothORFs:
        if len(orf) > minLen:
            reducedArray.append(getCoordinates(orf, DNA))
            reducedArray[arrayAcc].append(codingStrandToAA(orf))
            arrayAcc += 1
    reducedArray.sort()
    return reducedArray

def printGenes(genesList):
    for gene in genesList:
        print(gene, "\n")

    return

def main():
    salmonella = loadSeq("X73525.fa")
    longest = longestORFNoncoding(salmonella, 1500)
    genes = geneFinder(salmonella, longest)
    printGenes(genes)
main()   