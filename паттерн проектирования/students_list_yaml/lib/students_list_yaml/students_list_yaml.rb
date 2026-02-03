require 'yaml'
require_relative "student"
require_relative "data_list"
require_relative "student_short"
require_relative "data_list_student_short"


class DuplicateStudentError < ArgumentError; end

class StudentsListYAML
  def initialize(file)
    @file = file
    @students = []
    read_file
  end

  def read_file
    yaml_ex = File.read(@file)
    data = YAML.safe_load(yaml_ex, permitted_classes: [Symbol], symbolize_names: true)
    @students = data.map { |h| Student.from_h(id: h[:id], hash: h) }
  end

  def write_file
    data = @students.map { |s| s.to_h }
    File.write(@file, YAML.dump(data))
  end

  def get_student_by_id(id)
    @students.find { |s| s.id == id }
  end

  def get_k_n_student_short_list(k, n, data_list = nil)
    start_index = (n - 1) * k
    slice = @students[start_index, k] || []

    student_shorts = slice.map do |s|
      StudentShort.new(id: s.id, last_name_initials: s.last_name_initials, contact: s.contact, git: s.git)
    end

    if data_list
      data_list.data = student_shorts
      data_list
    else
      DataListStudentShort.new(student_shorts)
    end
  end

  def sort_by_surname_initials!
    @students.sort_by! { |s| s.last_name_initials }
  end

  def unique(student)
    raise DuplicateStudentError, "Студент с таким контактом уже существует" unless !@students.any? { |s| s == student }
  end

  def add_student(student)
    unique(student)
    max_id = @students.map { |s| s.id }.max || 0
    value = student.to_h
    @students << Student.from_h(id: max_id + 1, hash: value)
  end

  def replace_student_by_id(id, new_student)
    unique(new_student)
    index = @students.index { |s| s.id == id }
    return unless index
    @students[index] = Student.from_h(id: id, hash: new_student.to_h)
  end

  def delete_student_by_id(id)
    @students.reject! { |s| s.id == id }
  end

  def get_student_short_count
    @students.size
  end
end