def sortsel(array):
    n = len(array)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if array[j] < array[min_index]:
                min_index = j

        array[i], array[min_index] = array[min_index], array[i]

    return array

a = [1,3,2,4,1,20,8,35,6]
print (sortsel(a))