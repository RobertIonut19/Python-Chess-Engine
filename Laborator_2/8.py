def ascii(x = 1, list=[], flag = True):
    result = []
    i = 0
    for string in list:
        char_list = []
        for char in string:
            if flag and (ord(char) % x == 0):
                char_list.append(char)
            elif flag == False and (ord(char) % x != 0):
                char_list.append(char)
        if char_list:
            result.append("".join(char_list))
    return result

def main():
    print(ascii(x = 2, list=["test", "hello", "lab002"], flag = False))

main()

print(ord("e"))
print(ord("s"))
print(ord("o"))
print(ord("a"))
print()
print(ord("l"))
print(ord("h"))
print(ord("0"))
print(ord("2"))
print(ord("t"))