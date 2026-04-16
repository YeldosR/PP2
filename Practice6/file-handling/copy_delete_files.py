import shutil
import os

source = "sample.txt"
backup = "backup.txt"


if os.path.exists(source):
    shutil.copy(source, backup)
    print("File copied.")


if os.path.exists(backup):
    os.remove(backup)
    print("Backup file deleted.")
else:
    print("No backup file to delete.")