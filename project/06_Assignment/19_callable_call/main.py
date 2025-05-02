class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self , x):
        return self.factor *  x
    
multiplier = Multiplier(5)

print(f"Is multiplier callable? {callable(multiplier)}")

result = multiplier(10)
print(f"Result of multiplier(10): {result}")