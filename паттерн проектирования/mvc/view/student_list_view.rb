require 'fox16'
include Fox

class StudentListView < FXMainWindow
  attr_accessor :controller

  def initialize(app)
    super(app, "Студенты", width: 1200, height: 700)
    setup_ui
    setup_default_filters
  end

  def create
    super
    show
  end

  def on_data_changed(table, column)
    set_table_params(column, table.rows)
    set_table_data(table)
    update_pagination_info
  end

  private
  def setup_ui
    @tabs = FXTabBook.new(self, nil, 0, LAYOUT_FILL_X | LAYOUT_FILL_Y)
    build_students_tab
    build_other_tabs
  end



  def build_students_tab
    FXTabItem.new(@tabs, "Студенты")
    @students_tab = FXVerticalFrame.new(@tabs, LAYOUT_FILL_X | LAYOUT_FILL_Y, padding: 10)

    build_filters
    build_table
    build_pagination
    build_controls
  end

  def build_other_tabs
    FXTabItem.new(@tabs, "Вкладка2")
    FXVerticalFrame.new(@tabs, LAYOUT_FILL_X | LAYOUT_FILL_Y, padding: 10)

    FXTabItem.new(@tabs, "Вкладка3")
    FXVerticalFrame.new(@tabs, LAYOUT_FILL_X | LAYOUT_FILL_Y, padding: 10)
  end

  


  def build_filters
    frame = FXGroupBox.new(@students_tab, "Фильтрация",
      GROUPBOX_TITLE_LEFT | FRAME_GROOVE | LAYOUT_FILL_X)

    container = FXVerticalFrame.new(frame, LAYOUT_FILL_X, padding: 5)

    build_fio_filter(container)
    build_git_filter(container)
    build_email_filter(container)
    build_phone_filter(container)
    build_telegram_filter(container)
  end

  def build_fio_filter(parent)
    frame = FXHorizontalFrame.new(parent, LAYOUT_FILL_X)
    FXLabel.new(frame, "Фамилия и инициалы:")
    @fio_field = FXTextField.new(frame, 30)
  end

  def build_git_filter(parent)
    build_contact_filter(parent, "Гит:", :git)
  end

  def build_email_filter(parent)
    build_contact_filter(parent, "Почта:", :email)
  end

  def build_phone_filter(parent)
    build_contact_filter(parent, "Телефон:", :phone)
  end

  def build_telegram_filter(parent)
    build_contact_filter(parent, "Телеграм:", :telegram)
  end

  def build_contact_filter(parent, label, key)
    frame = FXHorizontalFrame.new(parent)
    FXLabel.new(frame, label)

    radio = FXDataTarget.new(2)
    radio_frame = FXHorizontalFrame.new(frame)

    FXRadioButton.new(radio_frame, "Да", radio, FXDataTarget::ID_OPTION)
    FXRadioButton.new(radio_frame, "Нет", radio, FXDataTarget::ID_OPTION + 1)
    FXRadioButton.new(radio_frame, "Не важно", radio, FXDataTarget::ID_OPTION + 2)

    field = FXTextField.new(frame, 30)
    field.disable

    radio.connect(SEL_COMMAND) do
      radio.value == 0 ? field.enable : field.disable
    end

    instance_variable_set("@#{key}_radio_group", radio)
    instance_variable_set("@#{key}_field", field)
  end

  
  
  def build_table
    frame = FXGroupBox.new(@students_tab, "Таблица студентов",
      GROUPBOX_TITLE_LEFT | FRAME_GROOVE | LAYOUT_FILL_X | LAYOUT_FILL_Y)

    @table = FXTable.new(frame,
      opts: TABLE_READONLY | TABLE_COL_SIZABLE | TABLE_ROW_SIZABLE |
            LAYOUT_FILL_X | LAYOUT_FILL_Y)

    @table.setTableSize(0, 4)
    @table.rowHeaderWidth = 40
    @table.columnHeaderHeight = 25

    @table.connect(SEL_CHANGED) { update_buttons_state }
  end

  def set_table_params(column_names, row_count)
    @table.setTableSize(row_count, column_names.size)

    column_names.each_with_index do |name, i|
      @table.setColumnText(i, name)
    end

    @table.setColumnWidth(0, 50)
    @table.setColumnWidth(1, 250)
    @table.setColumnWidth(2, 200)
    @table.setColumnWidth(3, 200)
  end

  def set_table_data(data_table)
    current_page = @controller.instance_variable_get(:@current_page) || 1
    page_size    = @controller.instance_variable_get(:@page_size) || 10
    offset = (current_page - 1) * page_size

    data_table.rows.times do |row|
      data_table.columns.times do |col|
        value =
          if col == 0
            offset + row + 1
          else
            data_table.get(row, col)
          end

        @table.setItemText(row, col, value.to_s)
      end
    end
  end

  
  
  def build_pagination
    frame = FXHorizontalFrame.new(@students_tab, LAYOUT_CENTER_X, padding: 10) 

    @prev_button = FXButton.new(frame, "Назад")
    @page_label  = FXLabel.new(frame, "Страница: 1 из 1")
    @next_button = FXButton.new(frame, "Вперед")

    @prev_button.connect(SEL_COMMAND) { prev_page }
    @next_button.connect(SEL_COMMAND) { next_page }

  end

  def prev_page
    @controller.prev_page
  end

  def next_page
    @controller.next_page
  end


  def update_pagination_info
    return unless @controller && @controller.student_list

    total = @controller.student_list.get_student_short_count
    size  = @controller.instance_variable_get(:@page_size) || 10
    page  = @controller.instance_variable_get(:@current_page) || 1
    pages = (total.to_f / size).ceil

    @page_label.text = "Страница: #{page} из #{pages}"
  end

  
  

  def build_controls
    frame = FXHorizontalFrame.new(@students_tab, LAYOUT_FILL_X | FRAME_GROOVE, padding: 10)

    @add_button    = FXButton.new(frame, "Добавить")
    @edit_button   = FXButton.new(frame, "Изменить")
    @delete_button = FXButton.new(frame, "Удалить")
    @refresh_button = FXButton.new(frame, "Обновить")

    @edit_button.enabled = false
    @delete_button.enabled = false

    @refresh_button.connect(SEL_COMMAND) do
      @controller.set_filters(collect_filters) if @controller
    end
  end

  


  def collect_filters
    {
      fio: @fio_field.text.strip,
      git: contact_filter(:git),
      email: contact_filter(:email),
      phone: contact_filter(:phone),
      telegram: contact_filter(:telegram)
    }
  end

  def contact_filter(key)
    {
      has: instance_variable_get("@#{key}_radio_group").value,
      text: instance_variable_get("@#{key}_field").text.strip
    }
  end

  def setup_default_filters
    @fio_field.text = ""
    %i[git email phone telegram].each do |k|
      instance_variable_get("@#{k}_radio_group").value = 2
      instance_variable_get("@#{k}_field").disable
    end
  end

  def update_buttons_state
    rows = selected_rows.size
    @edit_button.enabled = (rows == 1)
    @delete_button.enabled = (rows > 0)
  end

  def selected_rows
    (0...@table.numRows).select { |i| @table.isRowSelected(i) }
  end
end