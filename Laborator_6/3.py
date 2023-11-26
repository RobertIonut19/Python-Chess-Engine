import os
import sys

def read_directory():
    directory = sys.argv[1]
    try:
        if not os.path.exists(directory):
            raise Exception("Directory %s does not exist" % directory)
        if not os.path.isdir(directory):
            raise Exception("%s is not a directory" % directory)
    except FileNotFoundError:
        print("Directory %s does not exist" % directory)
        return None
    except PermissionError:
        print("You do not have permission to access directory %s" % directory)
        return None
    except Exception as e:
        print(e)
        return None

    return directory

def calculate_file_size(filename):
    try:
        if not os.path.exists(filename):
            raise Exception("File %s does not exist" % filename)
        if not os.path.isfile(filename):
            raise Exception("%s is not a file" % filename)
    except:
        print("Could not open file %s" % filename)
        return None

    return os.path.getsize(filename)

def calculate_total_size(directory):
    total_size = 0
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            total_size += calculate_file_size(os.path.join(root, filename))

    return total_size

def main():

    if len(sys.argv) != 2:
        print("Usage: python 3.py <directory>")
        return None

    directory = read_directory()
    if directory is None:
        return None

    total_size = calculate_total_size(directory)
    print("Total size of directory %s is %d bytes" % (directory, total_size))

main()