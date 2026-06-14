package calc;

public class Calc {
    public static void main(String[] args) {
        System.out.println("Hello World!");
        Calculator calc=new Calculator();
        System.out.println("2+2="+calc.sum(2,2));
        System.out.println(calc.sqrt(4));
    }
}
