import sys
import csv
import cs50

if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py data.csv sequence.txt")

reader = csv.DictReader(open(sys.argv[1]))
columns = len(next(reader))
reader = csv.DictReader(open(sys.argv[1]))
rows = len(list(reader))
txt = open(sys.argv[2]).read()
database = csv.DictReader(open(sys.argv[1]))

sequence_txt = [0] * columns
sequence_database = [0] * columns
names = [0] * rows
found = False

for i in range(1, columns):
    for j in range(50, 0, -1):
        if (database.fieldnames[i] * j) in txt:
            sequence_txt[i] = j
            break

for row in database:
    for i in range(1, columns):
        sequence_database[i] = int(row[database.fieldnames[i]])
        if sequence_database == sequence_txt:
            print (row[database.fieldnames[0]])
            found = True
            break

if found == False:
    print('No match')