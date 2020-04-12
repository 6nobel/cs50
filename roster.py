from cs50 import SQL
import csv
import sys

# start DB
db = SQL("sqlite:///students.db")

# if command line argument wrong, prompt message
if len(sys.argv) != 2:
    sys.exit("Usage: python roster.py house")

# make house a variable    
house = sys.argv[1]

# SQL Query
reader = db.execute("SELECT first, middle, last, birth FROM students WHERE house =? ORDER BY last, first", house)

# printing out the SQL result
for row in reader:
    if row['middle'] == None:
        print(row['first'], row['last'], row['birth'])
    else:
        print(row['first'], row['middle'], row['last'], row['birth']) 