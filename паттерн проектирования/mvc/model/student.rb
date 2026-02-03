require_relative 'parent_student'
class Student < ParentStudent
  attr_reader :last_name, :first_name, :patronymic
  include Comparable

  def initialize(id: nil, last_name:, first_name:, patronymic: nil, phone: nil, telegram: nil, email: nil, git: nil) 
    raise ArgumentError, "Неверный формат гита #{git}" unless self.class.valid_git?(git)
    super(id:id, git: git)
    self.last_name = last_name
    self.first_name = first_name
    self.patronymic = patronymic
    self.contact = {phone: phone, telegram: telegram, email: email}
  end

  def contact
    if @telegram && !@telegram.empty?
        "telegram - #{@telegram}"
    elsif @email && !@email.empty?
        "email - #{@email}"
    elsif @phone && !@phone.empty? 
        "phone - #{@phone}"
    else
        nil
    end
  end

  def contact=(contacts)
    contacts.each do |type, value|
      validator = "valid_#{type}?".to_sym
      raise ArgumentError, "Неверный формат #{type}" unless self.class.send(validator, value)
      instance_variable_set("@#{type}", value)
    end
  end

  def self.validated_attr_writer(attribute, validation_name)
    define_method("#{attribute}=") do |value|
        raise ArgumentError unless self.class.send(validation_name, value)
        instance_variable_set("@#{attribute}", value)
    end
  end

  validated_attr_writer :first_name, :valid_name?
  validated_attr_writer :last_name, :valid_name?
  validated_attr_writer :patronymic, :valid_name?
  validated_attr_writer :git, :valid_git?

  def last_name_initials
    if patronymic
      "#{last_name} #{first_name[0]}. #{patronymic[0]}."
    else
      "#{last_name} #{first_name[0]}."
    end
  end

  def self.valid_name?(name)
      name.nil? || (name.is_a?(String) && name.match?(/^[А-ЯA-Z][а-яa-z]+$/))
  end

  def self.valid_phone?(phone)
      phone.nil? || (phone.is_a?(String) && phone.match?(/^(\+7|8)?[\s\-\(]?(\d{3})[\s\-\)]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})$/)) 
  end

  def self.valid_telegram?(telegram)
      telegram.nil? || (telegram.is_a?(String) && telegram.match?(/^@[a-zA-Z0-9_]{5,32}$/))
  end

  def self.valid_email?(email)
      email.nil? || (email.is_a?(String) && email.match?(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/))
  end

  def self.valid_git?(git)
      git.nil? || (git.is_a?(String) && git.match?(/^https:\/\/(github|gitlab)\.com\/[a-zA-Z0-9_-]+\/?$/))
  end

  def to_s
    array = []
    array << "id студента: #{id}" if id
    array << "Фамилия: #{last_name}"
    array << "Имя: #{first_name}"
    array << "Отчество: #{patronymic}" if patronymic
    array << "Номер телефона: #{@phone}" if @phone
    array << "Телеграм: #{@telegram}" if @telegram
    array << "Почта: #{@email}" if @email
    array << "Гит: #{git}" if has_git?
    array.join(", ")
  end

  def to_h
    {
      id: id,
      last_name: last_name,
      first_name: first_name,
      patronymic: patronymic,
      phone: @phone,
      telegram: @telegram,
      email: @email,
      git: git
    }.compact
  end

  def self.from_h(id: nil, hash:)
    new(
      id: id,
      last_name: hash[:last_name],
      first_name: hash[:first_name],
      patronymic: hash[:patronymic],
      phone: hash[:phone],
      telegram: hash[:telegram],
      email: hash[:email],
      git: hash[:git]
    )
  end
  
  def <=>(value)
    [last_name, first_name, patronymic || nil] <=> [value.last_name, value.first_name, value.patronymic || nil]
  end

  def ==(other)
    return false unless other.is_a?(Student)
    [:telegram, :email, :phone, :git].any? do |field|
      self_val = to_h[field]
      other_val = other.to_h[field]
      self_val && other_val && self_val == other_val
    end
  end

end