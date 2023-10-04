def subStringCount(str1, str2):
    count = 0
    for i in range(len(str1)):
        if str1[i:].startswith(str2):
            count += 1
    return count

def main():
    str1 = input("Enter first string: ")
    str2 = input("Enter second string: ")

    print(subStringCount(str1, str2))

main()