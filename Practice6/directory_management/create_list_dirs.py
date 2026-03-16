import os
path = "KBTU/pp2/practice_6"
os.makedirs(path, exist_ok=True)
print(f"Directories created: {path}")
if os.path.exists("KBTU"):
    print("\nContents of 'KBTU':")
    for i in os.listdir("KBTU"):
        print(i)
else:
    print("KBTU does not exist.")