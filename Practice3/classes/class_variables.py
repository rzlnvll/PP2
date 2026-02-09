# Properties are variables that belong to a class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
p1 = Person("Rozie", 17)
print(p1.name)
print(p1.age)

# Class property vs instance property:
class Person2:
    species = "Human" # Class property
    def __init__(self, name):
        self.name = name # Instance property
p1 = Person2("Rozie")
p2 = Person2("Rinat")
print(p1.name)
print(p2.name)
print(p1.species)
print(p2.species)
