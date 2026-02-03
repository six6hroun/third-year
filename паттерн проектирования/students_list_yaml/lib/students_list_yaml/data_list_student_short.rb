require_relative 'data_list'
require_relative 'student_short'
class DataListStudentShort < DataList
  def get_custom_names
    ["ФИО", "Контакт", "Гит"]
  end

  def get_custom_row(student)
    [student.last_name_initials, student.contact, student.git]
  end
end