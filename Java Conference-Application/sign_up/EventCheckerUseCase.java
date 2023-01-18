package sign_up;

import schedule_system.EventEntity;

/**
 * use case to check if the attendee can sign up for an event
 */
public class EventCheckerUseCase {
    /**
     * check if the attendee is in the event already or not
     *
     * @param id    the attendee that want to sign up for an event
     * @param eventEntity the event that is signed up to
     * @return true if attendee is in the event, false otherwise
     */
    public boolean attendeeCheck(int id, EventEntity eventEntity) {
        return eventEntity.getAttendeeList().contains(id);
    }

    /**
     * check if the event have any space left
     *
     * @param eventEntity the event that want to be checked
     * @return true if the size of event is smaller than two, false otherwise
     */
    public boolean sizeCheck(EventEntity eventEntity) {
        return eventEntity.getAttendeeList().size() < eventEntity.getSize();
    }
}
