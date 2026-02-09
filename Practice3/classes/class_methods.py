# Methods are functions that belong to a class

# Create a method with parameters:
class Calculator:
    def add(self, a, b):
        return a + b
    def multiply(self, a, b):
        return a * b
calc = Calculator()
print(calc.add(5, 3))
print(calc.multiply(4, 7))

# Methods can modify the properties of an object:
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def celebrate_birthday(self):
        self.age += 1
        print(f"Happy birthday, {self.name}! You are now {self.age}")

p1 = Person("Rozie", 17)
p1.celebrate_birthday()
p1.celebrate_birthday()

# The __str__() method is a special method that controls what is returned when the object is printed:
class Person2:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return f"{self.name} ({self.age})"
p2 = Person2("Rinat", 20)
print(p2)