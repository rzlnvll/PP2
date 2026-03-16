name = "sample2.txt"
with open(name, "w") as file:
    file.write("This is a sample file\n")
    file.write("Python file handling practice\n")
print(f"{name} created")
with open(name, "a") as file:
    file.write("This line was appended later\n")
print("New lines appended")
with open(name, "r") as file:
    print("\nUpdated file contents:")
    print(file.read())