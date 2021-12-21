freq = {"act": 3, "cg": 2}
act_v = freq["act"]
print(act_v)
m = max(freq.values())

print(max(freq.values()))
print(freq.keys())

words = []

for key in freq:
    if freq[key] == m:
        words.append(key)

print(words)