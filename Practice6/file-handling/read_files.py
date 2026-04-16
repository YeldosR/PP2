file_path = "sample.txt"

try:
    with open(file_path, "r") as f:
        content = f.read()
        print("File content:\n")
        print(content)
except FileNotFoundError:
    print("File not found.")