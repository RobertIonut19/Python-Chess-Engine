def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def main():
    n1 = int(input("Enter first number: "))
    n2 = int(input("Enter second number: "))

    gcd_num = gcd(n1, n2)

    print(gcd_num)


main()