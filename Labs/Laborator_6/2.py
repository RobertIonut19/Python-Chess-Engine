import os

def rename_files(directory):
    if not os.path.exists(directory):
        print("Directory %s does not exist" % directory)
        return None
    if not os.path.isdir(directory):
        print("%s is not a directory" % directory)
        return None

    try:
        files = os.listdir(directory)

        for i, filename in enumerate(files, start=1):
            new_filename = f"file_{i}.{filename.split('.')[-1]}"

            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)

            os.rename(old_path, new_path)
            print(f"Renamed file {filename} to {new_filename}")

    except Exception as e:
        print(f"Error: {e}")

def main():
    rename_files("/Users/robertrascanu/Documents/Facultate/PY/test")

main()