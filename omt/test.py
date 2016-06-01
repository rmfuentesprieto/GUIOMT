def make_funcion(f_extract_new, f_extract_old):
    return lambda : (f_extract_new(),f_extract_old())

def num(n):
    return lambda :n + 1

a = lambda : 0

for cont in range(10):

    a = make_funcion(lambda :cont+1 , a)

print a()

def nx(x):
    return lambda y : x + y

add1 = nx(1)
add2 = nx(2)

print add1(1)
print add2(1)