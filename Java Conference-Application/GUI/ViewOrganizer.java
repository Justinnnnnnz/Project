package GUI;

import javax.swing.*;

public class ViewOrganizer extends ViewUser {
    /**
     * able to view the Organizer
     * create rooms.
     * create rooms and create accounts.
     * schedule speakers.
     * reschedule/cancel an event before it happens.
     * set event size.?
     * plan event/ create events.
     */
    public ViewOrganizer() {
        super();


        frame.setTitle("Organizer");
        JButton create_accounts = new JButton("Create Accounts");
        create_accounts.addActionListener(e -> getPresenter().createAccounts());
        JButton setup = new JButton("Set up Conference");
        setup.addActionListener(e -> getPresenter().setupConference());
        JButton create_events = new JButton("Create Events");
        create_events.addActionListener(e -> getPresenter().createEvent());
        JButton cancel_events = new JButton("Cancel Events");
        cancel_events.addActionListener(e -> getPresenter().cancelEvents());

        panel.add(create_accounts);
        panel.add(setup);
        panel.add(create_events);
        panel.add(cancel_events);

        frame.add(panel);
        frame.pack();
    }
}
