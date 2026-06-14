import java.awt.*;
import java.awt.event.*;
class Pictures extends Frame{
    Pictures(String s) {
        super(s);
        setBounds(0, 0, 1000, 600);
        setVisible(true);
    }
    
    public void paint(Graphics g) {
        elipc(g);
        rectangule(g);
        exemple(g);
    }

    public void elipc(Graphics g) {
        g.fillOval(50,50,200,200);
    }

    public void rectangule(Graphics g) {
        g.setColor(Color.green);
        g.fillRect(300,50,200,200);
    }

    public void exemple(Graphics g) {
        g.setColor(Color.blue);
        g.fillOval(600,50,50,50);
        g.fillOval(575,100,100,100);
        g.fillOval(550,200,150,150);
    }

    public static void main(String[] args){
        Pictures f = new Pictures(" Пример рисования");
        f.addWindowListener(new WindowAdapter(){
            public void windowClosing(WindowEvent ev){
                System.exit(0);
            }
        });
    }
}