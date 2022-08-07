package sign_up;

import schedule_system.EventEntity;

import java.util.ArrayList;

/**
 * use case to cancel or add attendee to an event
 */
public class AddRemoveUseCase {
    /**
     * Add the attendee into the event
     *
     * @param eventEntity the event that is adding the attendee
     * @param id    the attendee's id that is added
     */
    public void add(int id, EventEntity eventEntity) {
        ArrayList<Integer> al = eventEntity.getAttendeeList();
        al.add(id);
        eventEntity.setAttendeeList(al);
    }

    /**
     * remove the attendee into the event
     *
     * @param eventEntity the event that is removing the attendee
     * @param id    the attendee's id that is removed
     */
    public void cancel(int id, EventEntity eventEntity) {
        ArrayList<Integer> al = eventEntity.getAttendeeList();
        al.remove((Integer) id);
        eventEntity.setAttendeeList(al);
    }

}
