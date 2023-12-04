def primeCheck(n):
    if n < 2:
        return False
    else:
        for i in range(2, n // 2 + 1):
            if n % i == 0:
                return False
        return True

def listPrimeNumbers(list):
    result = []
    for i in list:
        if primeCheck(i):
            result.append(i)
    return result

def main():
    list = [int(i) for i in input("Enter a list of numbers: ").split()]
    print(listPrimeNumbers(list))

main()