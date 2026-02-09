# Using *args to accept any number of arguments:
def args(*args):
    print("Type:", type(args))
    print("First argument:", args[0])
    print("Second argument:", args[1])
    print("All arguments:", args)
args("Emil", "Tobias", "Linus")

# You can combine regular parameters with *args.
def combine(greeting, *names):
    for name in names:
        print(greeting, name)
combine("Hello", "Emil", "Tobias", "Linus")

# Finding the maximum value:
def maxim(*numbers):
    if len(numbers) == 0:
        return None
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num
print(maxim(3, 7, 2, 9, 1))

# The **kwargs parameter allows a function to accept any number of keyword arguments.
def kwargs(**myvar):
    print("Type:", type(myvar))
    print("Name:", myvar["name"])
    print("Age:", myvar["age"])
    print("All data:", myvar)
kwargs(name = "Tobias", age = 30, city = "Bergen")

# Using * to unpack a list into arguments:
def list_to_args(a, b, c):
    return a + b + c
numbers = [1, 2, 3]
result = list_to_args(*numbers) # Same as: my_function(1, 2, 3)
print(result)

# Using ** to unpack a dictionary into keyword arguments:
def dict_to_kwargs(fname, lname):
    print("Hello", fname, lname)
person = {"fname": "Emil", "lname": "Refsnes"}
dict_to_kwargs(**person)