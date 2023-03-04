package schedule_system;


import java.io.Serializable;
import java.util.ArrayList;

/**
 * use case to modify event to create event
 */
public class ScheduleUseCase implements Serializable {
    private static final long serialVersionUID = -2095916884810199532L;
    private EventEntity[][] schedule;
    private int start_time_of_day;
    private int end_time_of_day;
    private int room;
    private boolean hasSetConference;

    /**
     * set if there is a conference or not
     *
     * @param hasSetConference there is conference or not
     */
    public void setHasSetConference(boolean hasSetConference) {
        this.hasSetConference = hasSetConference;
    }

    /**
     * getter to see if there is a conference
     */
    public boolean getHasSetConference() {
        return this.hasSetConference;
    }

    /**
     * setter to create a schedule in our system it will check the time and number of room is available or not
     *
     * @param start_time  the start time  of conference
     * @param end_time    the end time of conference
     * @param room_number number of room in the conference
     */
    public boolean scheduleModifier(String start_time, String end_time, String room_number) {
        try {
            int start = Integer.parseInt(start_time);
            int end = Integer.parseInt(end_time);
            int roomNumber = Integer.parseInt(room_number);
            if (start < 9 || end > 17 || roomNumber > 20)
                return false;
            schedule = new EventEntity[roomNumber][end - start];
            start_time_of_day = start;
            end_time_of_day = end;
            room = roomNumber;
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }

    /**
     * getter to get the schedule
     */
    public EventEntity[][] get_schedule() {
        return schedule;
    }

    /**
     * This is the method to check the time and room is valid at that time
     *
     * @param room      the room user want to create event
     * @param startTime the start time of that event
     * @param endTime   the end time of that event
     */
    public boolean check_schedule(int room, int startTime, int endTime) {
        boolean time_valid = (startTime <= end_time_of_day && startTime >= start_time_of_day && endTime
                <= end_time_of_day && endTime >= start_time_of_day && endTime > startTime && (endTime - startTime)
                <= (end_time_of_day - start_time_of_day));
        try {
            if (time_valid) {
                int number_of_event = endTime - startTime;
                int index = startTime - start_time_of_day - 1;
                while (number_of_event > 0) {
                    if (schedule[room][index + number_of_event] != null) {
                        return false;
                    }
                    number_of_event -= 1;
                }
            }
        } catch (ArrayIndexOutOfBoundsException e) {
            return false;
        }
        return time_valid;

    }

    /**
     * This is the event to create event in our system at specific time and specific room
     *
     * @param title       the title of event
     * @param startTime   the start time of this event
     * @param endTime     the end time of this event
     * @param roomNumber  the room number of event
     * @param speakerName a list of speaker that is going to show up in this event
     * @param size        the size of this room
     * @param vip         this is a vip event or not
     */
    public void create_event(String title, int startTime, int endTime, Integer roomNumber, ArrayList<String> speakerName, int size, boolean vip) {
        int number_of_event = endTime - startTime;
        int index = startTime - start_time_of_day - 1;
        while (number_of_event > 0) {
            schedule[roomNumber][index + number_of_event] = new EventEntity(title, startTime, endTime, roomNumber, speakerName, size, vip);
            number_of_event -= 1;
        }

    }

    /**
     * This is the method to find if there is a event with the title we want at specific time and room number
     *
     * @param title      the title of this event we want to find
     * @param startTime  the start time of event we are looking for
     * @param roomNumber the room number of event the we are looking for
     */
    public EventEntity find_event(String title, int startTime, int roomNumber) {
        int column = end_time_of_day - start_time_of_day;
        for (int i = 0; i < room; i++) {
            for (int j = 0; j < column; j++) {
                EventEntity eventEntity = schedule[i][j];
                if (eventEntity != null && eventEntity.getTitle().equals(title) && eventEntity.getStartTime() == startTime && eventEntity.getRoomNumber() == roomNumber) {
                    return eventEntity;
                }
            }
        }
        return null;
    }

    /**
     * This is the method to cancel event user want to cancel at specific time and room number
     *
     * @param startTime  the start time of event user want to cancel
     * @param endTime    the end time of event user want to cancel
     * @param roomNumber the room number of event user want to cancel
     */

    public boolean cancel_event(int startTime, int endTime, int roomNumber) {
        int number_of_event = endTime - startTime;
        int index = startTime - start_time_of_day - 1;
        try {
            if (startTime < 9 || endTime > 17 || roomNumber > 20)
                return false;
            if (schedule[roomNumber][index + number_of_event] == null) {
                return false;
            } else {
                while (number_of_event > 0) {
                    schedule[roomNumber][index + number_of_event] = null;
                    number_of_event -= 1;
                }
                return true;
            }
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * This is the method to help speaker to find out what are the event they have
     *
     * @param speakerName the name of speaker
     */

    public ArrayList<String> speakerEventList(String speakerName) {
        ArrayList<String> list = new ArrayList<>();
        int column = end_time_of_day - start_time_of_day;
        for (int i = 0; i < room; i++) {
            for (int j = 0; j < column; j++) {
                if (schedule[i][j] != null) {
                    EventEntity eventEntity = schedule[i][j];
                    if (eventEntity.getSpeakerName().contains(speakerName)) {
                        list.add(eventEntity.getStartTime() + "-" + eventEntity.getEndTime() + " " + eventEntity.getTitle());
                    }
                }
            }
        }
        return list;
    }

    /**
     * This is the return the list of events our user signed for
     *
     * @param id the id of our user
     */
    public ArrayList<String> registerEventList(int id) {
        ArrayList<String> list = new ArrayList<>();
        int column = end_time_of_day - start_time_of_day;
        for (int i = 0; i < room; i++) {
            for (int j = 0; j < column; j++) {
                if (schedule[i][j] != null) {
                    EventEntity eventEntity = schedule[i][j];
                    if (eventEntity.getAttendeeList().contains(id)) {
                        list.add(eventEntity.getRoomNumber() + " " + eventEntity.getStartTime() + "-" + eventEntity.getEndTime() + " " + eventEntity.getTitle());
                    }
                }
            }
        }
        return list;
    }

    /**
     * This is the method for normal user to see the schedule of our conference
     *
     * @return the Arraylist that contains schedule information for normal attendees
     */
    public ArrayList<String> view() {
        ArrayList<String> a = new ArrayList<>();
        for (int i = 0; i < room; i++) {
            StringBuilder s = new StringBuilder("Room" + i + ": ");
            for (int j = 0; j < end_time_of_day - start_time_of_day; j++) {
                if (schedule[i][j] != null && !schedule[i][j].getVip()) {
                    s.append(schedule[i][j].getStartTime()).append("-").append(schedule[i][j].getEndTime()).append(" ").append(schedule[i][j].getTitle()).append(", ");
                }
            }
            a.add(s.toString());
        }
        return a;
    }

    /**
     * This is the method for our vip user to see the schedule of our conference
     *
     * @return the Arraylist that contains schedule information for vip attendees
     */
    public ArrayList<String> vipView() {
        ArrayList<String> a = new ArrayList<>();
        for (int i = 0; i < schedule.length; i++) {
            StringBuilder s = new StringBuilder("Room" + i + ": ");
            for (int j = 0; j < schedule[i].length; j++) {
                if (schedule[i][j] != null) {
                    s.append(schedule[i][j].getStartTime()).append("-").append(schedule[i][j].getEndTime()).append(" ").append(schedule[i][j].getTitle()).append(", ");
                }
            }
            a.add(s.toString());
        }
        return a;
    }
}
