require_relative "student"
require 'students_list_yaml'
class StudentTree
    include Enumerable
    attr_reader :root, :left, :right

    def initialize(root = nil, left = nil, right = nil)
      @root = root
      @left = left
      @right = right
    end

    def append(other)
      if @root.nil?
        @root = other
      else
        case other < @root
        when true
          if @left.nil?
             @left = StudentTree.new(other)
          else
            @left.append(other)
          end
          when false
            if @right.nil?
                @right = StudentTree.new(other)
            else
                @right.append(other)
            end 
        end
      end
    end

    def remove(other)
      case compare(other, @root)
        when -1
          @left = @left&.remove(other)
        when 1
          @right = @right&.remove(other)
        when 0
          return @right if @left.nil?
          return @left if @right.nil?

          min_value = @right.min
          @root = min_value
          @right = @right.remove(min_value)
      end
      self
    end

    def find(&block)
      return @root if !@root.nil? && block.call(@root)
      
      left_result = @left&.find(&block)
      return left_result unless left_result.nil?
      
      @right&.find(&block)
    end

    def each(&block)
      @left&.each(&block)
      block.call(@root) unless @root.nil?
      @right&.each(&block)
    end

    def compare(a, b)
        a <=> b
    end
end

tree = StudentTree.new
students = [
  Student.new(first_name: "Иван", last_name: "Смирнов", patronymic: "Алексеевич", telegram: "@ivan_smirnov", git: "https://github.com/ivan"),
  Student.new(first_name: "Анна", last_name: "Иванова", email: "anna@example.com"),
  Student.new(first_name: "Ольга", last_name: "Борисова", telegram: "@olga_bor", email: "olga@example.com"),
  Student.new(first_name: "Максим", last_name: "Зайцев", git: "https://github.com/max"),
  Student.new(first_name: "Елена", last_name: "Кузнецова", patronymic: "Игоревна", phone: "+79161234567"),
  Student.new(first_name: "Дмитрий", last_name: "Новиков", telegram: "@d_novikov"),
  Student.new(first_name: "Светлана", last_name: "Орлова", patronymic: "Владимировна", email: "svetlana@edu.ru", git: "https://github.com/svetlana"),
  Student.new(first_name: "Алексей", last_name: "Попов", phone: "+79201112233"),
  Student.new(first_name: "Татьяна", last_name: "Романова", email: "tatiana@corp.ru", git: "https://github.com/tatiana"),
  Student.new(first_name: "Сергей", last_name: "Сидоров", patronymic: "Геннадьевич", telegram: "@serg_sid", phone: "+79005556677"),
  Student.new(first_name: "Юлия", last_name: "Тихонова", git: "https://github.com/yulia", email: "yulia@domain.com"),
  Student.new(first_name: "Виктор", last_name: "Уваров", telegram: "@vik_uvarov"),
  Student.new(first_name: "Мария", last_name: "Федорова"),
  Student.new(first_name: "Андрей", last_name: "Харитонов", patronymic: "Николаевич", phone: "+79998887766", git: "https://github.com/andrey"),
  Student.new(first_name: "Людмила", last_name: "Цветкова", telegram: "@lyuda", email: "lyuda@mail.ru"),
  Student.new(first_name: "Егор", last_name: "Чистяков", patronymic: "Петрович"),
  Student.new(first_name: "Наталья", last_name: "Шестакова", git: "https://github.com/natalia"),
  Student.new(first_name: "Борис", last_name: "Щербаков", email: "boris@example.org"),
  Student.new(first_name: "Ирина", last_name: "Эренбург", patronymic: "Андреевна", telegram: "@irina_eren", phone: "+79209998877", git: "https://github.com/irina"),
]

students.each { |s| tree.append(s) }
ex1 = Student.new(first_name: "Яванннннннннн", last_name: "Ямирнов", patronymic: "Ялексеевич", telegram: "@ivan_smirnov", git: "https://github.com/ivan")
tree.append(ex1)
puts tree.to_a
puts
tree.remove(ex1)
puts tree.to_a
puts
puts tree.find{|s| s.first_name == 'Яванннннннннн'}
puts
puts tree.select {|x| x.last_name == "Чистяков"}