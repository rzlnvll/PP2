# Use self to access class properties:
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def greet(self):
        print("Hello, my name is " + self.name)
p1 = Person("Rozie", 25)
p1.greet()

# Call one method from another method using self:
class Person2:
    def __init__(self, name):
        self.name = name
    def greet(self):
        return "Hello, " + self.name
    def welcome(self):
        message = self.greet()
        print(message + "! Welcome to our website.")
p2 = Person2("Rozie")
p2.welcome()