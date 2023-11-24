import os
import PyPDF2
def read_file(filename):
    if not os.path.exists(filename):
        print("File %s does not exist" % filename)
        return None
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        if f is None:
            print("Could not open file %s" % filename)
            return None
        return f.read()

def read_pdf(filename):
    if not os.path.exists(filename):
        print("File %s does not exist" % filename)
        return None

    with open(filename, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
        return text

def write_file(filename, content):
    if not os.path.exists(filename):
        print("File %s does not exist" % filename)
        return None
    with open(filename, 'w') as f:
        if f is None:
            print("Could not open file %s" % filename)
            return None
        f.write(content)


def search_file_recursive(directory, extension):
    if not os.path.exists(directory):
        print("Directory %s does not exist" % directory)
        return None
    if not os.path.isdir(directory):
        print("%s is not a directory" % directory)
        return None
    if not extension.startswith("."):
        extension = "." + extension


    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                #save file content from read_file in a buffer
                if(extension == ".pdf"):
                    buffer = read_pdf(os.path.join(root, filename))
                else:
                    buffer = read_file(os.path.join(root, filename))
                print("File %s, from directory %s, has the following content: " % (filename, root))
                print(buffer)


def main():
    print("Search for files with extension .txt in directory /Users/robertrascanu/Documents/Facultate")
    search_file_recursive("/Users/robertrascanu/Documents/Facultate", ".txt")

main()