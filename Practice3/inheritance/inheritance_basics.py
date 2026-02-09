# Inheritance allows us to define a class that inherits all the methods and properties from another class.
class Person:  # parent class
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname
    def printname(self):
        print(self.firstname, self.lastname)
class Student(Person): # child class that has the same properties and methods as the parent class.
    pass
x = Student("Mike", "Olsen")
x.printname()
