package sign_up;

import schedule_system.ScheduleUseCase;

/**
 * Controller class for sign up
 */
public class SignUpSystem {
    private AddRemoveUseCase addRemoveUserCase = new AddRemoveUseCase();
    private EventCheckerUseCase eventCheckerController = new EventCheckerUseCase();
    private ScheduleUseCase su;

    public SignUpSystem(ScheduleUseCase su) {
        this.su = su;
    }

    /**
     * allow user to sign up
     *
     * @param id         the id of attendee who wants to sign up
     * @param title      the event's title that is signed up
     * @param startTime  the event's start time
     * @param roomNumber the event's room
     * @return boolean true if sign up success, false otherwise
     */
    public boolean signUp(int id, String title, int startTime, int roomNumber) {
        if (su.find_event(title, startTime, roomNumber) == null) {
            return false;
        } else if (su.find_event(title, startTime, roomNumber).getVip() && Integer.toString(id).charAt(0) != '9') {
            return false;
        } else if (eventCheckerController.attendeeCheck(id, su.find_event(title, startTime, roomNumber))) {
            return false;
        } else if (!eventCheckerController.sizeCheck(su.find_event(title, startTime, roomNumber))) {
            return false;
        } else {
            addRemoveUserCase.add(id, su.find_event(title, startTime, roomNumber));
            return true;
        }
    }


    /**
     * allow attendees to cancel the event they signed up
     *
     * @param id         the attendee's id
     * @param title      the event's title that is cancelling
     * @param startTime  the event's start time
     * @param roomNumber the event's room
     * @return true if cancel success, false otherwise
     */
    public boolean cancel(int id, String title, int startTime, int roomNumber) {
        if (su.find_event(title, startTime, roomNumber) == null) {
            return false;
        } else if (eventCheckerController.attendeeCheck(id, su.find_event(title, startTime, roomNumber))) {
            addRemoveUserCase.cancel(id, su.find_event(title, startTime, roomNumber));
            return true;
        } else {
            return false;
        }
    }
}
