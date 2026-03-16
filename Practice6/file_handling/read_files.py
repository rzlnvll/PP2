# Read and print file contents
with open("sample.txt", "r") as file:
    text = file.read()
    print("File:")
    print(text)