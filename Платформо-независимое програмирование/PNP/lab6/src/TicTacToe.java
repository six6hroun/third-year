import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class TicTacToe extends JFrame {

    private JButton[][] buttons;
    private char currentPlayer;
    private char[][] board;
    private JLabel statusLabel;
    private JButton restartButton;

    public TicTacToe() {
        setTitle("Крестики-нолики");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(400, 450);
        setLocationRelativeTo(null);
        setResizable(false);

        currentPlayer = 'X';
        board = new char[3][3];
        buttons = new JButton[3][3];

        JPanel gamePanel = new JPanel();
        gamePanel.setLayout(new GridLayout(3, 3, 5, 5));
        gamePanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));


        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                board[i][j] = ' ';

                JButton button = new JButton();
                button.setFont(new Font("Arial", Font.BOLD, 60));
                button.setFocusPainted(false);

                final int row = i;
                final int col = j;

                button.addActionListener(new ActionListener() {
                    @Override
                    public void actionPerformed(ActionEvent e) {
                        handleButtonClick(row, col);
                    }
                });

                buttons[i][j] = button;
                gamePanel.add(button);
            }
        }

        JPanel controlPanel = new JPanel();
        controlPanel.setLayout(new BorderLayout());

        statusLabel = new JLabel("Ходит: X", SwingConstants.CENTER);
        statusLabel.setFont(new Font("Arial", Font.BOLD, 18));
        controlPanel.add(statusLabel, BorderLayout.CENTER);

        restartButton = new JButton("Новая игра");
        restartButton.setFont(new Font("Arial", Font.PLAIN, 14));
        restartButton.addActionListener(e -> restartGame());
        controlPanel.add(restartButton, BorderLayout.EAST);

        add(gamePanel, BorderLayout.CENTER);
        add(controlPanel, BorderLayout.SOUTH);

        setVisible(true);
    }


    private void handleButtonClick(int row, int col) {
        if (board[row][col] != ' ' || isGameFinished()) {
            return;
        }

        board[row][col] = currentPlayer;
        buttons[row][col].setText(String.valueOf(currentPlayer));

        char winner = GameLogic.checkWinner(board);

        if (winner != ' ') {
            statusLabel.setText("Победил: " + winner + "!");
            disableAllButtons();
        } else if (GameLogic.isBoardFull(board)) {
            statusLabel.setText("Ничья!");
        } else {
            currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
            statusLabel.setText("Ходит: " + currentPlayer);
        }
    }


    private boolean isGameFinished() {
        char winner = GameLogic.checkWinner(board);
        return winner != ' ' || GameLogic.isBoardFull(board);
    }


    private void disableAllButtons() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                buttons[i][j].setEnabled(false);
            }
        }
    }


    private void restartGame() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                board[i][j] = ' ';
            }
        }

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                buttons[i][j].setText("");
                buttons[i][j].setEnabled(true);
            }
        }

        currentPlayer = 'X';
        statusLabel.setText("Ходит: X");
    }
}