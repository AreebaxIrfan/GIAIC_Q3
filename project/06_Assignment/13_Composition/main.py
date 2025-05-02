class Engine:
    def __init__(self, type):
        self.type = type
        
    def start(self):
        return f"{self.type} engine is starting."
    
class Car:
    def __init__(self ,brand, engine):
        self.brand = brand
        self.engine = engine
    
    def start_engine(self):
        return self.engine.start()
    
engine = Engine("V6")
car = Car("Toyota", engine)
print(car.start_engine())  # Output: V6 engine is starting.
        