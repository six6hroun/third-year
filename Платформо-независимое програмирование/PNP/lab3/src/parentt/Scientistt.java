package parentt;

import parent.Scientist;

public abstract class Scientistt implements EmployeeCalculator{
    protected int salary;
    protected int seniority;

    public Scientistt(int salary, int seniority){
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
        Scientistt other = (Scientistt) obj;
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

    @Override
    public double accural() {
        return salary + allowances();
    }
}
