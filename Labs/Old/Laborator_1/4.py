def convertUpperCamelCase(s):
    for i in range(len(s)):
        if s[i].isupper():
            s = s[:i] + '_' + s[i].lower() + s[i+1:]
    return s[1:]


def main():
    string = input("Enter UpperCamelCase String: ")

    print(convertUpperCamelCase(string))

main()