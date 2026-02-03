require 'fox16'
include Fox

@delete_button = nil
@id_sort_asc = true

app = FXApp.new
main_window = FXMainWindow.new(app, "Students", width: 1000, height: 600)


tabs = FXTabBook.new(main_window, nil, 0, LAYOUT_FILL_X | LAYOUT_FILL_Y)
FXTabItem.new(tabs, "Студенты")
students_tab = FXVerticalFrame.new(tabs, LAYOUT_FILL_X | LAYOUT_FILL_Y, padding: 10)

FXTabItem.new(tabs, "Вкладка2")
tab2 = FXVerticalFrame.new(tabs, LAYOUT_FILL_X | LAYOUT_FILL_Y, padding: 10)

FXTabItem.new(tabs, "Вкладка3")
tab3 = FXVerticalFrame.new(tabs, LAYOUT_FILL_X | LAYOUT_FILL_Y, padding: 10)



filters_frame = FXGroupBox.new(students_tab, "Фильтрация", GROUPBOX_TITLE_LEFT | FRAME_GROOVE | LAYOUT_FILL_X)
filters_container = FXVerticalFrame.new(filters_frame, LAYOUT_FILL_X, padding: 5)


fio_frame = FXHorizontalFrame.new(filters_container, LAYOUT_FILL_X)
FXLabel.new(fio_frame, "Фамилия и инициалы:", nil, LAYOUT_SIDE_LEFT)
fio_field = FXTextField.new(fio_frame, 30, nil, 0, TEXTFIELD_NORMAL)


phone_frame = FXHorizontalFrame.new(filters_container)
FXLabel.new(phone_frame, "Телефон:", nil, LAYOUT_SIDE_LEFT | LAYOUT_CENTER_Y)

phone_group = FXGroupBox.new(phone_frame, "", LAYOUT_SIDE_LEFT)
phone_radio_frame = FXHorizontalFrame.new(phone_group, LAYOUT_SIDE_LEFT | PACK_UNIFORM_WIDTH)
phone_radio_group = FXDataTarget.new(2)

FXRadioButton.new(phone_radio_frame, "Да", phone_radio_group, FXDataTarget::ID_OPTION + 0)
FXRadioButton.new(phone_radio_frame, "Нет", phone_radio_group, FXDataTarget::ID_OPTION + 1)
FXRadioButton.new(phone_radio_frame, "Не важно", phone_radio_group, FXDataTarget::ID_OPTION + 2)

phone_field = FXTextField.new(phone_frame, 30, nil, 0, TEXTFIELD_NORMAL)
phone_field.disable

phone_radio_group.connect(SEL_COMMAND) do
  phone_radio_group.value == 0 ? phone_field.enable : phone_field.disable
end


telegram_frame = FXHorizontalFrame.new(filters_container)
FXLabel.new(telegram_frame, "Телеграм:", nil, LAYOUT_SIDE_LEFT | LAYOUT_CENTER_Y)

telegram_group = FXGroupBox.new(telegram_frame, "", LAYOUT_SIDE_LEFT)
telegram_radio_frame = FXHorizontalFrame.new(telegram_group, LAYOUT_SIDE_LEFT | PACK_UNIFORM_WIDTH)
telegram_radio_group = FXDataTarget.new(2)

FXRadioButton.new(telegram_radio_frame, "Да", telegram_radio_group, FXDataTarget::ID_OPTION + 0)
FXRadioButton.new(telegram_radio_frame, "Нет", telegram_radio_group, FXDataTarget::ID_OPTION + 1)
FXRadioButton.new(telegram_radio_frame, "Не важно", telegram_radio_group, FXDataTarget::ID_OPTION + 2)

telegram_field = FXTextField.new(telegram_frame, 30, nil, 0, TEXTFIELD_NORMAL)
telegram_field.disable

telegram_radio_group.connect(SEL_COMMAND) do
  telegram_radio_group.value == 0 ? telegram_field.enable : telegram_field.disable
end


email_frame = FXHorizontalFrame.new(filters_container)
FXLabel.new(email_frame, "Почта:", nil, LAYOUT_SIDE_LEFT | LAYOUT_CENTER_Y)

email_group = FXGroupBox.new(email_frame, "", LAYOUT_SIDE_LEFT)
email_radio_frame = FXHorizontalFrame.new(email_group, LAYOUT_SIDE_LEFT | PACK_UNIFORM_WIDTH)
email_radio_group = FXDataTarget.new(2)

FXRadioButton.new(email_radio_frame, "Да", email_radio_group, FXDataTarget::ID_OPTION + 0)
FXRadioButton.new(email_radio_frame, "Нет", email_radio_group, FXDataTarget::ID_OPTION + 1)
FXRadioButton.new(email_radio_frame, "Не важно", email_radio_group, FXDataTarget::ID_OPTION + 2)


email_field = FXTextField.new(email_frame, 30, nil, 0, TEXTFIELD_NORMAL)
email_field.disable

email_radio_group.connect(SEL_COMMAND) do
  email_radio_group.value == 0 ? email_field.enable : email_field.disable
