def matr(a,b):
    n = len(a)
    result = []
    for i in range(n):
        result.append([0] * n)

    for i in range(n):
        for j in range(n):
            for l in range(n):
                result[i][j] += a[i][l] * b[l][j]

    return result

a = [[1,2,3],
     [4,5,6],
     [7,8,9]]
b = [[5,6,7],
     [8,9,4],
     [3,5,3]]

print (matr(a,b))