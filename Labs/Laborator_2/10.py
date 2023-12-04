def tupleList(*args):
    max_len = max(len(lst) for lst in args)
    result = []

    for i in range(max_len):
        result.append(tuple(lst[i] if i < len(lst) else None for lst in args))

    return result

def main():
    list1 = [1, 2, 3]
    list2 = [5, 6, 7]
    list3 = ["a", "b", "c", "d"]

    print(tupleList(list1, list2, list3))

main()