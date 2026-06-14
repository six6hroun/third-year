def scal (vec1,vec2):
    result = 0
    for i in range(len(vec1)):
        result += vec1[i] * vec2[i]
    return result

vec1 = [1,2,3]
vec2 = [4,5,6]
print(scal(vec1,vec2))