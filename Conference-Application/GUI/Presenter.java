package GUI;

import information_saving.Gateway;
import information_saving.IGateway;


import javax.swing.*;
import java.util.ArrayList;
import java.util.List;

public class Presenter implements IPresenter {
    /**
     * GUI Presenter class
     */

    private IModel IModel;
    private IMainMenu IMainMenu;
    private IViewUser IViewUser;
    private IPopupWindow IPopupWindow;

    /**
     * set up the Model Class
     *
     * @param IModel content model
     */

    public void setModel(IModel IModel) {
        this.IModel = IModel;
    }

    /**
     * set the window
     *
     * @param IPopupWindow pop up window
     */
    public void setWindow(IPopupWindow IPopupWindow) {
        this.IPopupWindow = IPopupWindow;
    }

    /**
     * the window to allow user to login to the system
     */
    public void login() {
        Object[] userInput = IMainMenu.returnUserInput();
        if (userInput.length == 0) {
            IMainMenu.displayErrorMessage();
        } else {
            Integer inputID = (Integer) userInput[0];
            Integer inputPassword = (Integer) userInput[1];
            if (IModel.verifyUser(inputID, inputPassword)) {
                IMainMenu.close();
                for (ArrayList<Object> user : IModel.getUsers()) {
                    if (user.get(0).equals(inputID)) {
                        IModel.setCurrentUser(user);
                    }
                }
                shiftToUserPage(inputID);
            } else {
                IMainMenu.displayErrorMessage();
            }
        }
    }

    /**
     * shift to sign up GUI window
     */
    public void shiftToSignup() {
        IMainMenu signupMenu = new ViewSignup();
        signupMenu.setPresenter(this);
        this.IMainMenu.close();
        this.setMenu(signupMenu);
    }

    /**
     * sign up process GUI window
     */

    public void signup() {
        Object[] userInput = IMainMenu.returnUserInput();
        if (userInput.length == 0) {
            IMainMenu.displayErrorMessage();
        } else {
            Integer inputID = (Integer) userInput[0];
            Integer inputPassword = (Integer) userInput[1];
            String name = (String) userInput[3];
            boolean start_with_three = (Integer.parseInt(Integer.toString(inputID).substring(0, 1)) == 3);
            if (IModel.existsID(inputID) || IModel.existsName(name) && start_with_three) {
                IMainMenu.displayErrorMessage();
            } else {
                IModel.addNewUsers(inputID, inputPassword, name);
                IMainMenu.close();
                if (IModel.getIsCreating()) {
                    IModel.setIsCreating(false);
                    this.shiftToUserPage((Integer) IModel.getCurrentUser().get(0));
                } else {
                    IMainMenu back = new ViewLogin();
                    back.setPresenter(this);
                    this.setMenu(back);
                }
            }
        }
    }

    /**
     * shift to user GUI page
     *
     * @param inputID input's id
     */
    public void shiftToUserPage(Integer inputID) {
        shift(inputID);
        IMainMenu.close();
    }

    /**
     * shift
     *
     * @param inputID input id
     */


    public void shift(Integer inputID) {
        //helper function
        Integer first = Integer.parseInt(inputID.toString().substring(0, 1));
        if (first.equals(9)) {
            ViewUser VIPUser = new ViewVIP();
            VIPUser.setPresenter(this);
            this.setIViewUser(VIPUser);
        } else if (first.equals(1)) {
            ViewUser organizer = new ViewOrganizer();
            organizer.setPresenter(this);
            this.setIViewUser(organizer);
        } else if (first.equals(2)) {
            ViewUser attendee = new ViewAttendee();
            attendee.setPresenter(this);
            this.setIViewUser(attendee);
        } else if (first.equals(3)) {
            ViewUser speaker = new ViewSpeaker();
            speaker.setPresenter(this);
            this.setIViewUser(speaker);
        }
    }

    /**
     * shift to login GUI window
     */
    @Override
    public void shiftToLogin() {
        IViewUser.close();
        IMainMenu back = new ViewLogin();
        back.setPresenter(this);
        this.setMenu(back);
    }

