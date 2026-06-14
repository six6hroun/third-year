import java.util.*;
import java.util.stream.Collectors;

public class InstrumentShop {
    private final List<Instrument> instruments;

    public InstrumentShop() {
        this.instruments = new ArrayList<>();
    }

    public void loadInvoice(List<Instrument> invoice) {
        instruments.addAll(invoice);
    }

    public List<Instrument> getAllInstruments() {
        return new ArrayList<>(instruments);
    }

    // а) С использованием интерфейса-предиката

    public Map<String, List<Instrument>> splitByName() {
        Map<String, List<Instrument>> result = new HashMap<>();
        for (Instrument i : instruments) {
            result.computeIfAbsent(i.getName(), k -> new ArrayList<>()).add(i);
        }
        return result;
    }

    public List<Instrument> sortByPrice() {
        List<Instrument> sorted = new ArrayList<>(instruments);
        sorted.sort((i1, i2) -> Double.compare(i1.getPrice(), i2.getPrice()));
        return sorted;
    }

    public List<Instrument> filterByPrice(double min, double max) {
        InstrumentPredicate pricePredicate = i -> i.getPrice() >= min && i.getPrice() <= max;

        List<Instrument> result = new ArrayList<>();
        for (Instrument i : instruments) {
            if (pricePredicate.test(i)) {
                result.add(i);
            }
        }
        return result;
    }

    public Map<String, List<Instrument>> groupBySize() {
        Map<String, List<Instrument>> result = new HashMap<>();
        for (Instrument i : instruments) {
            result.computeIfAbsent(i.getSize(), k -> new ArrayList<>()).add(i);
        }
        return result;
    }

    // б) С использованием лямбда-функций

    public Map<String, List<Instrument>> splitByNameLambda() {
        return instruments.stream()
                .collect(Collectors.groupingBy(Instrument::getName));
    }

    public List<Instrument> sortByPriceLambda() {
        return instruments.stream()
                .sorted(Comparator.comparingDouble(Instrument::getPrice))
                .collect(Collectors.toList());
    }

    public List<Instrument> filterByPriceLambda(double min, double max) {
        return instruments.stream()
                .filter(i -> i.getPrice() >= min && i.getPrice() <= max)
                .collect(Collectors.toList());
    }

    public Map<String, List<Instrument>> groupBySizeLambda() {
        return instruments.stream()
                .collect(Collectors.groupingBy(Instrument::getSize));
    }
}