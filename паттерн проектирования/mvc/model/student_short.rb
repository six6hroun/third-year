require_relative 'student'
require_relative 'parent_student'
class StudentShort < ParentStudent
  attr_reader :last_name_initials, :contact

  def initialize (id:, last_name_initials:, contact: nil, git: nil)
    super(id: id, git: git)
    @last_name_initials = last_name_initials
    @contact = contact
  end

  def self.from_student(student)
    raise ArgumentError, "id не существует" if student.id.nil?
    new(
      id: student.id,
      last_name_initials: student.last_name_initials,
      contact: student.contact,
      git: student.git
    )
  end
end