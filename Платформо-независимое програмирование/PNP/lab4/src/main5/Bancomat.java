package main5;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Bancomat extends JFrame {
    private Account account;
    private JLabel balanceLabel;
    private JLabel rateLabel;
    private JTextField amountField;

    public Bancomat() {
        account = new Account(1000.0, 5.0);

        setTitle("Банкомат");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(450, 350);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        JPanel topPanel = new JPanel();
        topPanel.setLayout(new GridLayout(2, 1, 5, 5));
        topPanel.setBorder(BorderFactory.createEmptyBorder(15, 15, 10, 15));

        balanceLabel = new JLabel();
        balanceLabel.setFont(new Font("Arial", Font.BOLD, 16));
        balanceLabel.setForeground(Color.BLACK);

        rateLabel = new JLabel();
        rateLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        rateLabel.setForeground(Color.BLACK);

        updateLabels();

        topPanel.add(balanceLabel);
        topPanel.add(rateLabel);

        JPanel centerPanel = new JPanel();
        centerPanel.setLayout(new GridBagLayout());
        centerPanel.setBorder(BorderFactory.createEmptyBorder(10, 20, 20, 20));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.insets = new Insets(5, 5, 5, 5);

        JLabel amountLabel = new JLabel("Сумма:");
        amountLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        amountLabel.setForeground(Color.BLACK);
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridwidth = 1;
        centerPanel.add(amountLabel, gbc);

        amountField = new JTextField(15);
        amountField.setFont(new Font("Arial", Font.PLAIN, 14));
        gbc.gridx = 1;
        gbc.gridy = 0;
        gbc.gridwidth = 2;
        centerPanel.add(amountField, gbc);

        JButton withdrawButton = createStyledButton("Снять наличные", new Color(255, 99, 71));
        gbc.gridx = 0;
        gbc.gridy = 1;
        gbc.gridwidth = 1;
        centerPanel.add(withdrawButton, gbc);

        JButton depositButton = createStyledButton("Пополнить счет", new Color(60, 179, 113));
        gbc.gridx = 1;
        gbc.gridy = 1;
        centerPanel.add(depositButton, gbc);

        JButton interestButton = createStyledButton("Начислить проценты", new Color(255, 165, 0));
        gbc.gridx = 2;
        gbc.gridy = 1;
        centerPanel.add(interestButton, gbc);

        JButton balanceButton = createStyledButton("Проверить баланс", new Color(200, 200, 200));
        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.gridwidth = 3;
        centerPanel.add(balanceButton, gbc);

        add(topPanel, BorderLayout.NORTH);
        add(centerPanel, BorderLayout.CENTER);

        withdrawButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                handleWithdraw();
            }
        });

        depositButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                handleDeposit();
            }
        });

        interestButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                handleInterest();
            }
        });

        balanceButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                handleBalance();
            }
        });
    }

    private JButton createStyledButton(String text, Color color) {
        JButton button = new JButton(text);
        button.setBackground(color);
        button.setForeground(Color.BLACK);
        button.setFont(new Font("Arial", Font.BOLD, 12));
        button.setFocusPainted(false);
        button.setBorder(BorderFactory.createEmptyBorder(10, 15, 10, 15));
        return button;
    }

    private void updateLabels() {
        balanceLabel.setText(String.format("Текущий баланс: %.2f руб.", account.getBalance()));
        rateLabel.setText(String.format("Годовая ставка: %.1f%% (месячный процент: %.2f руб.)",
                account.getDepositRate(), account.calculateMonthlyInterest()));
    }

    private void showMessage(String message, String title, int messageType) {
        JOptionPane.showMessageDialog(this, message, title, messageType);
    }

    private double getAmountFromField() {
        try {
            double amount = Double.parseDouble(amountField.getText().trim());
            amountField.setText("");
            return amount;
        } catch (NumberFormatException e) {
            showMessage("Пожалуйста, введите корректную сумму", "Ошибка", JOptionPane.ERROR_MESSAGE);
            return -1;
        }
    }

    private void handleWithdraw() {
        double amount = getAmountFromField();
        if (amount > 0) {
            try {
                account.withdraw(amount);
                updateLabels();
                showMessage(String.format("Снято %.2f руб.", amount), "Успешно", JOptionPane.INFORMATION_MESSAGE);
            } catch (IllegalArgumentException e) {
                showMessage(e.getMessage(), "Ошибка", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void handleDeposit() {
        double amount = getAmountFromField();
        if (amount > 0) {
            try {
                account.deposit(amount);
                updateLabels();
                showMessage(String.format("Внесено %.2f руб.", amount), "Успешно", JOptionPane.INFORMATION_MESSAGE);
            } catch (IllegalArgumentException e) {
                showMessage(e.getMessage(), "Ошибка", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void handleInterest() {
        double interest = account.calculateMonthlyInterest();
        account.addMonthlyInterest();
        updateLabels();
        showMessage(String.format("Начислены проценты: %.2f руб.", interest),
                "Начисление процентов", JOptionPane.INFORMATION_MESSAGE);
    }

    private void handleBalance() {
        showMessage(String.format("Текущий баланс: %.2f руб.", account.getBalance()),
                "Баланс", JOptionPane.INFORMATION_MESSAGE);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                try {
                    UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
                } catch (Exception e) {
                    e.printStackTrace();
                }
                new Bancomat().setVisible(true);
            }
        });
    }
}