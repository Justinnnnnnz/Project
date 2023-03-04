package message_system;

import java.io.Serializable;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

// ignore this class please

public class HelperFunction implements Serializable {
    private static final long serialVersionUID = -2095916884810199532L;

    public void printMessage(Message message) {
        System.out.println(message.getContent());
        System.out.println("\n");
    }

    public void statusIndicator(List<Message> message, int currentID, String order) {
        if (order.equals("receive")) {
            System.out.println("You have received the following message(s): ");
        } else if (order.equals("send")) {
            System.out.println("You have sent the following message(s): ");
        }
        System.out.println("-------------------------------------");

        String status = "";

        if (order.equals("receive")) {
            for (int i = 0; i < message.size(); i++) {
                status += Integer.toString(i + 1);
                status += ":\t";
                status += "from:\t";
                status += message.get(i).getSenderID();
                status += "\talready read?: ";
                status += Boolean.toString(message.get(i).getReadStatus());
                status += "\n";
            }
        } else if (order.equals("send")) {
            for (int i = 0; i < message.size(); i++) {
                status += Integer.toString(i + 1);
                status += ":\t";
                status += "to:\t";
                status += message.get(i).getReceiverID();
                status += "\n";
            }
        }

        System.out.println(status);
    }

    public boolean inputValidater(int[] validInput, int input) {
        for (int each : validInput) {
            if (each == input)
                return true;
        }

        System.out.println("Not a valid input!");
        System.out.println("Please try again!");
        return false;
    }

    public void textBox(String order) {
        System.out.println("Plz make your choice!");
        System.out.println("-------------------------------------");

        if (order.equals("receive")) {
            System.out.println("1. read other message(s)");
            System.out.println("2. mark this message as unread");
            System.out.println("3. reply to this sender");
            System.out.println("4. exit and do something else");
        } else if (order.equals("send")) {
            System.out.println("1. read other message(s)");
            System.out.println("2. send this receiver another message");
            System.out.println("3. exit and do something else");
        }

        System.out.println("-------------------------------------");
    }
}