import os


os.makedirs("test_dir/sub_dir", exist_ok=True)
print("Directories created.")


for root, dirs, files in os.walk("."):
    print("\nCurrent directory:", root)
    print("Folders:", dirs)
    print("Files:", files)


print("\n.txt files:")
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".txt"):
            print(os.path.join(root, file))#