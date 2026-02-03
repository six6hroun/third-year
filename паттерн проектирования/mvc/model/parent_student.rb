class ParentStudent
  attr_reader :id, :git

  def initialize(id: nil, git: nil)
    @id = id
    @git = git
  end

  def to_s
    short_info
  end

  def short_info
    array = []
    array << "id студента:#{id}" if id
    array << "Фамилия и инициалы: #{last_name_initials}"
    array << "Контакт: #{contact}" if has_contact?
    array << "Гит:#{git}" if has_git?
    array.join(", ")
  end

  def has_contact?
    !contact.nil? && !contact.empty?
  end

  def has_git?
    !git.nil? && !git.empty?
  end

  protected
  def last_name_initials
    raise NotImplementedError
  end

  def contact
    raise NotImplementedError
  end
end