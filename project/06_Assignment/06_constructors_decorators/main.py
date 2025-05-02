class Logger:
    def __init__(self,name):
        self.name = name
        print(f"Logger'{self.name}' created")
        
    def __del__(self):
        print(f"Logger '{self.name}' destroyed")

log1 = Logger("Log1")
log2 = Logger("Log2")
del log1