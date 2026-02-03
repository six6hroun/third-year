require 'sqlite3'

db = SQLite3::Database.new("db/sqlite3_student.db")
puts "Подключение к БД успешно"