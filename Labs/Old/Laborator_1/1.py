import sys
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def read_file(filepath):
    try:
        with open(filepath,'r',encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("hatz")
        sys.exit(1)

def main():
    n1 = int(input("Enter first number: "))
    n2 = int(input("Enter second number: "))

    gcd_num = gcd(n1, n2)

    print(gcd_num)

    content = read_file('2.py')
    print(content)

main()