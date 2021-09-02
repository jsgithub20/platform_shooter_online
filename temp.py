import csv
font_lst = []
with open("font_lst.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for item in reader:
        font_lst.append(item[0])

print('arial' in font_lst)
