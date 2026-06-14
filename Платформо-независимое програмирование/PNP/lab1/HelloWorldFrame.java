//Подключаем библиотеку для работы с графикой
import java.awt.*;
import java.awt.event.*;
//Класс с полем для рисования
class HelloWorldFrame extends Frame{
    HelloWorldFrame(String s){
        super(s);
    }
    public void paint(Graphics g){
        g.setFont(new Font("Serif", Font.ITALIC | Font.BOLD, 30));
        g.drawString("Hello, XXI century World!", 20, 100);
    }
    public static void main(String[] args){
        Frame f = new HelloWorldFrame("Здравствуй, мир XXI века!");
        f.setSize(400, 150);//Задаем размер окна
        f.setVisible(true);//Делаем его видимым
        f.addWindowListener(new WindowAdapter(){
            public void windowClosing(WindowEvent ev){
                System.exit(0);
            }
        });
    }
}