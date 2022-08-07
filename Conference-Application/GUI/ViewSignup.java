package GUI;

import javax.swing.*;

public class ViewSignup implements IMainMenu {
    private IPresenter IPresenter;
    JTextField username;
    JTextField password;
    JTextField password1;
    JTextField name;
    JFrame signup;

    /**
     * Able to view that user has signed up for
     */
    public ViewSignup() {
        signup = new JFrame("Create A New Account!");
        signup.setSize(750, 380);
        signup.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JLabel comment = new JLabel("Please Enter Your UNIQUE ID and Password in Numbers (10 Digits Maximum).");
        comment.setBounds(30, 0, 10000, 30);

        JLabel comment1 = new JLabel("Your ID Must Start With 9 If You Want to Sign Up as a VIP.");
        comment1.setBounds(30, 20, 10000, 30);

        JLabel comment2 = new JLabel("Your ID Must Start With 1 if You Want to Sign Up as an Organizer.");
        comment2.setBounds(30, 40, 10000, 30);

        JLabel comment3 = new JLabel("Your ID Must Start With 2 if You Want to Sign Up as an Attendee.");
        comment3.setBounds(30, 60, 10000, 30);

        JLabel comment4 = new JLabel("Your ID Must Start With 3 if You Want to Sign Up as a Speaker, " +
                "and You Must Enter Your Name.");
        comment4.setBounds(30, 80, 10000, 30);

        username = new JTextField();
        username.setBounds(250, 120, 150, 30);


        JLabel usernameLabel = new JLabel("Your ID:");
        usernameLabel.setBounds(100, 120, 200, 30);

        password = new JPasswordField();
        password.setBounds(250, 160, 150, 30);

        JLabel passwordLabel = new JLabel("Your Password:");
        passwordLabel.setBounds(100, 160, 200, 30);

        JLabel passwordlabel1 = new JLabel("Your Password Again:");
        passwordlabel1.setBounds(100, 200, 200, 30);

        password1 = new JPasswordField();
        password1.setBounds(250, 200, 150, 30);


        JLabel speakername = new JLabel("Your Name:");
        speakername.setBounds(100, 240, 200, 30);

        name = new JTextField();
        name.setBounds(250, 240, 150, 30);

        JButton signup1 = new JButton("Sign Up!");
        signup1.setBounds(200, 290, 100, 30);
        signup1.addActionListener(e -> getPresenter().signup());

        JPanel panel = new JPanel();
        panel.setLayout(null);


        panel.add(comment);
        panel.add(comment1);
        panel.add(comment2);
        panel.add(comment3);
        panel.add(comment4);
        panel.add(username);
        panel.add(usernameLabel);
        panel.add(password);
        panel.add(passwordLabel);
        panel.add(password1);
        panel.add(passwordlabel1);
        panel.add(signup1);
        panel.add(speakername);
        panel.add(name);

        signup.add(panel);
        signup.setLocationRelativeTo(null);
        signup.setVisible(true);
    }

    /**
     * set the presenter
     */
    @Override

    public void setPresenter(IPresenter IPresenter) {
        this.IPresenter = IPresenter;
    }

    /**
     * return the presenter
     */
    @Override
    public IPresenter getPresenter() {
        return IPresenter;
    }

    /**
     * display the error message
     */
    @Override
    public void displayErrorMessage() {
        JOptionPane.showMessageDialog(null,
                "At least one of your input is incorrect, " +
                        "please follow the instructions and try again.", "Incorrect Input",
                JOptionPane.ERROR_MESSAGE);

    }

    /**
     * return the user input
     */
    @Override
    public Object[] returnUserInput() {
        try {
            int inputID = Integer.parseInt(username.getText());
            int inputPassword = Integer.parseInt(password.getText());
            int confirmPassword = Integer.parseInt(password1.getText());
            String inputName = name.getText();
            int firstDigit = Integer.parseInt(Integer.toString(inputID).substring(0, 1));
            if (firstDigit != 1 && firstDigit != 2 && firstDigit != 3 && firstDigit != 9)
                return new Integer[]{};
            if (firstDigit == 3 && inputName.equals(""))
                return new Integer[]{};
            if (inputPassword != confirmPassword)
                return new Integer[]{};
            return new Object[]{inputID, inputPassword, confirmPassword, inputName};
        } catch (NumberFormatException e) {
            return new Integer[]{};
        }
    }

    /**
     * close the process
     */
    @Override
    public void close() {
        signup.setVisible(false);
    }
}
