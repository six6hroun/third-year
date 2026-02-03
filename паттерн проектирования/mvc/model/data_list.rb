require_relative 'data_table'

class DataList
  def initialize(array)
    self.data = array
    @selected = []
    @observers = []
  end

  def data=(array)
    @array = array.freeze
  end

  def select(number)
    @selected << @array[number]
  end

  def get_selected
    @selected.map { |i| i.id }
  end
  
  def get_names
    ["№ по порядку"] + get_custom_names
  end

  def get_data
    rows = []
    @array.each_with_index do |object, index|
        rows << [index + 1] + get_custom_row(object)
    end
    DataTable.new(rows)
  end

  def clear_selected
    @selected.clear
  end

  def to_s
    get_data.to_s
  end

  protected
  def get_custom_names
    raise NotImplementedError
  end

  def get_custom_row(object)
    raise NotImplementedError
  end
end