import java.awt.*;
import java.awt.event.*;
//Создаем наш класс, наследуясь от стандартного класса Frame
class SimpleFrame extends Frame{
    SimpleFrame(String s){
        super(s); //Передаем название окна в родительский класс
        setSize(400, 150); //Устанавливаем размер окна
        setVisible(true); //Окно становится видимым
//Добавляем слушателя, который будет реагировать на кнопку
//закрытия окна
        addWindowListener(new WindowAdapter(){
            public void windowClosing(WindowEvent ev){
                dispose(); //Закрываем окно
                System.exit(0); //Выходим из программы
            }
        });
    }
    //Создаем экземпляр нашего класса в главном классе
    public static void main(String[] args){
        new SimpleFrame(" Моя программа");
    }
}