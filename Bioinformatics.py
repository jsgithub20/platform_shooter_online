import random

# # PatternCount("ACTAT", "ACAACTATGCATACTATCGGGAACTATCCT")
#
# def pattern_count(pattern, text):
#     positions = []
#     count = 0
#     i = 0
#     while i <= (len(text) - len(pattern)):
#         if text[i:(i+len(pattern))] == pattern:
#             count += 1
#             positions.append(i)
#         i += 1
#     print(count)
#
#
# def PatternMatching(Pattern, Genome):
#     positions = []  # output variable
#     i = 0
#     while i <= (len(Genome) - len(Pattern)):
#         if Genome[i:(i+len(Pattern))] == Pattern:
#             positions.append(i)
#         i += 1
#     return positions
#
#
# def FrequencyMap(Text, k):
#     freq = {}
#     n = len(Text)
#     for i in range(n-k+1):
#         Pattern = Text[i:i+k]
#         freq[Pattern] = 0
#         for x in range(n-k+1):
#             if Text[x:x+k] == Pattern:
#                 freq[Pattern] += 1
#     return freq
#
#
# def FrequentWords(Text, k):
#     words = []
#     freq = FrequencyMap(Text, k)
#     m = max(freq.values())
#     for key in freq:
#         if freq[key] == m:
#             words.append(key)
#     return words
#
#
# def Reverse(Pattern):
#     # your code here
#     revstr = ""
#     for char in Pattern:
#         revstr = char + revstr
#
#     return revstr
#
#
# # Input:  A DNA string Pattern
# # Output: The complementary string of Pattern (with every nucleotide replaced by its complement).
# def Complement(Pattern):
#     # your code here
#     bp = {"A":"T", "G":"C", "T":"A", "C":"G"}
#     complement = ""
#     for base in Pattern:
#         complement += bp.get(base)
#     return complement
#
#
# # Input:  A DNA string Pattern
# # Output: The reverse complement of Pattern
# def ReverseComplement(Pattern):
#     # your code here
#     Pattern = Reverse(Pattern)
#     Pattern = Complement(Pattern)
#     return Pattern
#
#
# # fill in your PatternMatching() function along with any subroutines that you need.
# # def PatternMatching(Pattern, Genome):
# #     positions = []  # output variable
# #     count = 0
# #     i = 0
# #     while i <= (len(Genome) - len(Pattern)):
# #         if Genome[i:(i + len(Pattern))] == Pattern:
# #             count += 1
# #         i += 1
# #     return positions
#
#
# # pattern_count("ACAAC", "ACAACTATGCATACTATCGGGAAACAACCTATCCTACAAC")
# # Input:
# #     TTT
# #     AGCGTGCCGAAATATGCCGCCAGACCTGCTGCGGTGGCCTCGCCGACTTCACGGATGCCAAGTGCATAGAGGAAGCGAGCAAAGGTGGTTTCTTTCGCTTTATCCAGCGCGTTAACCACGTTCTGTGCCGACTTT
# # Output:
# #     88 92 98 132
#
# pm = PatternMatching("TTT", "AGCGTGCCGAAATATGCCGCCAGACCTGCTGCGGTGGCCTCGCCGACTTCACGGATGCCAAGTGCATAGAGGAAGCGAGCAAAGGTGGTTTCTTTCGCTTTATCCAGCGCGTTAACCACGTTCTGTGCCGACTTT")
# print(pm)

