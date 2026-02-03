require_relative 'view/student_list_view'
require_relative 'controller/student_list_controller'
app = FXApp.new

view = StudentListView.new(app)
controller = StudentListController.new(view)
view.controller = controller
controller.refresh_data

app.create
app.run