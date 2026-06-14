def sortpaste(array):
    n = len(array)
    for i in range(1,n):
        k = array[i]
        j = i - 1

        while j >= 0 and array[j] > k:
            array[j + 1] = array[j]
            j -= 1

        array[j + 1] = k
    return array

a = [1,3,4,2,7,10,22]
print (sortpaste(a))