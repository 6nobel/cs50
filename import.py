from cs50 import SQL
import csv
import sys

# start DB
db = SQL("sqlite:///students.db")

# if command line argument wrong, prompt message
if len(sys.argv) != 2:
    sys.exit("Usage: python import.py characters.csv")

# open csv file
reader = csv.DictReader(open(sys.argv[1]))

# go through each row and copy to data base
for row in reader:
    # split name into 2 or 3 parts
    name = row["name"].split()
    if len(name) == 2:  # print to DB as first null last
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", 
                   name[0], None, name[1], row["house"], row["birth"])
    if len(name) == 3:  # print to DB as first middle last
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", 
                   name[0], name[1], name[2], row["house"], row["birth"])