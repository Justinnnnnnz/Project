package GUI;

import javax.swing.*;

public class ViewLogin implements IMainMenu {
    private IPresenter IPresenter;
    JTextField username;
    JPasswordField password;
    JFrame frame;

    /**
     * view login content
     */
    public ViewLogin() {

        frame = new JFrame("Menu");
        frame.setSize(300, 220);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);


        JLabel welcome = new JLabel("Welcome To The Conference!");
        welcome.setBounds(60, 0, 10000, 40);

        username = new JTextField();
        username.setBounds(90, 50, 150, 30);

        JLabel usernameLabel = new JLabel("User ID:");
        usernameLabel.setBounds(15, 55, 50, 20);

        password = new JPasswordField();
        password.setBounds(90, 90, 150, 30);

        JLabel passwordLabel = new JLabel("Password:");
        passwordLabel.setBounds(15, 95, 100, 20);

        final JButton login = new JButton("Log In");
        login.setBounds(50, 130, 100, 30);

        final JButton signup = new JButton("Sign Up");
        signup.setBounds(150, 130, 100, 30);

        JButton exit = new JButton("Exit");
        exit.setBounds(0, 160, 100, 30);
        exit.addActionListener(e -> getPresenter().exit());

        login.addActionListener(e -> getPresenter().login());

        signup.addActionListener(e -> getPresenter().shiftToSignup());

        JPanel panel = new JPanel();
        panel.setLayout(null);

        panel.add(welcome);
        panel.add(usernameLabel);
        panel.add(username);
        panel.add(passwordLabel);
        panel.add(password);
        panel.add(login);
        panel.add(signup);
        panel.add(exit);

        frame.add(panel);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }

    /**
     * @param IPresenter presenter
     */
    @Override
    public void setPresenter(IPresenter IPresenter) {
        this.IPresenter = IPresenter;
    }

    /**
     * @return presenter
     */
    @Override
    public IPresenter getPresenter() {
        return IPresenter;
    }

    /**
     * display error message
     */
    @Override
    public void displayErrorMessage() {
        JOptionPane.showMessageDialog(null,
                "Incorrect ID or password",
                "Please try again", JOptionPane.ERROR_MESSAGE);
    }

    /**
     * @return user input
     */

    @Override
    public Object[] returnUserInput() {
        try {
            int inputID = Integer.parseInt(username.getText());
            int inputPassword = Integer.parseInt(new String(password.getPassword()));
            return new Integer[]{inputID, inputPassword};
        } catch (NumberFormatException e) {
            return new Integer[]{};
        }
    }

    /**
     * close
     */
    @Override
    public void close() {
        frame.setVisible(false);
    }
}




