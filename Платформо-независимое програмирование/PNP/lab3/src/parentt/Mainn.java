package parentt;
import parentt.heirr.Engineerr;
import parentt.heirr.JuniorEmployeee;
import parentt.heirr.SeniorEmployeee;

public class Mainn {
    public static void main(String args[]){
        SeniorEmployeee ex = new SeniorEmployeee(75700, 3);
        System.out.println(ex);

        Scientistt[] count = new Scientistt[9];
        count[0] = new SeniorEmployeee(10120, 1);
        count[1] = new SeniorEmployeee(10120, 1);
        count[2] = new SeniorEmployeee(20600, 3);
        count[3] = new JuniorEmployeee(30000,4);
        count[4] = new JuniorEmployeee(30000,4);
        count[5] = new JuniorEmployeee(42475,6);
        count[6] = new Engineerr(48900,7);
        count[7] = new Engineerr(48900,7);
        count[8] = new Engineerr(82475,9);
        for (Scientistt s : count) {
            System.out.println(s.getClass().getSimpleName() + ": зарплата = " + s.salary + ", сумма = " + (s.salary + s.accural()));
        }


        Scientistt[] tempResult = new Scientistt[count.length];
        int uniqueCount = 0;
        for (int i = 0; i < count.length; i++) {
            boolean isDuplicate = false;
            for (int j = 0; j < uniqueCount; j++) {
                if (count[i].equals(tempResult[j])) {
                    isDuplicate = true;
                    System.out.println("\nНайден дубликат: " + count[i].getClass().getSimpleName() + " с зарплатой " + count[i].salary);
                    break;
                }
            }

            if (!isDuplicate) {
                tempResult[uniqueCount] = count[i];
                uniqueCount++;
            }
        }


        Scientistt[] result = new Scientistt[uniqueCount];
        for (int i = 0; i < uniqueCount; i++) {
            result[i] = tempResult[i];
        }

        System.out.println("\nУникальные элементы");
        for (Scientistt x : result) {
            if (x != null) {
                System.out.println(x.getClass().getSimpleName() + ": зарплата = " + x.salary + ", сумма = " + (x.salary + x.accural()));
            }
        }
    }
}