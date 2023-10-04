def extractFirstNumber(text):
    num = ""

    for char in text:
        if char.isdigit():
            num += char
        elif num:
            break

    if num:
        return int(num)
    else:
        return "No number found"

def main():
    string = input("Enter a string: ")

    print(extractFirstNumber(string))

main()