    /**
     * shift to view message GUI window
     */
    public void shiftToViewMessage() {
        this.IViewUser.close();
        PopupWindow viewMessage = new PopupWindow();
        viewMessage.setTitle("View Message");
        viewMessage.addLabel("Please Remember The Sequence Numbers (right after #) of the messages");
        viewMessage.addLabel("that You Want To Alter Their Status by using Mark Messages Read/Unread.");
        viewMessage.addLabel("These Are The Messages You Received:");
        List<String> messageList = IModel.getReceivedMessage((Integer) IModel.getCurrentUser().get(0));
        for (String message : messageList) {
            viewMessage.addLabel(message);
        }
        viewMessage.addBackButton(viewMessage);
        viewMessage.setPresenter(this);
    }

    /**
     * shift to send message GUI
     */
    public void shiftToSendMessage() {

        this.IViewUser.close();
        PopupWindow sendMessage = new PopupWindow();
        sendMessage.setPresenter(this);
        sendMessage.setTitle("Send Message!");
        sendMessage.addLabel("Who Do You Want To Send Message, Enter his/her User ID and The Content");
        sendMessage.addLabel("You Can Send this Message to Multiple Users, Use Space to Separate Their IDs ");
        JTextField userID = sendMessage.addTextField();
        JTextField content = sendMessage.addTextField();
        JButton send = sendMessage.addButton("Send!");
        send.addActionListener(e -> shift1((Integer) IModel.getCurrentUser().get(0), userID, content));
        sendMessage.addBackButton(sendMessage);
    }

    /**
     * shift
     *
     * @param senderID send's id
     * @param userID   user's id
     * @param content1 content
     */
    public void shift1(Integer senderID, JTextField userID, JTextField content1) {
        boolean success = IModel.sendMessage(senderID, userID.getText(), content1.getText());
        if (success) {
            IViewUser.successMessage();
        } else {
            IViewUser.displayErrorMessage();
        }
    }

    /**
     * shift to view schedule GUI window
     */

    @Override
    public void shiftToViewSchedule() {

        this.IViewUser.close();
        PopupWindow viewSchedule = new PopupWindow();
        setWindow(viewSchedule);
        viewSchedule.setPresenter(this);
        viewSchedule.setTitle("View Schedule");
        viewSchedule.addLabel("If you want to sign up Event, ");
        viewSchedule.addLabel("please remember its title, start time, and room number");
        viewSchedule.addLabel("Here Is The Schedule Of The Conference:");
        try {
            ArrayList<String> schedule = IModel.getSchedule(Integer.toString((Integer) IModel.getCurrentUser().get(0)));

            for (String row : schedule) {
                viewSchedule.addLabel(row);
            }
        } catch (Exception e) {
            this.IPopupWindow.showMessageDialog("No Schedule Yet.","The Conference Has Not Been Set Up Yet, Please Wait Or Contact The Organizers.",false);
        }
        viewSchedule.addBackButton(viewSchedule);
    }

    /**
     * shift to sign up event GUI window
     */
    @Override
    public void shiftToSignupEvent() {

        this.IViewUser.close();
        PopupWindow signupEvent = new PopupWindow();
        setWindow(signupEvent);
        signupEvent.setPresenter(this);
        signupEvent.addLabel("Which Event Do You Want To Sign Up, Enter The Title Of The Event:");
        JTextField title = signupEvent.addTextField();
        signupEvent.addLabel("Enter The Start Time Of The Event:");
        JTextField startTime = signupEvent.addTextField();
        signupEvent.addLabel("Enter The Room Number Of The Event:");
        JTextField roomnumber = signupEvent.addTextField();
        JButton signUp = signupEvent.addButton("Sign Up!");
        signUp.addActionListener(e -> this.signupEvent((Integer) IModel.getCurrentUser().get(0),
                title, startTime, roomnumber));
        signupEvent.addBackButton(signupEvent);
    }

    /**
     * sign up event GUI interface
     *
     * @param userID     user's is
     * @param title      title
     * @param starttime  start time of event
     * @param roomnumber room number
     */
    public void signupEvent(Integer userID, JTextField title, JTextField starttime, JTextField roomnumber) {
        try {
            String t = title.getText();
            Integer s = Integer.parseInt(starttime.getText());
            Integer r = Integer.parseInt(roomnumber.getText());
            boolean success = IModel.signup(userID, t, s, r);
            if (success) {
                this.IPopupWindow.showMessageDialog("Success", "Signup Successful", true);
            } else {
                this.IPopupWindow.showMessageDialog("Please try again", "Invalid input or The Event Is Not Exist.", false);

            }
        } catch (Exception e) {
            this.IPopupWindow.showMessageDialog("Please try again", "Invalid input or The Event Is Not Exist.", false);

        }
    }

