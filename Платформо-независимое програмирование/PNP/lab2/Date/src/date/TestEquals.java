package date;
public class TestEquals {
    public static void main(String[] args) {
        MyDate date1=new MyDate(7,11,2014);
        MyDate date2=new MyDate(7,11,2014);
        if (date1==date2)
            System.out.println("date1 is identical date2");
        else
            System.out.println("date1 is not identical date2");

        if (date1.equals(date2))
            System.out.println("date1 is equals date2");
        else
            System.out.println("date1 is not equals date2");

        System.out.println("set date2=date1");
        date2=date1;
        if (date1==date2)
            System.out.println("date1 is identical date2");
        else
            System.out.println("date1 is not identical date2");
    }
}