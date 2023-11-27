from calculator import operations

def main():
    print(f"Addition: {operations.add(1, 2)}")
    print(f"Subtraction: {operations.subtract(1, 2)}")
    print(f"Multiplication: {operations.multiply(1, 2)}")
    print(f"Division: {operations.divide(1, 2)}")

    print(f"Division: {operations.divide(1, 0)}")

    print(f"Addition: {operations.add(1.56, 2.44)}")
    print(f"Subtraction: {operations.subtract(1.56, 2.34)}")
    print(f"Multiplication: {operations.multiply(1.56, 2.34)}")
    print(f"Division: {operations.divide(1.56, 2.34)}")

    print(f"Division: {operations.divide(1.56, 0)}")

main()