    /**
     * shift to cancel GUI interface
     */

    @Override
    public void shiftToCancel() {
        this.IViewUser.close();
        PopupWindow cancel = new PopupWindow();
        setWindow(cancel);
        cancel.setPresenter(this);
        cancel.setTitle("Cancel Enrolment");
        cancel.addLabel("Which Event Do You Want To Cancel, Enter The Title Of The Event:");
        JTextField title = cancel.addTextField();
        cancel.addLabel("Enter The Start Time Of The Event:");
        JTextField startTime = cancel.addTextField();
        cancel.addLabel("Enter The Room Number Of The Event:");
        JTextField roomnumber = cancel.addTextField();
        JButton cancelButton = cancel.addButton("Confirm!");
        cancelButton.addActionListener(e -> cancelevent((Integer) IModel.getCurrentUser().get(0), title,
                startTime, roomnumber));
        cancel.addBackButton(cancel);
    }

    /**
     * cancel event
     *
     * @param userID     user's id
     * @param title      tile
     * @param starttime  start time of conference
     * @param roomnumber room number of conference
     */

    public void cancelevent(Integer userID, JTextField title, JTextField starttime, JTextField roomnumber) {
        try {
            String t = title.getText();
            Integer s = Integer.parseInt(starttime.getText());
            Integer r = Integer.parseInt(roomnumber.getText());
            Boolean success = IModel.cancel(userID, t, s, r);
            if (success) {
                this.IPopupWindow.showMessageDialog("Success!", "Cancel Successful!", true);

            } else {
                this.IPopupWindow.showMessageDialog("Please try again", "Invalid input or The Event Is Not Exist.", false);
            }
        } catch (NumberFormatException e) {
            this.IPopupWindow.showMessageDialog("Please try again", "Invalid input or The Event Is Not Exist.", false);

        }
    }

    /**
     * shift to GUI interface of signed up events
     */

    @Override
    public void shiftToSignedUpEvents() {
        this.IViewUser.close();
        PopupWindow signedupEvents = new PopupWindow();
        setWindow(signedupEvents);
        signedupEvents.setTitle("Signed Up Events.");
        signedupEvents.setPresenter(this);
        signedupEvents.addLabel("These Are The Event Title You Have Signed Up:");
        signedupEvents.addLabel("Each row is arranged as Room Number Star Time-End Time Title.");
        ArrayList<String> eventList = IModel.viewSignUpEvent((Integer) IModel.getCurrentUser().get(0));
        for (String title : eventList) {
            signedupEvents.addLabel(title);
        }
        signedupEvents.addBackButton(signedupEvents);
    }

    /**
     * shift to mark messgae
     */

    public void shiftToMarkMessage() {
        this.IViewUser.close();
        PopupWindow markMessage = new PopupWindow();
        setWindow(markMessage);
        markMessage.setPresenter(this);
        markMessage.setTitle("Mark Message");
        markMessage.addLabel("Which Messages Do You Want To Alter Status?");
        markMessage.addLabel("The Message will Change To UNREAD If It Was READ.");
        markMessage.addLabel("The Message will Change To UNREAD If It Was READ.");
        markMessage.addLabel("Note that You Need To View Messages Before Altering Status.");
        markMessage.addLabel("Please Type the Sequence Numbers of the message.");
        markMessage.addLabel("Separate them by ONLY ONE Space!");
        JTextField number = markMessage.addTextField();
        JButton confirm = markMessage.addButton("Confirm!");
        confirm.addActionListener(e -> this.markMessage(number));
        markMessage.addBackButton(markMessage);
    }

    /**
     * mark a message
     *
     * @param number number of messgae marked
     */
    public void markMessage(JTextField number) {
        boolean success = IModel.markMessage(number.getText());
        if (success) {
            this.IPopupWindow.showMessageDialog("Success", "Mark Successful!", true);
        } else {
            this.IPopupWindow.showMessageDialog("Please try again", "Wrong input format Or The Message(s) is/are not Exist.", false);
        }
    }

