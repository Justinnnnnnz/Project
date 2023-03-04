package GUI;

import javax.swing.*;

public class ViewSpeaker extends ViewUser {
    /**
     * Speaker
     * see a list of talks that they are giving
     * message all attendees at once or individually.
     */
    public ViewSpeaker() {

        super();
        frame.setTitle("Speaker");
        JButton view_given_talks = new JButton("View Given Talks");
        view_given_talks.addActionListener(e -> getPresenter().viewTalks());
        JButton message_all_attendees = new JButton("Message All Attendees");
        message_all_attendees.addActionListener(e -> getPresenter().sendMessageToAllAttendee());

        panel.add(view_given_talks);
        panel.add(message_all_attendees);

        frame.add(panel);
        frame.pack();
    }
}
