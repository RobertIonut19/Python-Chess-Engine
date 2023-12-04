def isPalindrome(num):
    num = str(num)
    if len(num) == 1:
        return True
    elif len(num) == 2:
        if num[0] == num[1]:
            return True
        else:
            return False
    else:
        if num[0] == num[-1]:
            return isPalindrome(num[1:-1])
        else:
            return False

def main():
    num = int(input("Enter a number: "))
    print(isPalindrome(num))

main()