    /**
     * create user account for
     */
    @Override
    public void createAccounts() {
        IModel.setIsCreating(true);
        this.IViewUser.close();
        this.shiftToSignup();
    }

    /**
     * set up a conference
     */
    @Override
    public void setupConference() {
        IViewUser.close();
        PopupWindow setConference = new PopupWindow();
        setWindow(setConference);
        setConference.setTitle("Set Conference");
        setConference.setPresenter(this);
        setConference.addLabel("Please Set the Start Time, End Time, and Room Numbers for This Conference.");
        setConference.addLabel("The Conference can start at 9 at the earliest and end at 17 at the latest.");
        setConference.addLabel("This Conference Has A Maximum of 20 Rooms.");
        setConference.addLabel("Please Note You Can Only Set Up Conference Once.");
        setConference.addLabel("Please Enter the Start Time in 24 Hour Time ");
        JTextField start_time = setConference.addTextField();
        setConference.addLabel("Please Enter the End Time in 24 Hour Time");
        JTextField end_time = setConference.addTextField();
        setConference.addLabel("Please Enter the Number of Rooms");
        JTextField room_number = setConference.addTextField();
        JButton confirm = setConference.addButton("Confirm!");
        confirm.addActionListener(e -> this.checkSetConference(start_time, end_time, room_number));
        setConference.addBackButton(setConference);
    }

    /**
     * check if setted conference
     *
     * @param start_time  start time of conference
     * @param end_time    end time of conference
     * @param room_number room number of conference
     */

    public void checkSetConference(JTextField start_time, JTextField end_time, JTextField room_number) {

        String start = start_time.getText();
        String end = end_time.getText();
        String room = room_number.getText();
        if (IModel.setConference(start, end, room) && !IModel.getHasSetConference()) {
            IModel.setHasSetConference(true);
            this.IPopupWindow.showMessageDialog("Success", "Set Conference Successful.", true);
        } else {
            this.IPopupWindow.showMessageDialog("Please try again", "Incorrect Input or the Conference has already been set", false);

        }
    }

    /**
     * create event on GUI
     */
    public void createEvent() {
        IViewUser.close();
        PopupWindow createEvent = new PopupWindow();
        setWindow(createEvent);
        createEvent.setTitle("Create an Event");
        createEvent.setPresenter(this);
        createEvent.addLabel("Please Enter the Title of the Event");
        JTextField title = createEvent.addTextField();
        createEvent.addLabel("Please Enter the Start Time of the Event");
        JTextField start_time = createEvent.addTextField();
        createEvent.addLabel("Please Enter the End Time of the Event");
        JTextField end_time = createEvent.addTextField();
        createEvent.addLabel("Please Enter the Room Number of the Event");
        JTextField room_number = createEvent.addTextField();
        createEvent.addLabel("Please Enter the Names of Speakers(Separate by space) of the Event");
        JTextField speakers = createEvent.addTextField();
        createEvent.addLabel("Please Enter the Size of the Event");
        JTextField size = createEvent.addTextField();
        createEvent.addLabel("Is this a VIP Event? (yes/no)");
        JTextField isVIP = createEvent.addTextField();
        JButton confirm = createEvent.addButton("Confirm!");
        confirm.addActionListener(e -> this.checkCreateEvent(title, start_time, end_time, room_number, speakers, size, isVIP));
        createEvent.addBackButton(createEvent);
    }

    /**
     * check if create event
     *
     * @param title       title
     * @param start_time  start time of event
     * @param end_time    end time of event
     * @param room_number room number of event
     * @param speakers    speaker
     * @param size        size of event
     * @param isVIP       whether or not vip
     */

    public void checkCreateEvent(JTextField title, JTextField start_time, JTextField end_time, JTextField room_number,
                                 JTextField speakers, JTextField size, JTextField isVIP) {
        String title_ = title.getText();
        String start_time_ = start_time.getText();
        String end_time_ = end_time.getText();
        String room_number_ = room_number.getText();
        String speakers_ = speakers.getText();
        String size_ = size.getText();
        String isVIP_ = isVIP.getText();
        if (IModel.allSpeakerNameValid(speakers_) && IModel.createEvent(title_, start_time_, end_time_, room_number_, speakers_, size_, isVIP_)) {
            this.IPopupWindow.showMessageDialog("Success", "Create Event Successful.", true);
        } else {
            this.IPopupWindow.showMessageDialog("Please try again", "Incorrect Input", false);

        }

    }

