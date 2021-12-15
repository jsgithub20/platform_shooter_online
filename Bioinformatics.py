# PatternCount("ACTAT", "ACAACTATGCATACTATCGGGAACTATCCT")

def pattern_count(pattern, text):
    count = 0
    i = 0
    while i <= (len(text) - len(pattern)):
        if text[i:(i+len(pattern))] == pattern:
            count += 1
        i += 1
    print(count)


pattern_count("ACAAC", "ACAACTATGCATACTATCGGGAAACAACCTATCCTACAAC")