def vowelsCount(s):
    count = 0
    for i in s:
        if i in 'aeiouAEIOU':
            count += 1
    return count

def main():
    s = input("Enter a string: ")
    print(vowelsCount(s))

main()