package main4;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
public class Mainfour {
    public static void main(String args[]){
        JFrame f = new JFrame();
        JPanel p = new JPanel();
        f.setSize(600,300);
        f.setLocation(500,200);

        JButton b1 = new JButton("КЛИК");
        JButton b2 = new JButton("КЛИК");
        b1.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                b2.setEnabled(!b2.isEnabled());
            }
        });

        b2.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                b1.setEnabled(!b1.isEnabled());
            }
        });

        p.add(b1);
        p.add(b2);

        f.add(p);
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.setVisible(true);
    }
}
