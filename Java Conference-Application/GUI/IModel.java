package GUI;

import  information_saving.CollectorController;


import java.util.ArrayList;
import java.util.List;

public interface IModel {
    void addNewUsers(Integer ID, Integer password, String name);

    boolean verifyUser(Integer ID, Integer password);

    boolean existsID(Integer ID);

    ArrayList<ArrayList<Object>> getUsers();

    ArrayList<Object> getCurrentUser();

    void setCurrentUser(ArrayList<Object> user);

    ArrayList<String> getSchedule(String userID);

    List<String> getReceivedMessage(Integer userID);

    boolean sendMessage(Integer senderID, String receiverID, String content);

    boolean markMessage(String choice);

    CollectorController getCollector();

    boolean createEvent(String title, String startTime, String endTime, String roomNumber, String speakerName, String size, String vip);

    boolean getHasSetConference();

    void setHasSetConference(boolean hasSetConference);

    void setIsCreating(boolean isCreating);

    boolean getIsCreating();

    boolean setConference(String start, String end, String roomNumber);

    boolean signup(Integer userID, String title, Integer starttime, Integer roomnumber);

    ArrayList<String> viewSignUpEvent(Integer userID);

    Boolean cancel(Integer userID, String title, Integer starttime, Integer roomnumber);

    boolean existsName(String name);

    ArrayList<String> viewTalks(String name);

    boolean speakerSend(String text);

    boolean cancelEvent(Integer starttime, Integer endtime, Integer roomnumber);

    boolean allSpeakerNameValid(String names);

}
