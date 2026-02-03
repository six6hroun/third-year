def is_global_max?(array, index)
  if index < 0 || index >= array.length
    raise ArgumentError, "Индекс не входит/вышел за пределы массива"
  elsif array[index] == array.max
    true
  else
    false
  end
end

def local_minimum?(array, index)
  return false if index < 0 || index >= array.length
  return true if array.length == 1
  
  if index == 0
    array[0] <= array[1]
  elsif index == array.length - 1
    array[-1] <= array[-2]
  else
    array[index] <= array[index - 1] && array[index] <= array[index + 1]
  end
end

def shift_left_1(array)
  array.rotate(1)
end

def even_odd_index_elements(array)
  a1 = array.select { |n| n.odd? }
  a2 = array.select { |n| n.even? }
  a1 + a2
end

def frequency_lists(array)
  l1 = array.uniq
  l2 = l1.map { |n| array.count(n) }
  [l1, l2]
end