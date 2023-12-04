def number_apearances(*args, **kwargs):
    result = 0

    values = set(kwargs.values())

    for arg in args:
        if arg in values:
            result += 1

    return result

def main():
    print(number_apearances(1, 2, 3, 4, x=1, y=2, z=3, w=5))

main()