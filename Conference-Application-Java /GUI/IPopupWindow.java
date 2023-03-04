package GUI;

import javax.swing.*;

public interface IPopupWindow {
    void addLabel(String text);

    JTextField addTextField();

    JButton addButton(String text);

    void addPanel(JPanel panel);

    void addBackButton(IPopupWindow window);

    void setTitle(String text);

    void setPresenter(IPresenter presenter);

    void close();

    void exit();

    void showMessageDialog(String title, String message, boolean isSuccess);
}
