# Python also has a super() function that will make the child class inherit all the methods and properties from its parent:
class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname
    def printname(self):
        print(self.firstname, self.lastname)
class Student(Person):
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)
        self.graduation_year = year
x = Student("Rozalina", "Galiyeva", "2025")
print(f"Hello! My name is {x.firstname} {x.lastname} and I graduated in {x.graduation_year}")
