class Employee:
    def __init__(self, name, salary, ssn):
        self.name = name
        self._salary = salary
        self.__ssn = ssn
        
    def display(self):
        print(f"Name: {self.name}, Salary: {self._salary}, SSN: {self.__ssn}")

emp = Employee('Areeba Irfan', 50000, "123-45-6789")

print("Public variables (name):" , emp.name)

print("Protected variables (salary):", emp._salary)

try:
    print("Private varaible(__ssn):", emp.__ssn)
except AttributeError as e:
    print('Error accessing private varaible(__ssn):', e)

print("Private variable via name mangling (_Employee__ssn):", emp._Employee__ssn)  # Works

emp.display()