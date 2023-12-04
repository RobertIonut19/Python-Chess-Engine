class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

class Car(Vehicle):
    def calculate_mileage(self):
        return "Mileage: 5.6L/100km"

class Motorcycle(Vehicle):
    def calculate_mileage(self):
        return "Mileage: 3.2L/100km"

class Truck(Vehicle):

    def __init__(self, make, model, year, towing_capacity):
        super().__init__(make, model, year)
        self.towing_capacity = towing_capacity
    def calculate_mileage(self):
        return "Mileage: 7.8L/100km"

    def calculate_towing_capacity(self):
        return f"Towing capacity: {self.towing_capacity}kg"


def vehicle_exercise():
    car = Car('Toyota', 'Camry', 2018)
    print(car.calculate_mileage())
    motorcycle = Motorcycle('Honda', 'CBR', 2019)
    print(motorcycle.calculate_mileage())
    truck = Truck('Isuzu', 'NQR', 2015, 5000)
    print(truck.calculate_mileage())
    print(truck.calculate_towing_capacity())


vehicle_exercise()