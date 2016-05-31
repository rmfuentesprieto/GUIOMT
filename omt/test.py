a = lambda : None

for cont in range(10):
    b = a
    a = lambda :(cont, b())

print a()