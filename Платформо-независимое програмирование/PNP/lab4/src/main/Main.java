package main;
import javax.swing.*;
public class Main {
    public static void main(String[] args) {
        JFrame f = new JFrame ("Java");
        //JPanel p = new JPanel();
        JLabel a = new JLabel("Метка 1");
        JLabel b = new JLabel("Метка 2");
        JLabel c = new JLabel("Метка 3");

        a.setSize(100,100);
        b.setSize(100,100);
        c.setSize(100,100);

        f.add(a);
        f.add(b);
        f.add(c);

        //f.add(p);
        f.setSize(500,300);


        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.setVisible(true);
    }
}
