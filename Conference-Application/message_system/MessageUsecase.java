package message_system;

import java.io.Serializable;
import java.util.List;
import java.util.ArrayList;

/*
the use case for message system
* */
public class MessageUsecase implements Serializable {
    /**
     * @serialVersionUID, the variable used for storage purpose
     * @messageList, the list that stores entities of message
     */
    private static final long serialVersionUID = -2095916884810199532L;
    private ArrayList<Message> messageList = new ArrayList<>();

    /**
     * the method that adds messages to the array list
     *
     * @param senderID    , the user' id who sends this message
     * @param receiverID, the receiver's id who receives this message
     * @param content,    the content of this message
     */
    public void addMessage(int senderID, int receiverID, String content) {
        messageList.add(new Message(senderID, receiverID, content));
    }

    /**
     * the method that returns a list of integers,
     * each integer is an index of a message that a receiver receives
     *
     * @param ID , the user's id you wish to plug in to see what messages it receives
     */
    public List<Integer> getMessageByReceiver(Integer ID) {
        List<Integer> sequence = new ArrayList<Integer>();

        for (int i = 0; i < messageList.size(); i++) {
            if (messageList.get(i).getReceiverID().equals(ID))
                sequence.add(i);
        }

        return sequence;
    }

    /**
     * the function that returns an arraylist of Strings given a sequence
     * represents indexes of messages
     *
     * @param sequence , the list of integers that each integer represents
     *                 an index of message that you wish to export,
     *                 the sequence is given by previous method
     */
    public ArrayList<String> exportFormedMessageBySequence(List<Integer> sequence) {
        ArrayList<String> formedMessage = new ArrayList<String>();

        for (int i = 0; i < sequence.size(); i++) {
            formedMessage.add(formMessage(exportByPointer(sequence.get(i)), i + 1));
        }

        return formedMessage;
    }

    /**
     * the method that would give each to-be exported message a pattern
     * that is appropriate for user to view,
     * <p>
     * that indicates the sender of this message,
     * the number of this message
     * the read-or-not status of this message
     * the content of this message
     *
     * @param message , single message entity wanted to be exported
     * @param index,  the index represents in which place the message is in
     *                all messages that are going to be exported
     *                like if it is first, then 1, second then 2     *
     */
    public String formMessage(Message message, int index) {
        String ret = "#\t" + Integer.toString(index) + "\n";

        ret += "from:\t";
        ret += message.getSenderID();
        ret += "\talready read?: ";
        ret += Boolean.toString(message.getReadStatus());
        ret += "\n";
        ret += message.getContent();
        ret += "\n";

        return ret;
    }

    /**
     * the method that exports one message given an index of message
     *
     * @param pointer , the index of message
     */

    public Message exportByPointer(Integer pointer) {
        return this.messageList.get(pointer);
    }

    /**
     * when presented with array list of formed messages
     * the user would make a decision about which message
     * he or she is going to alter read status,
     * if the message is marked as read, then will be set to unread
     * if the message is marked as unread, then will be set to read
     *
     * @param pointer, the choice the user has made to alter the
     *                 read-or-not status of which message
     */

    public void alterReadStatus(int pointer) {
        if (exportByPointer(pointer).getReadStatus())
            exportByPointer(pointer).setAsUnread();
        else
            exportByPointer(pointer).setAsRead();
    }
}