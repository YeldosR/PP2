class Animal:
    def speak(self):
        print("Some sound")

class Cat(Animal):
    def speak(self):
        print("Meow")

a = Animal()
c = Cat()

a.speak()
c.speak()
