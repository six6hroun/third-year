package parentt;

public interface EmployeeManagment {
    default void accept() {System.out.println("Сотрудник принят на работу");}
    default void dismiss() {System.out.println("Сотрудник уволены");}
    default void post(String value) {System.out.println("Сотрудник перемещен на должность: " + value);};
}
