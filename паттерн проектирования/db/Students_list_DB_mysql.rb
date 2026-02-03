require 'mysql2'
require 'students_list_yaml'
require_relative 'apploger'

class UniqueStudentError < ArgumentError; end

class StudentListDBMysql
  def initialize(host: 'localhost', username: , password:, database:, port: 3306, log_path: nil)
    @logger = log_path ? AppLogger.build(log_path) : nil

    @db = Mysql2::Client.new(
      host: host,
      username: username,
      password: password,
      database: database,
      port: port,
      symbolize_keys: true
    )

    @logger&.info("MySQL подключение установлено")
    rescue => e
      @logger&.error("Ошибка подключения к MySQL: #{e.message}")
    raise
  end

  def get_student_by_id(id)
    @logger&.info("Поиск студента по id=#{id}")

    row = @db.query("SELECT * FROM student WHERE id = #{id} LIMIT 1").first
    return nil unless row

    student = Student.from_h(id: row[:id], hash: row)

    @logger&.debug("Найден студент: #{student.to_h}")
    student
    rescue => e
      @logger&.error("Ошибка get_student_by_id: #{e.message}")
    raise
  end

  def get_k_n_student_short_list(k, n)
    @logger&.info("Получение списка студентов k=#{k}, n=#{n}")

    offset = (n - 1) * k
    rows = @db.query("SELECT * FROM student ORDER BY id LIMIT #{k} OFFSET #{offset}")

    students = rows.map { |row| Student.from_h(id: row[:id], hash: row) }
    DataListStudentShort.new(students)
    
    rescue => e
      @logger&.error("Ошибка get_k_n_student_short_list: #{e.message}")
    raise
  end

  def add_student(student)
    @logger&.info("Добавление студента: #{student.short_info}")

    hash = student.to_h
    unique(hash)

    sql = <<~SQL
      INSERT INTO student (last_name, first_name, patronymic, telegram, email, phone, git)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    SQL

    stmt = @db.prepare(sql)
    stmt.execute(
      hash[:last_name], hash[:first_name], hash[:patronymic],
      hash[:telegram], hash[:email], hash[:phone], hash[:git]
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

    exists = @db.query("SELECT 1 FROM student WHERE id = #{id}").any?
    raise "Студент с id=#{id} не найден" unless exists

    sql = <<~SQL
      UPDATE student SET
        last_name = ?, first_name = ?, patronymic = ?,
        telegram = ?, email = ?, phone = ?, git = ?
      WHERE id = ?
    SQL

    stmt = @db.prepare(sql)
    stmt.execute(
      hash[:last_name], hash[:first_name], hash[:patronymic],
      hash[:telegram], hash[:email], hash[:phone], hash[:git],
      id
    )

    @logger&.debug("Студент id=#{id} обновлён")
    rescue => e
      @logger&.error("Ошибка в replace_student_by_id: #{e.message}")
    raise
  end

  def delete_student_by_id(id)
    @logger&.info("Удаление студента id=#{id}")

    @db.query("DELETE FROM student WHERE id = #{id}")

    @logger&.debug("Студент id=#{id} удалён")
    rescue => e
      @logger&.error("Ошибка в delete_student_by_id: #{e.message}")
    raise
  end

  def get_student_short_count
    @db.query("SELECT COUNT(*) AS count FROM student").first[:count]
  end

  private
  def unique(hash, ignore_id = nil)
    query = ignore_id ? "SELECT * FROM student WHERE id != #{ignore_id}" : "SELECT * FROM student"
    rows = @db.query(query)

    new_student = Student.from_h(id: ignore_id, hash: hash)

    rows.each do |row|
      existing_student = Student.from_h(id: row[:id], hash: row)
      raise UniqueStudentError, "Ошибка уникальности студента" if existing_student == new_student
    end
  end

  def symbolize(row)
    row.transform_keys(&:to_sym)
  end
end

# ex = StudentListDBMysql.new(host: 'localhost', username: 'gura', password: '2710', database: 'student_db', port: 3306, log_path: 'db/logs/mysql_student.log')

# puts "=== ДОБАВЛЕНИЕ СТУДЕНТОВ ==="
# s2 = Student.new(
#   last_name: "Грибов",
#   first_name: "Гриб",
#   phone: "+79990001111"
# )

# ex.add_student(s2)
# puts "Студент добавлен\n\n"

# puts "=== ДОБАВЛЕНИЕ СТУДЕНТОВ ==="

# s1 = Student.new(
#   last_name: "Галустянов",
#   first_name: "Галустян",
#   patronymic: "Галустянович"
# )

# ex.add_student(s1)
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