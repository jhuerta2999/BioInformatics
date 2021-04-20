from load import*
from dna import*
import random

def oneFrame(DNA):
    startCodon = ""
    ORFArray = []
    ORFacc = 0

    if "ATG" not in DNA:
        print("NO START CODON")
        return None
    else:
        for i in range(len(DNA)):
            print(startCodon)
            if "ATG" not in startCodon and len(startCodon) % 3 != 0:
                if startCodon % 3 == 0:
                    print(startCodon)
                    startCodon = ""
                    print(startCodon)
                startCodon += DNA[i]


            else:
                DNAacc = i
                # print(DNA[DNAacc])
                ORFArray.append("")
                
               # codon = DNA[DNAacc - 2] + (DNA[DNAacc - 1]) + (DNA[DNAacc])
                # print(codon)
                # print(len(DNA))
                # print(DNAacc)
                while "TAG" not in ORFArray[ORFacc] and "TAA" not in ORFArray[ORFacc] and "TGA" not in ORFArray[ORFacc] and len(ORFArray[ORFacc]) % 3 == 0 and DNAacc < len(DNA):
                    #DNAacc += 1
                    print("before: ", ORFArray[ORFacc])
                    ORFArray[ORFacc] += DNA[DNAacc] 
                    print("after: ", ORFArray[ORFacc])

                    DNAacc += 1
                    # if DNAacc < len(DNA):
                    #     codon = DNA[DNAacc - 2] + (DNA[DNAacc - 1]) + (DNA[DNAacc])
                    # print(codon)
                    # print(DNAacc)

                # print("before: ", ORFArray[ORFacc])
                ORFArray[ORFacc] = "ATG" + ORFArray[ORFacc]
                # print("after: ", ORFArray[ORFacc])
                
                if ORFArray[ORFacc] == "ATG":
                    ORFArray.pop()
                    ORFacc -= 1
                ORFacc += 1
                startCodon = ""

        return ORFArray

def oneFrameV2(DNA):
    ORFArray = oneFrame(DNA)
    
    if ORFArray != None:
        if len(ORFArray) != 0:
            # print(ORFArray)
            # print("fjnsjinfis")
            ORFacc = len(ORFArray)
            reducedArray = []

            while ORFacc > 1:
                if ORFArray[ORFacc - 1] not in ORFArray[ORFacc - 2]:
                    reducedArray.insert(0, ORFArray[ORFacc - 1])
                ORFacc -= 1

            reducedArray.insert(0, ORFArray[0])

            return reducedArray
        else:
            print("NO START CODON")
            return None

def longestORF(DNA):
    longestORF = ""
    for i in range(3):
        newLongestORF = oneFrameV2(DNA[i:-(2-i)])
        # print(newLongestORF)
        print(i)
        if newLongestORF != None:
            if len(newLongestORF[i]) > len(longestORF):
                longestORF = newLongestORF
    return longestORF

def longestORFBothStrands(DNA):
    longest = longestORF(DNA)
    reverse = reverseComplement(DNA)
    revComplement = longestORF(reverse)
    # print(longest)
    # print(revComplement)
    if len(longest) > len(revComplement):
        return longest
    else:
        return revComplement

def longestORFNoncoding(DNA, numReps):
    aaArray = list(DNA)
    

def main():
    #print(oneFrame("CATGAATAGGCCCA"))  
    #print(oneFrameV2("ATGCCCTAACATGAAAATGACTTAGG"))
    print(longestORF("ATGAAATAG"))
    #print(longestORFBothStrands("CTATTTCATG"))
main()   