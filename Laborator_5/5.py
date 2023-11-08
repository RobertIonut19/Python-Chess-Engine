class Animal:
    def __init__(self, name):
        self.name = name
    def move(self):
        print("move")
    def speak(self):
        pass


class Mammal(Animal):
    def speak(self):
        print("bark/ meow/ etc")

    def move(self):
        print("run")


class Fish(Animal):
    def speak(self):
        print("blub")

    def move(self):
        print("swim")


class Bird(Animal):
    def speak(self):
        print("tweet")

    def move(self):
        print("fly")


def animal_exercise():
    animals = [Mammal("Rover"), Fish("Goldie"), Bird("Tweetie")]
    for animal in animals:
        print(animal.name)
        animal.speak()
        animal.move()
        print()


animal_exercise()