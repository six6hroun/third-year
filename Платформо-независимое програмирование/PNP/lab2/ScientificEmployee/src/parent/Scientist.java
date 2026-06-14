package parent;
public abstract class Scientist {
    protected int salary;
    protected int seniority;

    public Scientist(int salary, int seniority){
        this.salary = salary;
        this.seniority = seniority;
    }

    @Override
    public String toString() {
        return "Зарплата сотрудника: " + salary + ",  Его стаж: " + seniority + " года";
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Scientist other = (Scientist) obj;
        return salary == other.salary && seniority == other.seniority;
    }

    @Override
    public int hashCode() {
        int result = 17;
        result = 31 * result + salary;
        result = 31 * result + seniority;
        return result;
    }

    public abstract double allowances();
    public void accept() {System.out.println("Сотрудник принят на работу");}
    public void dismiss() {System.out.println("Сотрудник уволены");}
    public void post(String value) {System.out.println("Сотрудник перемещен на должность:" + value);}
    public double accural() {return salary + allowances();}
}