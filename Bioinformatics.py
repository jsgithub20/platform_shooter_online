# PatternCount("ACTAT", "ACAACTATGCATACTATCGGGAACTATCCT")

def pattern_count(pattern, text):
    positions = []
    count = 0
    i = 0
    while i <= (len(text) - len(pattern)):
        if text[i:(i+len(pattern))] == pattern:
            count += 1
            positions.append(i)
        i += 1
    print(count)


def PatternMatching(Pattern, Genome):
    positions = []  # output variable
    i = 0
    while i <= (len(Genome) - len(Pattern)):
        if Genome[i:(i+len(Pattern))] == Pattern:
            positions.append(i)
        i += 1
    return positions


def FrequencyMap(Text, k):
    freq = {}
    n = len(Text)
    for i in range(n-k+1):
        Pattern = Text[i:i+k]
        freq[Pattern] = 0
        for x in range(n-k+1):
            if Text[x:x+k] == Pattern:
                freq[Pattern] += 1
    return freq


def FrequentWords(Text, k):
    words = []
    freq = FrequencyMap(Text, k)
    m = max(freq.values())
    for key in freq:
        if freq[key] == m:
            words.append(key)
    return words


def Reverse(Pattern):
    # your code here
    revstr = ""
    for char in Pattern:
        revstr = char + revstr

    return revstr


# Input:  A DNA string Pattern
# Output: The complementary string of Pattern (with every nucleotide replaced by its complement).
def Complement(Pattern):
    # your code here
    bp = {"A":"T", "G":"C", "T":"A", "C":"G"}
    complement = ""
    for base in Pattern:
        complement += bp.get(base)
    return complement


# Input:  A DNA string Pattern
# Output: The reverse complement of Pattern
def ReverseComplement(Pattern):
    # your code here
    Pattern = Reverse(Pattern)
    Pattern = Complement(Pattern)
    return Pattern


# fill in your PatternMatching() function along with any subroutines that you need.
# def PatternMatching(Pattern, Genome):
#     positions = []  # output variable
#     count = 0
#     i = 0
#     while i <= (len(Genome) - len(Pattern)):
#         if Genome[i:(i + len(Pattern))] == Pattern:
#             count += 1
#         i += 1
#     return positions


# pattern_count("ACAAC", "ACAACTATGCATACTATCGGGAAACAACCTATCCTACAAC")
# Input:
#     TTT
#     AGCGTGCCGAAATATGCCGCCAGACCTGCTGCGGTGGCCTCGCCGACTTCACGGATGCCAAGTGCATAGAGGAAGCGAGCAAAGGTGGTTTCTTTCGCTTTATCCAGCGCGTTAACCACGTTCTGTGCCGACTTT
# Output:
#     88 92 98 132

pm = PatternMatching("TTT", "AGCGTGCCGAAATATGCCGCCAGACCTGCTGCGGTGGCCTCGCCGACTTCACGGATGCCAAGTGCATAGAGGAAGCGAGCAAAGGTGGTTTCTTTCGCTTTATCCAGCGCGTTAACCACGTTCTGTGCCGACTTT")
print(pm)