import sys
import os

def read_directory():
    directory = sys.argv[1]

    try:
        if not os.path.exists(directory):
            raise Exception(f"Directory {directory} doesn't exist...")
        if not os.path.isdir(directory):
            raise Exception(f"{directory} is not a directory...")
        if not os.listdir(directory):
            raise Exception(f"{directory} is empty...")

    except FileNotFoundError:
        print("Directory given as argument does not exist")
    except PermissionError:
        print("Not allowed to open directory")
    except Exception as e:
        print(e)

    return directory


def number_of_files_by_extension(directory):

    try:
        extensions = {}
        for file_name in os.listdir(directory):
            _, extension = os.path.splitext(file_name)

            extensions[extension] = extensions.get(extension, 0) + 1

        print(f"Number of files by extension in {directory}:")
        for extension, count in extensions.items():
            print(f"{extension}: {count}")
    except Exception as e:
        print(e)


def main():
    if len(sys.argv) != 2:
        print("Usage: python 4.py <directory>")
        return None

    directory = read_directory()

    number_of_files_by_extension(directory)

main()
