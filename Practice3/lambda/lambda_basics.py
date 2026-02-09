# A lambda function is a small anonymous function.
def my_func(n):
    return lambda a : a * n
my_doubler = my_func(2)
my_tripler = my_func(3)
print(my_doubler(11))
print(my_tripler(11))
