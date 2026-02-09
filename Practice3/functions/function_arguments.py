# a function with one argument 
def greet(name):
    print(f"hello, {name}!") # name is a parameter
name1 = input()
greet(name1) # name1 is an argument

# You can send arguments with the key = value syntax.
def my_animal(animal, name):
    print("I have a", animal)
    print("My", animal + "'s name is", name)
my_animal(animal = "dog", name = "Buddy")

# You can send any data type as an argument to a function (string, number, list, dictionary, etc.).
def name_age(person):
    print("Name:", person["name"])
    print("Age:", person["age"])
my_person = {"name": "Emil", "age": 25}
name_age(my_person)