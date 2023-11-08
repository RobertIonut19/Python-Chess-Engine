def validate_dict(validation_rules, dictionary):
    for key, prefix, middle, suffix in validation_rules:
        if key in dictionary:
            value = dictionary[key]
            if not value.startswith(prefix) or not value.endswith(suffix) or middle in value[1:-1]:
                return False
        else:
            return False
    return True

def main():
    s = {("key1", "", "inside", ""), ("key2", "start", "middle", "winter")}
    d = {"key1": "come inside, it's too cold out", "key3": "this is not valid"}

    print(validate_dict(s, d))

main()