def FibonacciSequence(n):
    term1 = 1
    term2 = 1
    if n == 1:
        return term1
    else:
        result = [term1, term2]
        for i in range(2, n):
            result.append(result[i - 1] + result[i - 2])
        return result

def main():
    n = int(input("Enter number of Fibonacci numbers: "))
    print(FibonacciSequence(n))

main()