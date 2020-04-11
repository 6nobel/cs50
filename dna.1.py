import sys
import csv
import cs50

if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py data.csv sequence.txt")

reader = csv.DictReader(open(sys.argv[1]))
columns = len(next(reader))
reader = csv.DictReader(open(sys.argv[1]))
rows = len(list(reader))
database = csv.DictReader(open(sys.argv[1]))
txt = open(sys.argv[2]).read()

counter = [0] * rows
current_row = 0

for row in database:
    for i in range(1, columns):
        #print(int(row[database.fieldnames[i]])*database.fieldnames[i])
        if (int(row[database.fieldnames[i]])*database.fieldnames[i]) in txt: 
            counter[current_row] += 1
            #print((row[database.fieldnames[0]]))
    current_row += 1



for i in range(1, rows):
    if counter[i] == columns - 1:
        print()
        

if max(counter) != columns - 1:
    print('No match')
    
    