    /**
     * view talks in GUI
     */
    public void viewTalks() {
        IViewUser.close();
        PopupWindow viewTalks = new PopupWindow();
        setWindow(viewTalks);
        viewTalks.setPresenter(this);
        viewTalks.setTitle("View Talks");
        viewTalks.addLabel("These Are Your Talks:");
        ArrayList<String> talks = IModel.viewTalks((String) IModel.getCurrentUser().get(2));
        for (String talk : talks) {
            viewTalks.addLabel(talk);
        }
        viewTalks.addBackButton(viewTalks);
    }

    /**
     * sent message to all attendee
     */
    public void sendMessageToAllAttendee() {
        IViewUser.close();
        PopupWindow sendmessage = new PopupWindow();
        setWindow(sendmessage);
        sendmessage.setPresenter(this);
        sendmessage.setTitle("Send Message to All Attendees");
        sendmessage.addLabel("Enter Your Message:");
        JTextField text = sendmessage.addTextField();
        JButton send = sendmessage.addButton("Send!");
        send.addActionListener(e -> send(text));
        sendmessage.addBackButton(sendmessage);
    }

    /**
     * sent message
     *
     * @param text message text
     */

    public void send(JTextField text) {
        String t = text.getText();
        boolean success = IModel.speakerSend(t);
        if (success) {
            this.IPopupWindow.showMessageDialog("Success", "Send Message to ALL Attendees Successful.", true);
        } else {
            this.IPopupWindow.showMessageDialog("Please try again", "No Empty Content Please.", false);

        }
    }

    /**
     * cancel events
     */
    public void cancelEvents() {
        IViewUser.close();
        PopupWindow cancel = new PopupWindow();
        setWindow(cancel);
        cancel.setTitle("Cancel Events");
        cancel.setPresenter(this);
        cancel.addLabel("Which event Do you want to Cancel, Please enter its start time:");
        JTextField starttime = cancel.addTextField();
        cancel.addLabel("Please Enter its End Time:");
        JTextField endtime = cancel.addTextField();
        cancel.addLabel("Please Enter its Room Number:");
        JTextField room = cancel.addTextField();
        JButton confirm = cancel.addButton("Confirm");
        confirm.addActionListener(e -> cancel(starttime, endtime, room));
        cancel.addBackButton(cancel);
    }

    /**
     * cancel the progress
     *
     * @param startTime  startTime of conference
     * @param endTime    endTime of conference
     * @param roomNumber roomNumber of conference
     */

    public void cancel(JTextField startTime, JTextField endTime, JTextField roomNumber) {
        try {
            Integer s = Integer.parseInt(startTime.getText());
            Integer e = Integer.parseInt(endTime.getText());
            Integer r = Integer.parseInt(roomNumber.getText());
            boolean success = IModel.cancelEvent(s, e, r);
            if (success) {
                this.IPopupWindow.showMessageDialog("Success!", "Cancel Successful!", true);

            } else {
                this.IPopupWindow.showMessageDialog("Please try again", "Invalid input or The Event Is Not Exist.", false);

            }
        } catch (NumberFormatException e) {
            this.IPopupWindow.showMessageDialog("Please try again", "Invalid input or The Event Is Not Exist.", false);

        }
    }

    /**
     * set menu
     *
     * @param IMainMenu main menu
     */
    public void setMenu(IMainMenu IMainMenu) {
        this.IMainMenu = IMainMenu;
    }

    /**
     * set Iview user
     *
     * @param IViewUser iview user
     */

    public void setIViewUser(IViewUser IViewUser) {
        this.IViewUser = IViewUser;
    }

    /**
     * go back
     *
     * @param window window
     */
    @Override
    public void back(IPopupWindow window) {
        setWindow(window);
        IPopupWindow.close();
        shift((Integer) IModel.getCurrentUser().get(0));
        window.setPresenter(this);
    }

    /**
     * run the program
     */

    public void run() {
        IMainMenu.setPresenter(this);
    }

    /**
     * exit the program
     */

    @Override
    public void exit() {
        IMainMenu.close();
        PopupWindow exit = new PopupWindow();
        exit.exit();
        IGateway IGateway = new Gateway();
        IGateway.save(IModel.getCollector());
        System.exit(0);
    }
}

