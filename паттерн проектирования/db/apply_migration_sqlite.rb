require 'sqlite3'

db = SQLite3::Database.new("db/sqlite3_student.db")
sql = File.read("db/migrations/001_sqllite3_create_student.sql")
db.execute_batch(sql)
puts "Таблица создана"