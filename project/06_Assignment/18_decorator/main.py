class Product:
    def __init__(self , name , price):
        self.name = name 
        self._price = price
    @property 
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value
        
    @price.deleter
    def price(self):
        del self._price
        
product = Product("Laptop", 1000)

print(f"Price: {product.price}")

product.price = 1200
print(f"Updated Price: {product.price}")

del product.price
try:
    print(product.price)
except AttributeError as e:
    print("Error: ", e)

try:
    product.price = -50
except ValueError as e:
    print("Error: ", e)

