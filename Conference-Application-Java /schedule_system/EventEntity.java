package schedule_system;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * @author Kangzhi Gao
 * An entity class that stores the information of events.
 */
public class EventEntity implements Serializable {
    private static final long serialVersionUID = -2095916884810199532L;
    private String title;
    private int startTime;
    private int endTime;
    private ArrayList<Integer> attendeeList;
    private int roomNumber;
    private ArrayList<String> speakerName;
    private int size;
    private boolean vip;

    /**
     * Constructor to create an instance of Event.
     *
     * @param title       the title of the event.
     * @param startTime   the start time of the event.
     * @param endTime     the end time of the event.
     * @param roomNumber  the place where the event takes place.
     * @param speakerName the name of the speaker of the event.
     * @param size        the size of the event
     * @param vip         the event is an vip only event or not
     */

    public EventEntity(String title, int startTime, int endTime, int roomNumber, ArrayList<String> speakerName, int size, boolean vip) {
        this.title = title;
        this.startTime = startTime;
        this.endTime = endTime;
        this.attendeeList = new ArrayList<>();
        this.roomNumber = roomNumber;
        if (speakerName.isEmpty()) {
            this.speakerName = new ArrayList<>();
        } else {
            this.speakerName = speakerName;
        }
        this.size = size;
        this.vip = vip;
    }

    /**
     * Gets the input title of the event
     *
     * @return A string that is the title of the event.
     */
    public String getTitle() {
        return title;
    }

    /**
     * Gets the input start time of the event.
     *
     * @return An int that represents the start time of the event.
     */
    public int getStartTime() {
        return startTime;
    }

    /**
     * Gets the input end time of the event.
     *
     * @return An int that represents the end time of the event.
     */
    public int getEndTime() {
        return endTime;
    }

    /**
     * Gets the attendee list of the event
     *
     * @return An arraylist that contains the usernames of the attended attendees
     */
    public ArrayList<Integer> getAttendeeList() {
        return attendeeList;
    }

    /**
     * Gets the input room number of the event that will take place.
     *
     * @return An integer that represents the room number.
     */
    public int getRoomNumber() {
        return roomNumber;
    }

    /**
     * Gets the input name of the speaker of the event.
     *
     * @return A string that represents the name of the speaker.
     */
    public ArrayList<String> getSpeakerName() {
        return speakerName;
    }

    /**
     * Gets the value of size of the event.
     *
     * @return An integer that represents the value of the size.
     */
    public int getSize() {
        return size;
    }

    public void setAttendeeList(ArrayList<Integer> attendeeList) {
        this.attendeeList = attendeeList;
    }

    public boolean getVip() {
        return this.vip;
    }
}

