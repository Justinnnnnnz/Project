package GUI;

public interface IPresenter {
    void login();

    void shiftToSignup();

    void shiftToLogin();

    void shiftToViewMessage();

    void shiftToUserPage(Integer ID);

    void shiftToSendMessage();

    void shiftToViewSchedule();

    void shiftToSignupEvent();

    void shiftToCancel();

    void shiftToSignedUpEvents();

    void createAccounts();

    void signup();

    void setModel(IModel IModel);

    void setMenu(IMainMenu IMainMenu);

    void setIViewUser(IViewUser IViewUser);

    void shiftToMarkMessage();

    void setupConference();

    void back(IPopupWindow window);

    void createEvent();

    void run();

    void exit();

    void viewTalks();

    void sendMessageToAllAttendee();

    void cancelEvents();
}
