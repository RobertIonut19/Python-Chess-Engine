def unique_and_duplicate_elements(input_list):
    input_set = set(input_list)
    duplicate_elements = set()
    for i in input_set:
        if input_list.count(i) > 1:
            duplicate_elements.add(i)

    unique_elements = input_set - set(duplicate_elements)

    return (len(unique_elements), len(duplicate_elements))

def main():
    input_list = [1,2,3,4,5,  1,2,3,4,5,  6]
    print(unique_and_duplicate_elements(input_list))

main()