require 'sqlite3'
require 'students_list_yaml'
require_relative 'apploger'

class UniqueStudentError < ArgumentError; end

class StudentListDBSqlite
  def initialize(db_path: 'db/sqlite3_student.db', log_path: nil)
    @logger = log_path ? AppLogger.build(log_path) : nil

    @db = SQLite3::Database.new(db_path)
    @db.results_as_hash = true

    @logger&.info("SQLite подключение установлено")
    rescue => e
      @logger&.error("Ошибка подключения к БД: #{e.message}")
    raise
    
  end

  def get_student_by_id(id)
    @logger&.info("Поиск студента по id=#{id}")

    row = @db.get_first_row("SELECT * FROM student WHERE id = ?", id)
    return nil unless row

    student = Student.from_h(id: row['id'], hash: symbolize(row))

    @logger&.debug("Найден студент: #{student.to_h}")
    student
    rescue => e
      @logger&.error("Ошибка get_student_by_id: #{e.message}")
    raise
  end

  def get_k_n_student_short_list(k, n)
    @logger&.info("Получение списка студентов k=#{k}, n=#{n}")

    offset = (n - 1) * k
    rows = @db.execute('SELECT * FROM student ORDER BY id LIMIT ? OFFSET ?', [k, offset])   

    students = rows.map do |row|
      Student.from_h(id: row['id'], hash: symbolize(row))
    end

    DataListStudentShort.new(students)

    rescue => e
      @logger&.error("Ошибка get_k_n_student_short_list: #{e.message}")
    raise
  end

  def add_student(student)
    @logger&.info("Добавление студента: #{student.short_info}")

    hash = student.to_h
    unique(hash)

    @db.execute(
      <<~SQL,
        INSERT INTO student
        (last_name, first_name, patronymic, telegram, email, phone, git)
        VALUES (?, ?, ?, ?, ?, ?, ?)
      SQL
      hash.values_at(:last_name, :first_name, :patronymic, :telegram, :email, :phone, :git)
    )

    @logger&.debug("Студент успешно добавлен")
    rescue => e
      @logger&.error("Ошибка в add_student: #{e.message}")
    raise
  end

  def replace_student_by_id(id, student)
    @logger&.info("Обновление студента id=#{id}")

    hash = student.to_h
    unique(hash, id)

    exists = @db.get_first_value("SELECT 1 FROM student WHERE id = ?", id)
    raise "Студент с id=#{id} не найден" unless exists

    sql = <<~SQL
      UPDATE student SET
          last_name = ?,
          first_name = ?,
          patronymic = ?,
          telegram = ?,
          email = ?,
          phone = ?,
          git = ?
      WHERE id = ?
    SQL

    params = hash.values_at(
        :last_name, :first_name, :patronymic,
        :telegram, :email, :phone, :git
    ) + [id]
    
    @db.execute(sql, params)

    @logger&.debug("Студент id=#{id} обновлён")
    rescue => e
      @logger&.error("Ошибка в replace_student_by_id: #{e.message}")
    raise
  end

  def delete_student_by_id(id)
    @logger&.info("Удаление студента id=#{id}")

    @db.execute("DELETE FROM student WHERE id = ?", id)

    @logger&.debug("Студент id=#{id} удалён")
    rescue => e
      @logger&.error("Ошибка в delete_student_by_id: #{e.message}")
    raise
  end

  def get_student_short_count
    @db.get_first_value("SELECT COUNT(*) FROM student")
  end

  private
  def unique(hash, ignore_id = nil)
    if ignore_id
      rows = @db.execute("SELECT * FROM student WHERE id != ?", ignore_id)
    else
      rows = @db.execute("SELECT * FROM student")
    end

    new_student = Student.from_h(id: ignore_id, hash: hash)

    rows.each do |row|
      existing_student = Student.from_h(id: row['id'], hash: row.transform_keys(&:to_sym))
      raise UniqueStudentError, "Ошибка уникальности студента" if existing_student == new_student
    end
  end

  def symbolize(row)
    row.transform_keys(&:to_sym)
  end
end

# ex = StudentListDBSqlite.new(db_path: 'db/sqlite3_student.db', log_path: 'db/logs/sqlite_student.log')

# puts "=== ДОБАВЛЕНИЕ СТУДЕНТОВ ==="

# s1 = Student.new(
#   last_name: "Галустянов",
#   first_name: "Галустян",
#   patronymic: "Галустянович"
# )

# ex.add_student(s1)
# puts "Студент добавлен\n\n"

# puts "=== ДОБАВЛЕНИЕ СТУДЕНТОВ ==="

# s2 = Student.new(
#   last_name: "Грибов",
#   first_name: "Гриб",
#   phone: "+79990001111"
# )

# ex.add_student(s2)
# puts "Студент добавлен\n\n"


# puts "=== ПОДСЧЁТ СТУДЕНТОВ ==="
# puts "Всего студентов: #{ex.get_student_short_count}\n\n"


# puts "=== ПОЛУЧЕНИЕ ПО ID ==="
# student = ex.get_student_by_id(1)
# puts student
# puts


# puts "=== ПОЛУЧЕНИЕ K-N СПИСКА ==="
# short_list = ex.get_k_n_student_short_list(5, 1)
# puts short_list
# puts

# puts "=== ОБНОВЛЕНИЕ СТУДЕНТА ==="

# updated = Student.new(
#   last_name: "Ахвердян",
#   first_name: "Гурген",
#   patronymic: "Артурович",
#   phone: "+79530753916",
#   git: "https://github.com/gurik"
# )

# ex.replace_student_by_id(3, updated)
# puts "Студент обновлён\n\n"


# puts "=== УДАЛЕНИЕ СТУДЕНТА ==="
# ex.delete_student_by_id(4)
# puts "Студент удалён\n\n"


# puts "=== ИТОГОВОЕ КОЛИЧЕСТВО ==="
# puts "Всего студентов: #{ex.get_student_short_count}"