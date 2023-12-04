def group_by_rhyme(word_list):
    result = []
    for word in word_list:
        flag = False
        for result_word in result:
            if word[-2:] == result_word[0][-2:]:
                result_word.append(word)
                flag = True
                break
        if flag == False:
            result.append([word])
    return result

def main():
    print(group_by_rhyme(['ana', 'banana', 'carte', 'arme', 'parte']))

main()