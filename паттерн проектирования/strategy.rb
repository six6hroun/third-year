class Ex
attr_accessor :num1, :num2

  def initialize(num1, num2)
    @num1 = num1
    @num2 = num2
  end

  def number
    @num1 + @num2
  end
end

class Ex2
attr_accessor :num1, :num2

  def initialize(num1, num2)
    @num1 = num1
    @num2 = num2
  end

  def number
    @num1 * @num2
  end
end

class Itog
  attr_accessor :strategy
  def initialize(ex)
    @strategy = ex
  end

  def number
    @strategy.number
  end
end

one = Ex.new(3,5)
two = Ex2.new(3,5)
three = Itog.new(two)
puts three.number