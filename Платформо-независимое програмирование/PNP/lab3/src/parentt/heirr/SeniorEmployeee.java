package parentt.heirr;

import parentt.EmployeeManagment;
import parentt.Scientistt;

public class SeniorEmployeee extends Scientistt implements EmployeeManagment {
    double x = 0.03;
    public SeniorEmployeee(int salary, int seniority) {
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
