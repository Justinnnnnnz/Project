package schedule_system;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;

public class ScheduleSystem implements Serializable {
    private static final long serialVersionUID = -2095916884810199532L;
    private final ScheduleUseCase scheduleUseCase;


    /**
     * constructor of our schedule system
     */
    public ScheduleSystem()  {
        scheduleUseCase = new ScheduleUseCase();
    }

    /**
     * getter to get our usecase
     */

    public ScheduleUseCase getScheduleUseCase() {
        return scheduleUseCase;
    }


    /**
     * after check this event can held at specific room and event, create a event by adding it to schedule of conference
     * and event list of speaker
     *
     * @param title       the title of event
     * @param startTime   the  time event start
     * @param endTime     the endTime of event
     * @param roomNumber  the room number  the event will take place
     * @param speakerName the name of the speaker who are going to give a talk
     */
    public boolean create_event(String title, String startTime, String endTime, String roomNumber, String speakerName, String size, String vip) {
        try {
            int start = Integer.parseInt(startTime);
            int end = Integer.parseInt(endTime);
            int room = Integer.parseInt(roomNumber);
            int size_ = Integer.parseInt(size);
            boolean vip_ = vip.equals("yes");
            ArrayList<String> speaker = new ArrayList<>();
            Collections.addAll(speaker, speakerName.trim().split(" "));

            if (scheduleUseCase.check_schedule(room, start, end)) {
                scheduleUseCase.create_event(title, start, end, room, speaker, size_, vip_);
                return true;
            } else {
                return false;
            }
        } catch (NumberFormatException e) {
            return false;
        }
    }

    /**
     * setter to set the start time, end time and how many room we have for our conference
     *
     * @param start_time  the start time of conference
     * @param end_time    the end time of conference
     * @param room_number how many room we have
     */
    public boolean setConference(String start_time, String end_time, String room_number) {
        return this.getScheduleUseCase().scheduleModifier(start_time, end_time, room_number);
    }

    /**
     * give the schedule of conference
     */
    public EventEntity[][] get_schedule() {
        return scheduleUseCase.get_schedule();
    }

    /**
     * cancel event at specific time and room number
     *
     * @param startTime  the start time of event we want to cancel
     * @param endTime    the end time of event we want to cancel
     * @param roomNumber the room number of event we want to cancel
     */
    public boolean cancel_event(int startTime, Integer endTime, Integer roomNumber) {
        return scheduleUseCase.cancel_event(startTime, endTime, roomNumber);
    }

    /**
     * return the Arraylist that contains schedule information depends on vip user or not
     *
     * @param id the user's id
     * @return the Arraylist that contains schedule information
     */
    public ArrayList<String> view_schedule(String id) {
        if (Integer.parseInt(id.substring(0, 1)) == 9) {
            return scheduleUseCase.vipView();
        }
        return scheduleUseCase.view();
    }

    /**
     * to find the event at specific time and specific roomnumber
     *
     * @param title      the title of event we are looking for
     * @param startTime  the start time of event we are looking for
     * @param roomNumber the room number of event we are looking for
     */
    public EventEntity find_event(String title, int startTime, int roomNumber) {
        return scheduleUseCase.find_event(title, startTime, roomNumber);
    }

    /**
     * return list of event's title this user signed up for
     *
     * @param userID the id of this user
     */
    public ArrayList<String> viewSignupEvent(Integer userID) {
        return scheduleUseCase.registerEventList(userID);
    }

    /**
     * return list of event's title this speaker going to give a talk
     *
     * @param name the name of speaker
     */
    public ArrayList<String> viewTalks(String name) {
        return scheduleUseCase.speakerEventList(name);
    }

}
