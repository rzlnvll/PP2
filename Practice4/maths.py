import math
# exercise 1 ----------------------------------------------------------------
d = float(input("Input degree: "))
r = d * math.pi / 180
print("Output radian:", format(r, ".6f"))

# exercise 2 ----------------------------------------------------------------
h = float(input("Height: "))
b1 = float(input("Base, first value: "))
b2 = float(input("Base, second value: "))
a = ((b1 + b2) / 2) * h
print("Expected Output:", a)

# exercise 3 ----------------------------------------------------------------
n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
area = (n * s * s) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", area)

# exercise 4 ----------------------------------------------------------------
b = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
ar= b * height
print("Expected Output:", ar)