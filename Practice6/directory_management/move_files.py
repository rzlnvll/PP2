import os
import shutil
os.makedirs("Kbtu/pp2/practice6", exist_ok=True)

if os.path.exists("sample.txt"):
    shutil.copy("sample.txt", "Kbtu/pp2/sample.txt")
    shutil.move(
        "Kbtu/pp2/sample.txt",
        "Kbtu/pp2/practice6/sample.txt"
    )
    print("File copied and moved")
else:
    print("sample.txt not found")