# E_coli.txt
# Input:  Strings Genome and symbol
# Output: SymbolArray(Genome, symbol)
def SymbolArray(Genome, symbol):
    # type your code here
    array = {}
    n = len(Genome)
    ExtendedGenome = Genome + Genome[0:n // 2]
    for i in range(n):
        array[i] = PatternCount(symbol, ExtendedGenome[i:i + (n // 2)])
    return array


# Reproduce the PatternCount function here.
def PatternCount(Pattern, Text):
    count = 0
    for i in range(len(Text) - len(Pattern) + 1):
        if Text[i:i + len(Pattern)] == Pattern:
            count = count + 1
    return count


def FasterSymbolArray(Genome, symbol):
    array = {}
    n = len(Genome)
    ExtendedGenome = Genome + Genome[0:n // 2]

    # look at the first half of Genome to compute first array value
    array[0] = PatternCount(symbol, Genome[0:n // 2])

    for i in range(1, n):
        # start by setting the current array value equal to the previous array value
        array[i] = array[i - 1]

        # the current array value can differ from the previous array value by at most 1
        if ExtendedGenome[i - 1] == symbol:
            array[i] -= 1
        if ExtendedGenome[i + (n // 2) - 1] == symbol:
            array[i] += 1
    return array


def SkewArray(Genome):
    Skew = []
    Skew.append(0)
    for j in range(len(Genome)):
        if Genome[j] == "A" or Genome[j] == "T":
            Skew.append(Skew[j])
        elif Genome[j] == "G":
            Skew.append(Skew[j] + 1)
        elif Genome[j] == "C":
            Skew.append((Skew[j] - 1))

    return Skew


# print(SkewArray("CATGGGCATCGGCCATACGCC"))

# Input:  Two strings p and q
# Output: An integer value representing the Hamming Distance between p and q.
def HammingDistance(p, q):
    c = 0
    for i in range(len(p)):
        if p[i] != q[i]:
            c += 1

    return c


# p = "GGGCCGTTGGT"
# q = "GGACCGTTGAC"

# print(HammingDistance(p, q))

# Input:  Strings Pattern and Text along with an integer d
# Output: A list containing all starting positions where Pattern appears
# as a substring of Text with at most d mismatches
def ApproximatePatternMatching(Text, Pattern, d):
    c = []
    l = len(Pattern)
    for i in range(len(Text) - l + 1):
        if HammingDistance(Text[i:i + l], Pattern) <= d:
            c.append(i)
    return c


# p = "ATTCTGGA"
# t = "CGCCCGAATCCAGAACGCATTCCCATATTTCGGGACCACTGGCCTCCACGGTACGGACGTCAATCAAAT"
#
# # print(ApproximatePatternMatching(t, p, 3))
#
# one = "TGACCCGTTATGCTCGAGTTCGGTCAGAGCGTCATTGCGAGTAGTCGTTTGCTTTCTCAAACTCC"
# two = "GAGCGATTAAGCGTGACAGCCCCAGGGAACCCACAAAACGTGATCGCAGTCCATCCGATCATACA"
#
# # print(HammingDistance(one, two))
# three = "GATACACTTCCCGAGTAGGTACTG"

# print(SkewArray(three))

# Input:  A set of kmers Motifs
# Output: Count(Motifs)
def Count(Motifs):
    count = {}  # initializing the count dictionary
    k = len(Motifs[0])
    for symbol in "ACGT":
        count[symbol] = []
        for j in range(k):
            count[symbol].append(0)
    t = len(Motifs)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            count[symbol][j] += 1
    return count


# Input:  A list of kmers Motifs
# Output: the profile matrix of Motifs, as a dictionary of lists.
def Profile(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    profile = Count(Motifs)
    for key, v in profile.items():
        # v = [x/t for x in v]
        # print(v)
        profile[key] = [x / t for x in v]
    return profile


# Input:  A set of kmers Motifs
# Output: A consensus string of Motifs.
def Consensus(Motifs):
    k = len(Motifs[0])
    count = Count(Motifs)
    consensus = ""
    for j in range(k):
        m = 0
        frequentSymbol = ""
        for symbol in "ACGT":
            if count[symbol][j] > m:
                m = count[symbol][j]
                frequentSymbol = symbol
        consensus += frequentSymbol
    return consensus


a1 = "0.4  0.3  0.0  0.1  0.0  0.9"
b1 = "0.2  0.3  0.0  0.4  0.0  0.1"
g1 = "0.1  0.3  1.0  0.1  0.5  0.0"
t1 = "0.3  0.1  0.0  0.4  0.5  0.0"

profile2 = {"A": [float(f) for f in a1.split("  ")],
            "C": [float(f) for f in b1.split("  ")],
            "G": [float(f) for f in g1.split("  ")],
            "T": [float(f) for f in t1.split("  ")]}


# Input:  A set of k-mers Motifs
# Output: The score of these k-mers.
def Score(Motifs):
    c_str = Consensus(Motifs)
    score = 0
    t = len(Motifs)
    k = len(Motifs[0])
    for j in range(k):
        for i in range(t):
            if Motifs[i][j] != c_str[j]:
                score += 1
    return score


# Input:  String Text and profile matrix Profile
# Output: Pr(Text, Profile)
def Pr(Text, Profile):
    p = 1
    for i in range(len(Text)):
        p *= Profile[Text[i]][i]

    return p


# print(Pr("CAGTGA", profile2))


# print(Pr("ATGCTA", profile2))
# print(Pr("ACGCGA", profile2))
# print(Pr("AGGTGA", profile2))
# print(Pr("AGGCTA", profile2))
# print(Pr("AAGAGA", profile2))
# print(Pr("TCGCGA", profile2))

# Write your ProfileMostProbableKmer() function here.
# The profile matrix assumes that the first row corresponds to A, the second corresponds to C,
# the third corresponds to G, and the fourth corresponds to T.
# You should represent the profile matrix as a dictionary whose keys are 'A', 'C', 'G', and 'T' and whose values are lists of floats
def ProfileMostProbableKmer(text, k, profile):
    p = -1
    most = ""
    for i in range(len(text) - k + 1):
        kmer = text[i:i + k]
        pk = Pr(kmer, profile)
        if pk > p:
            most = kmer
            p = pk

    return most


text1 = "ACCTGTTTATTGCCTAAGTTCCGAACAAACCCAATATAGCCCGAGGGCCT"
a1 = "0.2 0.2 0.3 0.2 0.3"
b1 = "0.4 0.3 0.1 0.5 0.1"
g1 = "0.3 0.3 0.5 0.2 0.4"
t1 = "0.1 0.2 0.1 0.1 0.2"

profile1 = {"A": [float(f) for f in a1.split(" ")],
            "C": [float(f) for f in b1.split(" ")],
            "G": [float(f) for f in g1.split(" ")],
            "T": [float(f) for f in t1.split(" ")]}


# print(ProfileMostProbableKmer(text1, 5, profile1))

# Input:  A list of kmers Dna, and integers k and t (where t is the number of kmers in Dna)
# Output: GreedyMotifSearch(Dna, k, t)
def GreedyMotifSearch(Dna, k, t):
    BestMotifs = []
    for i in range(0, t):
        BestMotifs.append(Dna[i][0:k])
    n = len(Dna[0])
    for i in range(n - k + 1):
        Motifs = []
        Motifs.append(Dna[0][i:i + k])
        for j in range(1, t):
            P = Profile(Motifs[0:j])
            Motifs.append(ProfileMostProbableKmer(Dna[j], k, P))
        if Score(Motifs) < Score(BestMotifs):
            BestMotifs = Motifs

    return BestMotifs


# dna = ["GGCGTTCAGGCA", "AAGAATCAGTCA", "CAAGGAGTTCGC", "CACGTCAATCAC", "CAATAATATTCG"]

# motifs = GreedyMotifSearch(dna, 3, 5)
# print(motifs)
# print(Score(motifs))

# dna = [
# "GCGCCCCGCCCGGACAGCCATGCGCTAACCCTGGCTTCGATGGCGCCGGCTCAGTTAGGGCCGGAAGTCCCCAATGTGGCAGACCTTTCGCCCCTGGCGGACGAATGACCCCAGTGGCCGGGACTTCAGGCCCTATCGGAGGGCTCCGGCGCGGTGGTCGGATTTGTCTGTGGAGGTTACACCCCAATCGCAAGGATGCATTATGACCAGCGAGCTGAGCCTGGTCGCCACTGGAAAGGGGAGCAACATC",
# "CCGATCGGCATCACTATCGGTCCTGCGGCCGCCCATAGCGCTATATCCGGCTGGTGAAATCAATTGACAACCTTCGACTTTGAGGTGGCCTACGGCGAGGACAAGCCAGGCAAGCCAGCTGCCTCAACGCGCGCCAGTACGGGTCCATCGACCCGCGGCCCACGGGTCAAACGACCCTAGTGTTCGCTACGACGTGGTCGTACCTTCGGCAGCAGATCAGCAATAGCACCCCGACTCGAGGAGGATCCCG",
# "ACCGTCGATGTGCCCGGTCGCGCCGCGTCCACCTCGGTCATCGACCCCACGATGAGGACGCCATCGGCCGCGACCAAGCCCCGTGAAACTCTGACGGCGTGCTGGCCGGGCTGCGGCACCTGATCACCTTAGGGCACTTGGGCCACCACAACGGGCCGCCGGTCTCGACAGTGGCCACCACCACACAGGTGACTTCCGGCGGGACGTAAGTCCCTAACGCGTCGTTCCGCACGCGGTTAGCTTTGCTGCC",
# "GGGTCAGGTATATTTATCGCACACTTGGGCACATGACACACAAGCGCCAGAATCCCGGACCGAACCGAGCACCGTGGGTGGGCAGCCTCCATACAGCGATGACCTGATCGATCATCGGCCAGGGCGCCGGGCTTCCAACCGTGGCCGTCTCAGTACCCAGCCTCATTGACCCTTCGACGCATCCACTGCGCGTAAGTCGGCTCAACCCTTTCAAACCGCTGGATTACCGACCGCAGAAAGGGGGCAGGAC",
# "GTAGGTCAAACCGGGTGTACATACCCGCTCAATCGCCCAGCACTTCGGGCAGATCACCGGGTTTCCCCGGTATCACCAATACTGCCACCAAACACAGCAGGCGGGAAGGGGCGAAAGTCCCTTATCCGACAATAAAACTTCGCTTGTTCGACGCCCGGTTCACCCGATATGCACGGCGCCCAGCCATTCGTGACCGACGTCCCCAGCCCCAAGGCCGAACGACCCTAGGAGCCACGAGCAATTCACAGCG",
# "CCGCTGGCGACGCTGTTCGCCGGCAGCGTGCGTGACGACTTCGAGCTGCCCGACTACACCTGGTGACCACCGCCGACGGGCACCTCTCCGCCAGGTAGGCACGGTTTGTCGCCGGCAATGTGACCTTTGGGCGCGGTCTTGAGGACCTTCGGCCCCACCCACGAGGCCGCCGCCGGCCGATCGTATGACGTGCAATGTACGCCATAGGGTGCGTGTTACGGCGATTACCTGAAGGCGGCGGTGGTCCGGA",
# "GGCCAACTGCACCGCGCTCTTGATGACATCGGTGGTCACCATGGTGTCCGGCATGATCAACCTCCGCTGTTCGATATCACCCCGATCTTTCTGAACGGCGGTTGGCAGACAACAGGGTCAATGGTCCCCAAGTGGATCACCGACGGGCGCGGACAAATGGCCCGCGCTTCGGGGACTTCTGTCCCTAGCCCTGGCCACGATGGGCTGGTCGGATCAAAGGCATCCGTTTCCATCGATTAGGAGGCATCAA",
# "GTACATGTCCAGAGCGAGCCTCAGCTTCTGCGCAGCGACGGAAACTGCCACACTCAAAGCCTACTGGGCGCACGTGTGGCAACGAGTCGATCCACACGAAATGCCGCCGTTGGGCCGCGGACTAGCCGAATTTTCCGGGTGGTGACACAGCCCACATTTGGCATGGGACTTTCGGCCCTGTCCGCGTCCGTGTCGGCCAGACAAGCTTTGGGCATTGGCCACAATCGGGCCACAATCGAAAGCCGAGCAG",
# "GGCAGCTGTCGGCAACTGTAAGCCATTTCTGGGACTTTGCTGTGAAAAGCTGGGCGATGGTTGTGGACCTGGACGAGCCACCCGTGCGATAGGTGAGATTCATTCTCGCCCTGACGGGTTGCGTCTGTCATCGGTCGATAAGGACTAACGGCCCTCAGGTGGGGACCAACGCCCCTGGGAGATAGCGGTCCCCGCCAGTAACGTACCGCTGAACCGACGGGATGTATCCGCCCCAGCGAAGGAGACGGCG",
# "TCAGCACCATGACCGCCTGGCCACCAATCGCCCGTAACAAGCGGGACGTCCGCGACGACGCGTGCGCTAGCGCCGTGGCGGTGACAACGACCAGATATGGTCCGAGCACGCGGGCGAACCTCGTGTTCTGGCCTCGGCCAGTTGTGTAGAGCTCATCGCTGTCATCGAGCGATATCCGACCACTGATCCAAGTCGGGGGCTCTGGGGACCGAAGTCCCCGGGCTCGGAGCTATCGGACCTCACGATCACC"
# ]
#
# print(GreedyMotifSearch(dna, 15, 10))
# print(Score(dna))

m1 = [
    "AACGTA",
    "CCCGTT",
    "CACCTT",
    "GGATTA",
    "TTCCGG"]

m2 = [
    "GTACAACTGT",
    "CAACTATGAA",
    "TCCTACAGGA",
    "AAGCAAGGGT",
    "GCGTACGACC",
    "TCGTCAGCGT",
    "AACAAGGTCA",
    "CTCAGGCGTC",
    "GGATCCAGGT",
    "GGCAAGTACC"
]


# Input:  A set of kmers Motifs
# Output: CountWithPseudocounts(Motifs)
def CountWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    count = {}  # initializing the count dictionary
    for symbol in "ACGT":
        count[symbol] = []
        for j in range(k):
            count[symbol].append(1)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            count[symbol][j] += 1
    return count


# print(CountWithPseudocounts(m2))

# Input:  A set of kmers Motifs
# Output: ProfileWithPseudocounts(Motifs)
def ProfileWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    profile = CountWithPseudocounts(Motifs)  # output variable
    for key, v in profile.items():
        profile[key] = [x / t for x in v]
    return profile


# print(ProfileWithPseudocounts(m1))

def Motifs(Profile, Dna):
    motifs = []
    for i in range(len(Dna)):
        text = Dna[i]
        k = len(Profile["A"])
        probable = ProfileMostProbableKmer(text, k, Profile)
        motifs.append(probable)
    return motifs


Dna = [
    "TGACGTTC",
    "TAAGAGTT",
    "GGACGAAA",
    "CTGTTCGC"]

def RandomizedMotifSearch(Dna, k, t):
    # M = RandomMotifs(Dna, k, t)
    M = ["TGA", "GTT", "GAA", "TGT"]
    BestMotifs = M
    while True:
        Profile = ProfileWithPseudocounts(M)
        M = Motifs(Profile, Dna)
        if Score(M) < Score(BestMotifs):
            BestMotifs = M
        else:
            return BestMotifs


print(RandomizedMotifSearch(Dna, 3, 4))

# Input:  Integers k, t, and N, followed by a collection of strings Dna
# Output: GibbsSampler(Dna, k, t, N)
def GibbsSampler(Dna, k, t, N):
    randmotifs = RandomMotifs(Dna, k, t)
    BestMotifs = randmotifs
    for j in range(1, N + 1):
        reducedmotifs = []
        i = random.randint(0, t - 1)
        for h in range(0, t):
            if h != i:
                reducedmotifs.append(randmotifs[h])
        profile = ProfileWithPseudocounts(reducedmotifs)
        randmotifs[i] = ProfileGeneratedString(Dna[i], profile, k)
        if Score(randmotifs) < Score(BestMotifs):
            BestMotifs = randmotifs
    return BestMotifs

# ----------------------- subroutines ------------------------
def ProfileGeneratedString(Text, profile, k):
    n = len(Text)
    probabilities = {}
    for i in range(0, n - k + 1):
        probabilities[Text[i:i + k]] = Pr(Text[i:i + k], profile)
    probabilities = Normalize(probabilities)
    return WeightedDie(probabilities)


def WeightedDie(Probabilities):
    count = 0
    randec = random.uniform(0, 1)
    for k, v in Probabilities.items():
        count += v
        if randec <= count:
            return k


def Normalize(Probabilities):
    normalized = {}
    totpr = 0
    for v in Probabilities.values():
        totpr += v
    keys = [k for k in Probabilities]
    for symbol in keys:
        normalized[symbol] = Probabilities[symbol] / totpr
    return normalized


# p = {"A":0.15, "B":0.6, "C":0.225, "D":0.225, "E":0.3}
# print(Normalize(p))

Dna = ["ATGAGGTC",
       "GCCCTAGA",
       "AAATAGAT",
       "TTGTGCTA"]


def RandomizedMotifSearch(Dna, k, t):
    # M = RandomMotifs(Dna, k, t)
    M = ["GTC", "CCC", "ATA", "GCT"]
    BestMotifs = M
    while True:
        Profile = ProfileWithPseudocounts(M)
        M = Motifs(Profile, Dna)
        if Score(M) < Score(BestMotifs):
            BestMotifs = M
        else:
            return BestMotifs


print(RandomizedMotifSearch(Dna, 3, 4))


def RandomMotifs(Dna, k, t):
    ranmotifs = []
    M = len(Dna[0]) - k - 1
    for i in range(len(Dna)):
        ri = random.randint(1, M)
        ranmotifs.append(Dna[i][ri:ri + k])
    return ranmotifs