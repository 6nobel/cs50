from cs50 import get_float

while True:
    cash = get_float("chang owed: ")
    if cash > 0:
        break

cash = round(cash * 100)
coins = 0

while (cash - 25 >= 0):
    cash -= 25
    coins += 1

while (cash - 10 >= 0):
    cash -= 10
    coins += 1

while (cash - 5 >= 0):
    cash -= 5
    coins += 1

while (cash - 1 >= 0):
    cash -= 1
    coins += 1

print(coins)
