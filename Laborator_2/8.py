def ascii(x=1, input_list=[], flag=True):
    result = []
    for string in input_list:
        char_list = []
        for char in string:
            if (flag and ord(char) % x == 0) or (not flag and ord(char) % x != 0):
                char_list.append(char)
        if char_list:
            result.append(char_list)
    return result

def main():
    print(ascii(x = 2, input_list=["test", "hello", "lab002"], flag = False))

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