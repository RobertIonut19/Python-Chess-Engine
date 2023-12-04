from itertools import combinations
def set_operations(*args):
    results = {}

    set_pairs = list(combinations(args, 2))

    for set1, set2 in set_pairs:
        union_result = set1 | set2
        intersection_result = set1 & set2
        difference_result1 = set1 - set2
        difference_result2 = set2 - set1

        results[f"{set1} | {set2}"] = union_result
        results[f"{set1} & {set2}"] = intersection_result
        results[f"{set1} - {set2}"] = difference_result1
        results[f"{set2} - {set1}"] = difference_result2

    return results

def main():
    set1 = {1, 2, 3, 4}
    set2 = {3, 4, 5, 6}
    set3 = {1, 2, 3, 4, 5, 6, 7, 8}

    result = set_operations(set1, set2, set3)

    for key, value in result.items():
        print(f"{key} = {value}")


main()