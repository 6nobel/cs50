from cs50 import get_string

# prompt user to give text
string = get_string("text: ")
string = string.replace("'", "")
string = string.replace('"', '')

# initilize counters
words = 0
sentences = 0
letters = 0

# fill counters
sentences = string.count('.') + string.count('?') + string.count('!')
letters = len(string) - string.count(' ') - string.count('.') - string.count('?') - string.count('!') - string.count(',')
words = string.count(" ") + 1

# pluf them into the formula
grade = 0.0588 * letters / words * 100 - 0.296 * sentences / words * 100 - 15.8

# print result
if grade > 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1")
else:
    print("Grade ")
    print(round(grade))