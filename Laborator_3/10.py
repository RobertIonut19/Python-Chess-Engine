def loop(mapping):
    keys = set()
    result = [mapping['start']]
    while True:
        key = result[-1]

        if key in keys:
            return result[:-1]
        else:
            keys.add(key)
            result.append(mapping[key])

def main():
    print(loop({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'}))

main()
