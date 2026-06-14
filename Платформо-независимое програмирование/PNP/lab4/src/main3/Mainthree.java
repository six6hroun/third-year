package main3;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
public class Mainthree {
    public static void main(String args[]){
        JFrame f = new JFrame();
        JPanel p = new JPanel();
        f.setSize(600,300);
        f.setLocation(500,200);

        JButton b = new JButton("10");
        b.addActionListener(new ActionListener() {
            int k = 10;

            @Override
            public void actionPerformed(ActionEvent e) {
                k--;
                b.setText(String.valueOf(k));
                if (k == 1) { f.dispose();}
            }
        });
        p.add(b);
        f.add(p);

        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.setVisible(true);
    }
}
