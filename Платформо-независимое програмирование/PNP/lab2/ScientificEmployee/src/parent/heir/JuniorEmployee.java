package parent.heir;
import parent.Scientist;

public class JuniorEmployee extends Scientist {
    double x = 0.02;
    public JuniorEmployee(int salary, int seniority) {
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