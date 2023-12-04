def spiralMatrix(mat):
    m = len(mat)
    n = len(mat[0])
    top = 0
    bottom = m-1
    left = 0
    right = n-1
    dir = 0
    while(top <= bottom and left <= right):
        if(dir == 0):
            for i in range(left, right+1):
                print(mat[top][i], end=" ")
            top += 1
        elif(dir == 1):
            for i in range(top, bottom+1):
                print(mat[i][right], end=" ")
            right -= 1
        elif(dir == 2):
            for i in range(right, left-1, -1):
                print(mat[bottom][i], end=" ")
            bottom -= 1
        elif(dir == 3):
            for i in range(bottom, top-1, -1):
                print(mat[i][left], end=" ")
            left += 1
        dir = (dir+1)%4


def main():
    mat = [[1,2,3,4],
           [12,13,14,5],
           [11,16,15,6],
           [10, 9, 8,7]]

    spiralMatrix(mat)

main()