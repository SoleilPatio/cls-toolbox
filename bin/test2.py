
# read lines from file
import os
PATH=r"C:\"
filename = os.path.join(PATH, "test.txt")

with open(filename, "r") as in_file:
    lines = in_file.readlines()
    lines.split("\n")


if __name__ == "__main__":
    print("Done")