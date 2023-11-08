def dictionary_compare(dict1, dict2):
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        if set(dict1.keys()) != set(dict2.keys()):
            return False

        for key in dict1:
            if not dictionary_compare(dict1[key], dict2[key]):
                return False

        return True

    else:
        return  dict1 == dict2



def main():
    dict1 = {'a': 1, 'b': [2, 3, {'x': 4}], 'c': {'y': 5}}
    dict2 = {'a': 1, 'b': [2, 3, {'x': 3}], 'c': {'y': 5}}
    print(dictionary_compare(dict1, dict2))

main()