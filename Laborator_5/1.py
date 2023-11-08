import math

class Shape:
    def __init__(self, name):
        self.name = name

    def area(self):
        pass

    def perimeter(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        super().__init__('Circle')
        self.radius = radius


    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        super().__init__('Rectangle')

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

class Triangle(Shape):
    def __init__(self, base, height, side1, side2, side3):
        super().__init__('Triangle')
        self.base = base
        self.height = height
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

    def area(self):
        return 0.5 * self.base * self.height

    def perimeter(self):
        return self.side1 + self.side2 + self.side3
def shape_exercise():
    shapes = [Circle(5), Rectangle(2, 3), Triangle(3, 4, 5, 6, 7)]
    for shape in shapes:
        print(shape.name)
        print(shape.area())
        print(shape.perimeter())

shape_exercise()