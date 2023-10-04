def numberOfOnes(number):
    count = 0
    while number > 0:
        if number % 2 == 1:
            count += 1
        number //= 2
    return count

def main():
    number = int(input("Enter a number: "))
    print(numberOfOnes(number))

main()