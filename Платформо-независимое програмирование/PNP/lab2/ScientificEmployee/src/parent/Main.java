package parent;
import parent.heir.Engineer;
import parent.heir.JuniorEmployee;
import parent.heir.SeniorEmployee;

public class Main {
    public static void main(String args[]){
        SeniorEmployee ex = new SeniorEmployee(75700, 3);
        System.out.println(ex);

        Scientist[] count = new Scientist[9];
        count[0] = new SeniorEmployee(10120, 1);
        count[1] = new SeniorEmployee(10120, 1);
        count[2] = new SeniorEmployee(20600, 3);
        count[3] = new JuniorEmployee(30000,4);
        count[4] = new JuniorEmployee(30000,4);
        count[5] = new JuniorEmployee(42475,6);
        count[6] = new Engineer(48900,7);
        count[7] = new Engineer(48900,7);
        count[8] = new Engineer(82475,9);
        for (Scientist s : count) {
            System.out.println(s.getClass().getSimpleName() + ": зарплата = " + s.salary + ", сумма = " + (s.salary + s.accural()));
        }


        Scientist[] tempResult = new Scientist[count.length];
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


        Scientist[] result = new Scientist[uniqueCount];
        for (int i = 0; i < uniqueCount; i++) {
            result[i] = tempResult[i];
        }

        System.out.println("\nУникальные элементы");
        for (Scientist x : result) {
            if (x != null) {
                System.out.println(x.getClass().getSimpleName() + ": зарплата = " + x.salary + ", сумма = " + (x.salary + x.accural()));
            }
        }
    }
}