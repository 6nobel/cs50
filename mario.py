while True:
    h = int(input("Height:"))
    if h > 1 and h < 9:
        break

for i in range(h):
    for j in range(h-1, i, -1):
        print(" ", end="")
    for k in range(i+1):
        print("#", end="")
    print()