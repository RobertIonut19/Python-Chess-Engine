def set_operations(a, b):
    intersection = set(a) & set(b)
    union = set(a) | set(b)
    a_difference = set(a) - set(b)
    b_difference = set(b) - set(a)

    return [intersection, union, a_difference, b_difference]

def main():
    list_a = [1, 2, 3, 4]
    list_b = [3, 4, 5, 6]

    result = set_operations(list_a, list_b)
    for elem in result:
        print(elem)
main()