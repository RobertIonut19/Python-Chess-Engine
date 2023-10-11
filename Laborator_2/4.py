def compose(notes, moves, start):
    result = [notes[start]]
    for move in moves:
        new_index = start + move

        if(new_index >= len(notes)):
            new_index = new_index % len(notes)
        elif(new_index < 0):
            new_index = new_index + len(notes)

        result.append(notes[new_index])
        start = new_index

    return result


def main():
    print(compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2))

main()

