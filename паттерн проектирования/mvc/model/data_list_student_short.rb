require_relative 'data_list'
require_relative 'student_short'
require_relative 'student'
class DataListStudentShort < DataList

  def add_observer(observer)
    @observers << observer
  end

  def notify_observers
    table = get_data
    column = get_names
    @observers.each do |observer|
      observer.on_data_changed(table, column)
    end
  end

  def get_custom_names
    ["ФИО", "Контакт", "Гит"]
  end

  def get_custom_row(student)
    [student.last_name_initials, student.contact, student.git]
  end
end