package parent.heir;
import date.MyDate;
import parent.Scientist;

public class SeniorEmployee extends Scientist {
    double x = 0.03;
    public SeniorEmployee(int salary, int seniority) {
        super (salary,seniority);
    }

    @Override
    public double allowances() {
        return salary * (1 + seniority * x);
    }

    void setSalary(int salary) {
        this.salary = salary;
    }

    int getSalary(){
        return this.salary;
    }

    void setSeniority(int salary) {
        this.seniority = salary;
    }

    int getSeniority(){
        return this.seniority;
    }
}