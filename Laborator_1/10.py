def numberOfWord(string):
    return len(string.split(" "))

def main():
    s = input("Enter a string: ")
    print(numberOfWord(s))

main()