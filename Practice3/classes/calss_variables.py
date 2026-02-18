class Student:
    school = "NIS"

    def __init__(self, name):
        self.name = name

s1 = Student("Rustem")
s2 = Student("Aruzhan")

print(s1.school, s2.school)
