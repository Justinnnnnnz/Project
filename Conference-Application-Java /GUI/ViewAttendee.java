package GUI;

import javax.swing.*;

public class ViewAttendee extends ViewUser {
    JButton viewEvents;

    /**
     * Attendee
     * see a schedule
     * sign up for an event
     * cancel enrolment
     * see the schedule that they have signed up
     * send or receive messages with other attendees and speaker
     */
    public ViewAttendee() {

        super();
        frame.setTitle("Attendee");
        viewEvents = new JButton("View Schedule");
        viewEvents.addActionListener(e -> getPresenter().shiftToViewSchedule());

        JButton signupEvent = new JButton("Sign Up For Events");
        signupEvent.addActionListener(e -> getPresenter().shiftToSignupEvent());

        JButton cancel = new JButton("Cancel Enrolment");
        cancel.addActionListener(e -> getPresenter().shiftToCancel());

        JButton viewSchedule = new JButton("View Signed Up Events");
        viewSchedule.addActionListener(e -> getPresenter().shiftToSignedUpEvents());


        panel.add(viewEvents);
        panel.add(viewSchedule);
        panel.add(signupEvent);
        panel.add(cancel);

        frame.add(panel);
        frame.pack();
    }
}
