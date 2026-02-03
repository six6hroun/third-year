require 'sqlite3'

db = SQLite3::Database.new("db/sqlite3_student.db")
sql = File.read("db/seeds/001_sqllite3_seed_student.sql")
db.execute_batch(sql)
puts "Таблица заполнена"