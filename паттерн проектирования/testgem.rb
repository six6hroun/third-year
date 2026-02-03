require 'students_list_yaml'
# require_relative 'student_list_JSON'
students = StudentsListYAML.new("studentlist.yaml")
student = Student.new(
  id: nil,
  last_name: "Иванов",
  first_name: "Иван",
  phone: "+79990001125",
  telegram: "@ivannko",
  email: "sus@example.com"
)

students.add_student(student)
students.write_file