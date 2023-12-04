def badGame(matrix):
    result = []
    maxPerLine = matrix[0][:]  # Initialize with the first row

    for i in range(1, len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] <= maxPerLine[j]:
                result.append((i, j))
            else:
                maxPerLine[j] = matrix[i][j]

    return result

def main():
    print(badGame(
        [[1, 2, 3, 2, 1, 1],
        [2, 4, 4, 3, 7, 2],
        [5, 5, 2, 5, 6, 4],
        [6, 6, 7, 6, 7, 5]]))

main()
