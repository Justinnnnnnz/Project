package message_system;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

// the entity storing single piece of message

public class Message implements Serializable {
    /**
     * @param senderID, the ID who sends this message
     * @param receiverID, the ID who receives this message
     * @param content, the content of this message
     * @param hasRead, can represent whether this message is read or not
     */

    private static final long serialVersionUID = -2095916884810199532L;
    private Integer senderID;
    private Integer receiverID;
    private String content;
    private boolean hasRead;

    public Message(Integer sID, Integer rID, String c) {
        this.senderID = sID;
        this.receiverID = rID;
        this.content = c;
        this.hasRead = false;
    }

    // return the if-read-or-not status of this single message
    public boolean getReadStatus() {
        return this.hasRead;
    }

    // set the current message as read
    public void setAsRead() {
        this.hasRead = true;
    }

    // set the current message as unread
    public void setAsUnread() {
        this.hasRead = false;
    }

    // return the id who sends this message
    public Integer getSenderID() {
        return this.senderID;
    }

    // return the id who receives this message
    public Integer getReceiverID() {
        return this.receiverID;
    }

    // return the content of this message
    public String getContent() {
        return this.content;
    }
}