end


git_frame = FXHorizontalFrame.new(filters_container)
FXLabel.new(git_frame, "Гит:", nil, LAYOUT_SIDE_LEFT | LAYOUT_CENTER_Y)

git_group = FXGroupBox.new(git_frame, "", LAYOUT_SIDE_LEFT)
git_radio_frame = FXHorizontalFrame.new(git_group, LAYOUT_SIDE_LEFT | PACK_UNIFORM_WIDTH)
git_radio_group = FXDataTarget.new(2)

FXRadioButton.new(git_radio_frame, "Да", git_radio_group, FXDataTarget::ID_OPTION + 0)
FXRadioButton.new(git_radio_frame, "Нет", git_radio_group, FXDataTarget::ID_OPTION + 1)
FXRadioButton.new(git_radio_frame, "Не важно", git_radio_group, FXDataTarget::ID_OPTION + 2)

git_field = FXTextField.new(git_frame, 30, nil, 0, TEXTFIELD_NORMAL)
git_field.disable

git_radio_group.connect(SEL_COMMAND) do
  git_radio_group.value == 0 ? git_field.enable : git_field.disable
end



table_frame = FXGroupBox.new(students_tab, "Таблица студентов", GROUPBOX_TITLE_LEFT | FRAME_GROOVE | LAYOUT_FILL_X | LAYOUT_FILL_Y)
@table = FXTable.new(table_frame, opts: TABLE_READONLY | TABLE_COL_SIZABLE | TABLE_ROW_SIZABLE | LAYOUT_FILL_X | LAYOUT_FILL_Y, padding: 5)

@table.setTableSize(10, 8)
@table.rowHeaderWidth = 40
@table.columnHeaderHeight = 25

@table.setColumnText(0, "ID")
@table.setColumnText(1, "Фамилия")
@table.setColumnText(2, "Имя")
@table.setColumnText(3, "Отчество")
@table.setColumnText(4, "Телефон")
@table.setColumnText(5, "Telegram")
@table.setColumnText(6, "Email")
@table.setColumnText(7, "Git")

@test_data = [
  [1, "Иванов", "Иван", "Иванович", "+79161234567", "@ivanov", "ivanov@mail.ru", "https://github.com/ivanov"],
  [2, "Петров", "Петр", "Петрович", "+79031234568", "@petrov", "petrov@gmail.com", "https://github.com/petrov"],
  [3, "Сидорова", "Анна", "Сергеевна", "", "", "sidorova@yandex.ru", ""],
  [4, "Кузнецов", "Алексей", "Дмитриевич", "", "@kuznetsov", "kuznetsov@mail.ru", "https://github.com/kuznetsov"],
  [5, "Смирнов", "Дмитрий", "Андреевич", "+79561234570", "@smirnov", "smirnov@gmail.com", ""],
  [6, "Попов", "Сергей", "Викторович", "+79111234571", "@popov", "popov@yandex.ru", "https://github.com/popov"],
  [7, "Лебедев", "Максим", "Олегович", "+79091234572", "", "lebedev@mail.ru", "https://github.com/lebedev"],
  [8, "Козлов", "Андрей", "Николаевич", "+79211234573", "@kozlov", "kozlov@gmail.com", ""],
  [9, "Новиков", "Евгений", "Владимирович", "", "@novikov", "novikov@yandex.ru", "https://github.com/novikov"],
  [10, "Морозов", "Владимир", "Александрович", "+79361234574", "@morozov", "morozov@mail.ru", "https://github.com/morozov"]
]

@test_data.each_with_index do |row_data, r|
  row_data.each_with_index do |cell_data, c|
    @table.setItemText(r, c, cell_data.to_s)
  end
end

@table.setColumnWidth(3, 120)
@table.setColumnWidth(4, 120)
@table.setColumnWidth(5, 110)
@table.setColumnWidth(6, 165)
@table.setColumnWidth(7, 195)

@table.connect(SEL_CHANGED) do
  update_buttons_state
end

pagination_frame = FXHorizontalFrame.new(students_tab, LAYOUT_CENTER_X, padding: 10)
FXButton.new(pagination_frame, "Назад")
FXLabel.new(pagination_frame, "Страница: 1 из 1")
FXButton.new(pagination_frame, "Вперед")

buttons_frame = FXHorizontalFrame.new(students_tab, LAYOUT_FILL_X | FRAME_GROOVE, padding: 10)
@add_button = FXButton.new(buttons_frame, "Добавить")
@edit_button = FXButton.new(buttons_frame, "Изменить")
@delete_button = FXButton.new(buttons_frame, "Удалить")
@refresh_button = FXButton.new(buttons_frame, "Обновить")

@edit_button.enabled = false
@delete_button.enabled = false

def selected_rows
  (0...@table.numRows).select { |i| @table.isRowSelected(i) }
end

def update_buttons_state
  rows = selected_rows
  count = rows.size

  @edit_button.enabled   = (count == 1)
  @delete_button.enabled = (count >= 1)
end

main_window.connect(SEL_CLOSE) { app.exit }

app.create
main_window.show
app.run