while True:
    h = input("Height:")
    if h.isdigit() and int(h) > 0 and int(h) < 9:
        break

h = int(h)
for i in range(h):
    for j in range(h-1, i, -1):
        print(" ", end="")
    for k in range(i+1):
        print("#", end="")
    print()