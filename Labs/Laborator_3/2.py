def dictionary(text):
    char_count = {}

    for char in text:
        #char = char.lower()
        char_count[char] = char_count.get(char, 0) + 1

    return char_count

def main():
    text = "Ana are mere."
    print(dictionary(text))

main()