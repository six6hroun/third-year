package main2;
import javax.swing.*;
public class Maintwo {
    public static void main(String[] args) {
        JFrame f = new JFrame ("Java");
        JPanel p = new JPanel();
        JButton b = new JButton("Клик 1!");
        JButton c = new JButton("Клик 2!");
        JButton d = new JButton("Клик 3!");
        JButton e = new JButton("Клик 4!");
        JButton g = new JButton("Клик 5!");
        JButton h = new JButton("Клик 6!");
        JButton j = new JButton("Клик 7!");
        JButton k = new JButton("Клик 8!");
        JButton l = new JButton("Клик 9!");

        JButton[] array = {b,c,d,e,g,h,j,k,l};
        for (JButton x : array) {
            x.setSize(100,100);
            p.add(x);
        }

        f.add(p);
        f.setSize(600,400);

        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.setVisible(true);
    }
}
