import sys
import csv
#program that compares a DNA sequence with the sequences stored in a database

#if incorrect command line argument, ask user for correct usage
if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py data.csv sequence.txt")

#open files
reader = csv.DictReader(open(sys.argv[1]))
columns = len(next(reader))
reader = csv.DictReader(open(sys.argv[1]))
rows = len(list(reader))
txt = open(sys.argv[2]).read()
database = csv.DictReader(open(sys.argv[1]))

#helper variables
sequence_txt = [0] * columns
sequence_database = [0] * columns
names = [0] * rows
found = False

#read sequences in such a way that it makes a list with the values
for i in range(1, columns):
    for j in range(50, 0, -1):
        if (database.fieldnames[i] * j) in txt:
            sequence_txt[i] = j
            break
        
#read database in such a way that it makes a list with values
for row in database:
    sequence_database = [0] * columns
    for i in range(1, columns):
        sequence_database[i] = int(row[database.fieldnames[i]])
        # compares list from sequences with list from databases and return names if matches
        if sequence_database == sequence_txt:
            print (row[database.fieldnames[0]])
            found = True
            break

#if no match was found above, return line No match
if found == False:
    print('No match')