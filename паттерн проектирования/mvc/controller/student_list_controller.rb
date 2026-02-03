require_relative '../model/student_list'
class StudentListController
  attr_reader :view, :student_list, :current_data_list
  
  def initialize(view)
    @view = view
    @student_list = StudentsListYAML.new('studentlist.yaml')
    @current_page = 1
    @page_size = 10
    @filters = {}
  end
  
  def refresh_data
    @current_data_list = @student_list.get_k_n_student_short_list(@page_size, @current_page, @current_data_list)
    @current_data_list.add_observer(@view)
    @current_data_list.notify_observers
  end
  
  def next_page
    total_students = @student_list.get_student_short_count
    total_pages = (total_students.to_f / @page_size).ceil

    return if @current_page >= total_pages

    @current_page += 1
    refresh_data
  end

  def prev_page
    @current_page -= 1 if @current_page > 1
    refresh_data
  end
end