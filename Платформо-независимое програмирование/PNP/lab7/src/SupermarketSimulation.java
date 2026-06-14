import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.ThreadLocalRandom;

public class SupermarketSimulation {

    static class ServiceSystem {
        private final int channels;
        private final boolean isRandomService;
        private final ExecutorService workers;
        private final AtomicInteger served = new AtomicInteger(0);
        private final AtomicInteger arrived = new AtomicInteger(0);
        private ScheduledExecutorService generator;

        public ServiceSystem(int channels, boolean isRandomService) {
            this.channels = channels;
            this.isRandomService = isRandomService;
            this.workers = Executors.newFixedThreadPool(channels);
        }

        public void start() {
            generator = Executors.newScheduledThreadPool(1);
            generator.scheduleAtFixedRate(() -> {
                arrived.incrementAndGet();
                workers.submit(() -> {
                    try {
                        if (isRandomService) {
                            int seconds = ThreadLocalRandom.current().nextInt(60, 301);
                            Thread.sleep(seconds * 1000L);
                        } else {
                            Thread.sleep(90 * 1000L);
                        }
                        served.incrementAndGet();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            }, 0, 60, TimeUnit.SECONDS);
        }

        public void stop() {
            generator.shutdown();
            workers.shutdown();
            try {
                workers.awaitTermination(10, TimeUnit.SECONDS);
            } catch (InterruptedException e) {
                workers.shutdownNow();
            }
        }

        public int getServed() { return served.get(); }
        public int getArrived() { return arrived.get(); }
    }

    public static void main(String[] args) throws InterruptedException {
        ServiceSystem cashDesks = new ServiceSystem(5, false);
        ServiceSystem selfService = new ServiceSystem(5, true);

        cashDesks.start();
        selfService.start();

        Thread.sleep(30 * 60 * 1000L);

        cashDesks.stop();
        selfService.stop();

        int cashServed = cashDesks.getServed();
        int cashArrived = cashDesks.getArrived();
        int autoServed = selfService.getServed();
        int autoArrived = selfService.getArrived();

        System.out.println("Кассы:");
        System.out.println("  Пришло: " + cashArrived);
        System.out.println("  Обслужено: " + cashServed);
        System.out.println("  Эффективность: " + (cashServed * 100.0 / cashArrived) + "%");
        System.out.println();

        System.out.println("Автоматы:");
        System.out.println("  Пришло: " + autoArrived);
        System.out.println("  Обслужено: " + autoServed);
        System.out.println("  Эффективность: " + (autoServed * 100.0 / autoArrived) + "%");
        System.out.println();

        int totalArrived = cashArrived + autoArrived;
        int totalServed = cashServed + autoServed;

        System.out.println("Суммарная эффективность: " + (totalServed * 100.0 / totalArrived) + "%");

        if (cashServed > autoServed) {
            System.out.println("Кассы эффективнее");
        } else if (autoServed > cashServed) {
            System.out.println("Автоматы эффективнее");
        } else {
            System.out.println("Одинаково");
        }
    }
}