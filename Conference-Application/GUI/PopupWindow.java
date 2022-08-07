package GUI;

import javax.swing.*;
import java.awt.*;

public class PopupWindow implements IPopupWindow {
    public JFrame frame;
    public JPanel panel;
    public IPresenter presenter;

    /**
     * pop up the GUI window
     */
    public PopupWindow() {
        frame = new JFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        panel = new JPanel();
        panel.setBorder(BorderFactory.createEmptyBorder(80, 80, 80, 80));
        panel.setLayout(new GridLayout(0, 1));

        frame.add(panel, BorderLayout.CENTER);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }

    /**
     * add label
     *
     * @param text text of label
     */
    public void addLabel(String text) {
        JLabel label = new JLabel(text);
        this.panel.add(label);
        this.addPanel(panel);
    }

    /**
     * @return test field
     */

    public JTextField addTextField() {
        JTextField field = new JTextField();
        this.panel.add(field);
        addPanel(panel);
        return field;
    }

    /**
     * @param text test
     * @return button
     */
    public JButton addButton(String text) {
        JButton button = new JButton(text);
        this.panel.add(button);
        addPanel(panel);
        return button;
    }

    /**
     * add panel
     *
     * @param panel panel
     */
    public void addPanel(JPanel panel) {
        this.frame.add(panel, BorderLayout.CENTER);
        this.frame.pack();
        this.frame.setLocationRelativeTo(null);
        this.frame.setVisible(true);
    }

    /**
     * add back buttom
     *
     * @param window window
     */

    public void addBackButton(IPopupWindow window) {
        JButton back = new JButton("Back");
        this.panel.add(back);
        back.addActionListener(e -> presenter.back(window));
        this.addPanel(panel);
    }

    /**
     * set tile
     *
     * @param text text
     */

    public void setTitle(String text) {
        this.frame.setTitle(text);
    }

    /**
     * set presenter
     *
     * @param presenter presenter
     */
    public void setPresenter(IPresenter presenter) {
        this.presenter = presenter;
    }

    /**
     * close it
     */
    public void close() {
        this.frame.setVisible(false);
    }

    /**
     * edit it
     */
    @Override
    public void exit() {
        this.close();
        JOptionPane.showMessageDialog(new JFrame(), "Thank you for joining this conference! " +
                "Your information will be saved.");
    }

    /**
     * Display a message depending on user input
     * @param title the title of the message
     * @param message the message itself
     * @param isSuccess is this a success message or failure message
     */
    @Override
    public void showMessageDialog(String title, String message, boolean isSuccess) {
        if(isSuccess){
            JOptionPane.showMessageDialog(null, message, title, JOptionPane.PLAIN_MESSAGE);
        }else {
            JOptionPane.showMessageDialog(null, message, title, JOptionPane.ERROR_MESSAGE);
        }
    }
}
