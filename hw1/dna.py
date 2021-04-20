def reverseComplement(DNA):
    complementDNA = ""

    for char in DNA:
        if char == "T":
            complementDNA = "A" + complementDNA
        elif char == "C":
            complementDNA = "G" + complementDNA
        elif char == "A":
            complementDNA = "T" + complementDNA
        elif char == "G":
            complementDNA = "C" + complementDNA

    return complementDNA

def codingStrandToAA(DNA):
    acidDict = {
        "TTT": "F",
        "TTC": "F",
        "TTA": "L",
        "TTG": "L",
        "TCT": "S",
        "TCC": "S",
        "TCA": "S",
        "TCG": "S",
        "TAT": "Y",
        "TAC": "Y",
        # "TAA": "S" STOP,
        # "TAG": "S" STOP,
        "TGT": "C",
        "TGC": "C",
        # "TGA": "P" STOP,
        "TGG": "W",
        "CTT": "L",
        "CTC": "L",
        "CTA": "L",
        "CTG": "L",
        "CCT": "P",
        "CCC": "P",
        "CCA": "P",
        "CCG": "P",
        "CAT": "H",
        "CAC": "H",
        "CAA": "Q",
        "CAG": "Q",
        "CGT": "R",
        "CGC": "R",
        "CGA": "R",
        "CGG": "R",
        "ATT": "I",
        "ATC": "I",
        "ATA": "I",
        "ATG": "M",
        "ACT": "T",
        "ACC": "T",
        "ACA": "T",
        "ACG": "T",
        "AAT": "N",
        "AAC": "N",
        "AAA": "K",
        "AAG": "K",
        "AGT": "S",
        "AGC": "S",
        "AGA": "R",
        "AGG": "R",
        "GTT": "V",
        "GTC": "V",
        "GTA": "V",
        "GTG": "V",
        "GCT": "A",
        "GCC": "A",
        "GCA": "A",
        "GCG": "A",
        "GAT": "D",
        "GAC": "D",
        "GAA": "E",
        "GAG": "E",
        "GGT": "G",
        "GGC": "G",
        "GGA": "G",
        "GGG": "G",
    }

    codonSeq = ""
    acid = ""

    if len(DNA) % 3 != 0:
        print("ERROR")
        return None
    else:
        for char in DNA:
            if len(codonSeq) == 3:
                if codonSeq in acidDict:
                    acid += acidDict.get(codonSeq)
                    codonSeq = "" + char
            else:
                codonSeq += char

        if codonSeq in acidDict:
            acid += acidDict.get(codonSeq)

    return acid
