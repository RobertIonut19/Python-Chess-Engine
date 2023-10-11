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

def listPalindrome(list):
    count = 0
    greatestPalindrome = 0

    for i in range(len(list)):
        if isPalindrome(list[i]):
            count += 1
            if list[i] > greatestPalindrome:
                greatestPalindrome = list[i]

    result = (count, greatestPalindrome)

    return result

def main():
    list = [121, 123, 1331, 12321, 123321]
    result = listPalindrome(list)
    print(result)

main()