def mostCommonLetter(string):
    string = string.lower()
    count = 0
    mostCommon = ""
    for i in string:
        if string.count(i) == count and i not in mostCommon:
            mostCommon += ' ' + i
        elif string.count(i) > count:
            count = string.count(i)
            mostCommon = i

    return mostCommon

def main():
    string = input("Enter a string: ")
    print(mostCommonLetter(string))

main()