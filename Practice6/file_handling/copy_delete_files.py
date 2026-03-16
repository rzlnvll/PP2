import os
import shutil
if os.path.exists("sample.txt"):
    shutil.copy("sample.txt", "copy_file.txt")
    shutil.copy("sample.txt", "backup.txt")
    print("sample.txt copied to copy_file.txt and backup.txt")
else:
    print("Error: sample.txt does not exist.")

if os.path.exists("copy_file.txt"):
    os.remove("copy_file.txt")
    print("copy_file.txt deleted")
else:
    print("copy_file.txt not found")
