def order(tuple_list):
    def keyFunction(item):
        return item[1][2]
    return sorted(tuple_list, key=keyFunction)

def main():
    tuples = [('abc', 'bcd'), ('abc', 'zza')]
    sorted_tuples = order(tuples)
    print(sorted_tuples)

main()