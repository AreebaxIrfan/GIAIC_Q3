class Car:
    def __init__(self, brand):
        self.brand = brand
        
    def start(self):
        print(f"The {self.brand} car is starting.")

car = Car("Toyota")
print(car.brand)
car.start()