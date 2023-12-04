def intersetion(list1, list2):
    result = [element for element in list1 if element in list2]
    return result

def reunion(list1, list2):
    result = [element for element in list1 if element not in list2]
    result.extend(list2)
    return result

def aMinusB(list1, list2):
    result = [element for element in list1 if element not in list2]
    return result

def bMinusA(list1, list2):
    result = [element for element in list2 if element not in list1]
    return result

def main():
    list1 = [int(i) for i in input("Enter first list: ").split()]
    list2 = [int(i) for i in input("Enter second list: ").split()]

    print("Intersection: ", intersetion(list1, list2))
    print("Reunion: ", reunion(list1, list2))
    print("A - B: ", aMinusB(list1, list2))
    print("B - A: ", bMinusA(list1, list2))

main()