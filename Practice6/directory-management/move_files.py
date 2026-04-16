import shutil
import os


os.makedirs("destination", exist_ok=True)

source = "sample.txt"
destination = "destination/sample.txt"


if os.path.exists(source):
    shutil.move(source, destination)
    print("File moved.")


if os.path.exists(destination):
    shutil.copy(destination, source)
    print("File copied back.")#