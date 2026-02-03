class ArrayProcessor
  def initialize (array)
    @array = array
  end

  def to_a
    @array.dup
  end

  def count(&block)
    k = 0
    i = 0
    while i < @array.length
      k += 1 if block.call(@array[i])
      i += 1
    end
    k
  end

  def group_by(&block)
    result = {}
    i = 0
    while i < @array.length
      key = block.call(@array[i])
      result[key] = result[key] || []
      result[key] << @array[i]
      i += 1
    end
    result
  end

  def partition(&block)
    k1 = []
    k2 = []
    i = 0
    while i < @array.length
      if block.call(@array[i])
        k1 << @array[i]
      else
        k2 << @array[i]
      end
      i += 1
    end
    [k1, k2]
  end

  def take_while(&block)
    k = []
    i = 0
    while i < @array.length && block.call(@array[i])
      k << @array[i]
      i += 1
    end
    k
  end

  def min(&block)
    return false if @array.empty?
    min_value = @array[0]
    i = 1
    while i < @array.length
      if block.call(@array[i], min_value) == -1
        min_value = @array[i]
      end
      i += 1
    end
    min_value
  end

  def filter_map(&block)
    k = []
    i = 0
    while i < @array.length
      value = block.call(@array[i])
      k << value if value
      i += 1
    end
    k
  end
end