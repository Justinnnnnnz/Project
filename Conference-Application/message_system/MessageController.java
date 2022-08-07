package message_system;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.Arrays;
import java.util.stream.*;

/**
 * This is the controller for message system
 */
public class MessageController implements Serializable {
    /**
     * @param seriaVersionUID, used for information storing purpose
     * @message the instantiated message usecase
     * @sequence a list of integers that stores the index of messages
     */

    private static final long serialVersionUID = -2095916884810199532L;
    private MessageUsecase message = new MessageUsecase();
    private List<Integer> sequence = new ArrayList<Integer>();

    /**
     * write message is a function to be called whenever you
     * wish to write a message
     * the function eventually returns a true value if all
     * messages are sent properly
     * else returns a false in the mid way
     *
     * @param currentUserID, the userID you currently logg-in,
     *                       as well as the ID who sends the message
     * @param receivers,     the id that will receive this message,
     *                       could be more than one,
     *                       use space to separate between different IDs
     *                       if any of the receiver's ID does not exist in
     *                       user entity, or is not integer,
     *                       the writeMessage returns a false
     * @param content,       the content of this message,
     *                       if the content is empty,
     *                       the writeMessage returns a false
     * @param user,          the use case for user
     * @param data,          the entity for user     *
     */

    public boolean writeMessage(int currentUserID,
                                String receivers,
                                String content,
                                user.UserUseCase user,
                                user.UserEntity data) {
        List<Integer> receiverList = new ArrayList<Integer>();

        if (content.isEmpty())
            return false;

        try {
            for (String each : receivers.trim().split(" ")) {
                int receiverID = Integer.parseInt(each);

                if (receiverID == currentUserID)
                    return false;

                if (!user.existsID(data, receiverID)) {
                    return false;
                }

                receiverList.add(receiverID);
            }

            for (int each : receiverList) {
                message.addMessage(currentUserID, each, content);
            }

            return true;

        } catch (NumberFormatException e) {
            return false;
        }

    }

    /**
     * the viewMessage is used to export the message that
     * currentUserID receives, and returns it as an array list of strings
     *
     * @param currentUserID, the id of user you curretnly logged in,
     *                       also, the method returns all the message received by this user
     */

    public ArrayList<String> viewMessage(int currentUserID) {
        sequence = message.getMessageByReceiver(currentUserID);

        if (sequence.isEmpty())
            return new ArrayList<String>();

        return message.exportFormedMessageBySequence(sequence);
    }

    /**
     * this is a boolean function that would change the read status of
     * messages selected by user, this function must run after a viewMessage
     * method is called
     * the function will return true if all choices are valid
     * like each corresponds to a message presented by viewMessage
     * like in you are resented with following messages
     * <p>
     * 1.................
     * 2.................
     * 3.................
     * 4.................
     * 5.................
     * <p>
     * then the valid choice is(are) integers between 1 and 5 inclusive
     * else, a false is returned
     *
     * @param choice, the string stores the choices made by user,
     *                could be more than one,
     *                and use space to separate between different choices
     */
    public boolean alterReadStatus(String choice) {
        List<Integer> intends = new ArrayList<Integer>();
        int intend = -1;

        for (String each : choice.trim().split(" ")) {
            try {
                intend = Integer.parseInt(each);
            } catch (NumberFormatException e) {
                return false;
            }

            if (intend < 1 || intend > sequence.size())
                return false;

            intends.add(intend - 1);
        }

        for (Integer each : intends)
            message.alterReadStatus(sequence.get(each));

        return true;
    }

    /**
     * this is a boolean function that implements the funtionality that a speaker sends all
     * its attendees a message, if all things go well, returns true, otherwise, returns false
     *
     * @param currentID , the currently logged in user's id, can only be speaker account
     *                  as well as the user that is send the message
     * @param content   , the content of this message
     *                  if it is empty, then return false
     * @param data,     the user entity
     */

    public boolean speakerSendToAll(int currentID, String content, user.UserEntity data) {
        if (content.isEmpty())
            return false;

        try {
            for (ArrayList<Object> each : data.getAttendeeList()) {
                message.addMessage(currentID, (Integer) each.get(0), content);
            }

            return true;
        } catch (NumberFormatException e) {
            return false;
        }


    }

    // returns the use case for message
    public MessageUsecase getMessage() {
        return this.message;

    }
}