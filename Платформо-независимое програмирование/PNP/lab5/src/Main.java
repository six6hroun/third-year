import java.util.Arrays;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        InstrumentShop shop = new InstrumentShop();

        List<Instrument> invoice = Arrays.asList(
                new Instrument("дрель", "большой", 5500),
                new Instrument("дрель", "средний", 3500),
                new Instrument("дрель", "малый", 2500),
                new Instrument("ключ разводной", "большой", 1800),
                new Instrument("ключ разводной", "средний", 1200),
                new Instrument("ключ разводной", "малый", 800),
                new Instrument("молоток", "большой", 600),
                new Instrument("молоток", "средний", 450),
                new Instrument("молоток", "малый", 300),
                new Instrument("отвертка", "малый", 150),
                new Instrument("сверло", "средний", 200),
                new Instrument("гвозди", "малый", 50)
        );

        shop.loadInvoice(invoice);

        System.out.println("Все инструменты:");
        shop.getAllInstruments().forEach(System.out::println);

        System.out.println("\nЧЕРЕЗ ИНТЕРФЕЙС-ПРЕДИКАТ");

        System.out.println("\n1. Разделение по названиям:");
        shop.splitByName().forEach((name, instruments) -> {
            System.out.println("  " + name + ": " + instruments.size() + " шт.");
        });

        System.out.println("\n2. Сортировка по цене:");
        shop.sortByPrice().forEach(i -> System.out.println("  " + i));

        System.out.println("\n3. Товары от 500 до 2000 руб.:");
        shop.filterByPrice(500, 2000).forEach(i -> System.out.println("  " + i));

        System.out.println("\n4. Раскладка по габаритам:");
        shop.groupBySize().forEach((size, instruments) -> {
            System.out.println("  " + size + ": " + instruments.size() + " шт.");
        });

        System.out.println("\nЧЕРЕЗ ЛЯМБДА-ФУНКЦИИ");

        System.out.println("\n1. Разделение по названиям:");
        shop.splitByNameLambda().forEach((name, instruments) -> {
            System.out.println("  " + name + ": " + instruments.size() + " шт.");
        });

        System.out.println("\n2. Сортировка по цене:");
        shop.sortByPriceLambda().forEach(i -> System.out.println("  " + i));

        System.out.println("\n3. Товары от 500 до 2000 руб.:");
        shop.filterByPriceLambda(500, 2000).forEach(i -> System.out.println("  " + i));

        System.out.println("\n4. Раскладка по габаритам:");
        shop.groupBySizeLambda().forEach((size, instruments) -> {
            System.out.println("  " + size + ": " + instruments.size() + " шт.");
        });
    }
}