package date;
public class MyDate {
    private int day, month,year;
    public MyDate(int d, int m, int y)
    {day=d; month=m; year=y;}

    @Override
    public boolean equals(Object o)
    {
        boolean result =false;
        if(o!=null && o instanceof MyDate)
        { MyDate d=(MyDate)o; //Явное приведение типов
            if ((day==d.day)&&(month==d.month)&&(year==d.year))
                result=true;
        }
        return result;
    }
}