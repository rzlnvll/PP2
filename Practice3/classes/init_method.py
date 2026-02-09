# Create a class named Person, use the __init__() method to assign values for name and age:
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
p1 = Person("Rozie", 36)
print(p1.name)
print(p1.age)

# Set a default value for the age parameter:
class Person2:
    def __init__(self, name, age=18):
        self.name = name
        self.age = age

p1 = Person2("Rozie")
p2 = Person2("Rinat", 25)

print(p1.name, p1.age)
print(p2.name, p2.age)