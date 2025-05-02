class Employee:
    def __init__(self , name):
        self.name = name
        
    def get_details(self):
        return f"Employee :{self.name}"
    
class Department:
    def __init__(self, name , employee):
        self.name = name
        self.employee = employee
    def show_employee(self):
        return f"{self.name} Department - {self.employee.get_details()}"
    
emp = Employee("Areeba Irfan")
dept = Department("IT", emp)
print(dept.show_employee())
        