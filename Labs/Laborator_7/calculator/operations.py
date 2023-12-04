def add(x, y):
    """Addition"""
    return x + y

def subtract(x, y):
    """Subtraction"""
    return x - y

def multiply(x, y):
    """Multiplication"""
    return x * y

def divide(x, y):
    """Division"""
    try:
        return x / y
    except ZeroDivisionError:
        return "Division by zero is not allowed"
