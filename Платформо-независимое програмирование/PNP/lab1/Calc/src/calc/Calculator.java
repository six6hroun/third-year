package calc;
import calc.operation.Adder;
import calc.operation.Square;
public class Calculator {
    public int sum(int... a)
    {
        Adder adder=new Adder();
        for(int i:a)
        {
            adder.add(i);
        }
        return adder.getSum();
    }

    public int sqrt(int x) {
        Square square=new Square(x);
        return square.sqrt();
    }
}
