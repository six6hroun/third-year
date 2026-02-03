require 'json'
require 'students_list_yaml'

# Исключение, возникающее при попытке добавить дубликат студента
class DuplicateStudentError < ArgumentError; end

# Класс для работы со списком студентов, хранящимся в JSON-файле
class StudentsListJSON

  # Инициализация списка студентов
  # @param file [String] путь к JSON-файлу со студентами
  def initialize(file)
    @file = file
    @students = []
    read_file
  end

  # Считывает список студентов из JSON-файла
  # @return [Array<Student>] массив студентов
  def read_file
    json = File.read(@file)
    data = JSON.parse(json, symbolize_names: true)
    @students = data.map { |h| Student.from_h(id: h[:id], hash: h) }
  end

  # Записывает текущий список студентов в JSON-файл
  # @return [void]
  def write_file
    data = @students.map(&:to_h)
    File.write(@file, JSON.pretty_generate(data))
  end

  # Возвращает студента по его идентификатору
  # @param id [Integer] идентификатор студента
  # @return [Student, nil] найденный студент или nil
  def get_student_by_id(id)
    @students.find { |s| s.id == id }
  end

  # Возвращает список краткой информации о студентах
  # @param k [Integer] количество студентов на странице
  # @param n [Integer] номер страницы
  # @param data_list [DataListStudentShort, nil] объект для заполнения
  # @return [DataListStudentShort]
  def get_k_n_student_short_list(k, n, data_list = nil)
    start_index = (n - 1) * k
    slice = @students[start_index, k] || []

    student_shorts = slice.map do |s|
      StudentShort.new(
        id: s.id,
        last_name_initials: s.last_name_initials,
        contact: s.contact,
        git: s.git
      )
    end

    if data_list
      data_list.data = student_shorts
      data_list
    else
      DataListStudentShort.new(student_shorts)
    end
  end

  # Сортирует список студентов по фамилии и инициалам
  # @return [void]
  def sort_by_surname_initials!
    @students.sort_by!(&:last_name_initials)
  end

  # Проверяет уникальность студента по контактным данным
  # @param student [Student] проверяемый студент
  # @param ignore_id [Integer, nil] id студента, который следует игнорировать
  # @raise [DuplicateStudentError] если найден дубликат
  # @return [void]
  def unique(student, ignore_id: nil)
    if @students.any? { |s| s.id != ignore_id && s == student }
      raise DuplicateStudentError, 'Студент с таким контактом уже существует'
    end
  end

  # Добавляет нового студента в список
  # @param student [Student] объект студента
  # @raise [DuplicateStudentError] если студент не уникален
  # @return [void]
  def add_student(student)
    unique(student)
    max_id = @students.map { |s| s.id }.max || 0
    @students << Student.from_h(id: max_id + 1, hash: student.to_h)
  end

  # Заменяет данные студента по id
  # @param id [Integer] идентификатор студента
  # @param new_student [Student] новые данные студента
  # @raise [DuplicateStudentError] если нарушена уникальность
  # @return [void]
  def replace_student_by_id(id, new_student)
    unique(new_student, ignore_id: id)
    index = @students.index { |s| s.id == id }
    return unless index
    @students[index] = Student.from_h(id: id, hash: new_student.to_h)
  end

  # Удаляет студента по id
  # @param id [Integer] идентификатор студента
  # @return [void]
  def delete_student_by_id(id)
    @students.reject! { |s| s.id == id }
  end

  # Возвращает количество студентов
  # @return [Integer]
  def get_student_short_count
    @students.size
  end
end