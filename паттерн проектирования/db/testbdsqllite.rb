require 'sqlite3'

db = SQLite3::Database.new "db/sqlite3_student.db"
count = db.get_first_value("SELECT COUNT(*) FROM student")
puts "В таблице #{count} записей"

db.execute("SELECT * FROM student") do |row|
  p row
end