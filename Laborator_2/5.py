def replace(matrix):
    for i in range(len(matrix)):
        for j in range(min(i, len(matrix[i]))):
            if i > j:
                matrix[i][j] = 0
    return matrix

def main():
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    replica = replace(matrix)

    for i in range(len(replica)):
        for j in range(len(replica[i])):
            print(replica[i][j], end=" ")
        print()

main()