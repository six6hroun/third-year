require 'sqlite3'

db = SQLite3::Database.new("db/sqlite3_student.db")
db.execute("DROP TABLE IF EXISTS student")
puts "Таблица удалена"