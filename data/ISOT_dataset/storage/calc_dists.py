import json

ifile = open("users_features.csv", 'r')
ifile.readline()[:-1]

csv_lst = []
for line in ifile:
    csv = line[:-1].split(',')
    csv_lst.append(csv)

dists = []
for r in range(len(csv_lst)):
    curr_csv = csv_lst[r]
    dists.append([])
    for r2 in range(len(csv_lst)):
        if r == r2:
            continue
        next_csv = csv_lst[r2]
        inner_sum = 0.0
        for c in range(1,len(curr_csv)):
            inner_sum += (abs(float(curr_csv[c])-float(next_csv[c])))**2
        dist = inner_sum**(.5)
        dists[r].append(dist)

jsonfile = open("dists.json", 'w')
json.dump(dists, jsonfile, indent=2)

csv_file = open("dists.csv", 'w')
csv_file.write(f"user")
for i in range(26):
    csv_file.write(f",user{i+1}")
csv_file.write('\n')

for row in range(len(dists)):
    csv_file.write(f"user{row+1}")
    back_one = 0
    for col in range(len(dists[row])+1):
        if row == col:
            csv_file.write(", ")
            back_one = 1
            continue
        if back_one:
            col -= 1
        csv_file.write(f",{dists[row][col]}")
    csv_file.write('\n')

