package main5;

public class Account {
    private double balance;
    private double depositRate;

    public Account(double initialBalance, double depositRate) {
        this.balance = initialBalance;
        this.depositRate = depositRate;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        } else {
            throw new IllegalArgumentException("Сумма пополнения должна быть положительной");
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
        } else if (amount <= 0) {
            throw new IllegalArgumentException("Сумма снятия должна быть положительной");
        } else {
            throw new IllegalArgumentException("Недостаточно средств на счете");
        }
    }

    public double calculateMonthlyInterest() {
        return balance * (depositRate / 100) / 12;
    }

    public void addMonthlyInterest() {
        balance += calculateMonthlyInterest();
    }

    public double getDepositRate() {
        return depositRate;
    }
}