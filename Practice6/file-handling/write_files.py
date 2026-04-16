import os

file_path = "sample.txt"


with open(file_path, "w") as f:
    f.write("Hello, this is a sample file.\n")
    f.write("Python file handling practice.\n")

print("File created and written.")


with open(file_path, "a") as f:
    f.write("New line added.\n")

print("Line appended.")