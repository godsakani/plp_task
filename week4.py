#Task 1
# File Read & Write Challenge 🖋️: Create a program that reads a file and writes a modified version to a new file.
try:
    with open('input.txt', mode="w") as file:
        data = file.write("File Read & Write Challenge. Create a program that reads a file and writes a modified version to a new file")
    with open('input.txt', mode="r") as file:
        data1 = file.read()
        print(data1)
except FileNotFoundError:
    print("Error writing into the file")
    


#Task 2
# Error Handling Lab 🧪: Ask the user for a filename and handle errors if it doesn’t exist or can’t be read.

file_name = str(input("Please input filename:"))
try:
    with open(f"{file_name}.txt", mode="r") as file:
        print(file.read())
except FileExistsError:
    print("File does not exist or please check file name")