class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display(self):
        print("Name: ", self.name, ", Salary: ", self.salary)

class Manager(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, salary)
        self.department = department

    def display(self):
        super().display()
        print("Department: ", self.department)

class Engineer(Employee):
    def __init__(self, name, salary, project):
        super().__init__(name, salary)
        self.project = project

    def display(self):
        super().display()
        print("Project: ", self.project)


class Salesperson(Employee):
    def __init__(self, name, salary, region):
        super().__init__(name, salary)
        self.region = region

    def display(self):
        super().display()
        print("Region: ", self.region)


def employee_exercise():
    employees = [Manager("John", 50000, "Sales"), Engineer("Jane", 60000, "Website"), Salesperson("Bob", 40000, "Europe")]
    for employee in employees:
        employee.display()


employee_exercise()