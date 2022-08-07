package GUI;

import javax.swing.*;
import java.awt.*;

public class ViewUser implements IViewUser {

    private IPresenter IPresenter;
    public JFrame frame;
    public JPanel panel;

    /**
     * able to view user's data
     */
    public ViewUser() {

        frame = new JFrame();
        frame.setSize(600, 400);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        //Jlabel and Jbutton part
        JLabel welcome = new JLabel("Log In Success! Welcome!");

        JLabel welcome1 = new JLabel("You Can:");
        JButton logout = new JButton("Log Out");
        logout.addActionListener(e -> getPresenter().shiftToLogin());

        //view message
        JButton viewMessage = new JButton("View Message");
        viewMessage.addActionListener(e -> getPresenter().shiftToViewMessage());
        //send message
        JButton sendMessage = new JButton("Send Message");
        sendMessage.addActionListener(e -> getPresenter().shiftToSendMessage());
        //Mark message read/unread
        JButton mark = new JButton("Mark Messages Read/Unread");
        mark.addActionListener(e -> getPresenter().shiftToMarkMessage());

        panel = new JPanel();
        panel.setBorder(BorderFactory.createEmptyBorder(80, 80, 80, 80));
        panel.setLayout(new GridLayout(0, 1));

        //panel add part
        panel.add(welcome);
        panel.add(welcome1);
        panel.add(logout);
        panel.add(viewMessage);
        panel.add(sendMessage);
        panel.add(mark);

        frame.add(panel, BorderLayout.CENTER);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }

    /**
     * set up the presenter
     */
    @Override

    public void setPresenter(IPresenter IPresenter) {
        this.IPresenter = IPresenter;
    }

    /**
     * get the presenter
     */

    @Override
    public IPresenter getPresenter() {
        return this.IPresenter;
    }

    /**
     * close the process
     */

    @Override
    public void close() {
        this.frame.setVisible(false);
    }


    /**
     * display the Error Message
     */
    @Override
    public void displayErrorMessage() {
        JOptionPane.showMessageDialog(null,
                "Incorrect or Empty ID Provided",
                "Please try again", JOptionPane.ERROR_MESSAGE);
    }

    /**
     * see a message if view succeed
     */
    public void successMessage() {
        JOptionPane.showMessageDialog(null,
                "Sent Success!",
                "Success!", JOptionPane.PLAIN_MESSAGE);
    }


}
