class Calculator:
    def calc(self, a, b):
        return a + b
class SmartCalculator(Calculator):
    def calc(self, a, b):
        # The child's calc function overrides the inheritance of the parent's calc function.
        return a * b


c1 = Calculator()
c2 = SmartCalculator()

print(c1.calc(2, 3))  # 5
print(c2.calc(2, 3))  # 6