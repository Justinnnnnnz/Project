package GUI;

import message_system.*;
import schedule_system.ScheduleSystem;
import sign_up.SignUpSystem;
import user.UserEntity;
import user.UserUseCase;
import information_saving.*;

import java.util.ArrayList;
import java.util.List;

public class Model implements IModel{
    MessageController MC;
    ScheduleSystem SS;
    UserEntity UE;
    UserUseCase US = new UserUseCase();
    SignUpSystem SU;
    ArrayList<Object> currentUser;
    boolean isCreating;

    /**
     * Reading variables from the files the program saves last time
     */
    public Model(){
        RestoreController restoreController = new RestoreController();
        this.UE = restoreController.getUE();
        this.MC = restoreController.getMC();
        this.SS = restoreController.getSS();
        this.SU = new SignUpSystem(SS.getScheduleUseCase());

    }

    /**
     * get HasSetConference content
     * @return whether Has Set Conference
     */
    @Override
    public boolean getHasSetConference() {
        return SS.getScheduleUseCase().getHasSetConference();
    }

    /**
     *  set up has conference
     * @param hasSetConference a bool determine whether has or not conference
     */
    @Override
    public void setHasSetConference(boolean hasSetConference) {
        SS.getScheduleUseCase().setHasSetConference(hasSetConference);
    }

    /**
     *
     * @return return whether is not creating
     */
    @Override
    public boolean getIsCreating() {
        return this.isCreating;
    }

    /**
     * set iscreating
     * @param isCreating whether is not creating
     */
    @Override
    public void setIsCreating(boolean isCreating) {
        this.isCreating = isCreating;
    }

    /**
     * add a new user
     * @param ID user's id
     * @param password user's password
     * @param name user's name
     */

    @Override
    public void addNewUsers(Integer ID, Integer password, String name)  {
        US.addNewUser(UE, ID, password, name);
    }

    /**
     * vertify user's id and pass
     * @param ID user's id
     * @param password user's password
     * @return bool reutrn whether is or not user
     */

    @Override
    public boolean verifyUser(Integer ID, Integer password) {
        return US.verifyUser(UE, ID, password);
    }

    /**
     * return a bool whether id exist
     * @param ID user id
     * @return a bool whether id exist
     */
    @Override

    public boolean existsID(Integer ID){
        return US.existsID(UE, ID);
    }

    /**
     *
     * @return a list of user
     */
    @Override
    public ArrayList<ArrayList<Object>> getUsers() {
        return UE.getUserData();
    }

    /**
     *
     * @return return list of cur user
     */

    @Override
    public ArrayList<Object> getCurrentUser() {
        return currentUser;
    }

    /**
     * set up a list of users
     * @param currentUser cur list of users
     */
    @Override
    public void setCurrentUser(ArrayList<Object> currentUser) {
        this.currentUser = currentUser;
    }

    /**
     * send a message
     * @param senderID sender's id
     * @param receiverID    receiver's id
     * @param content message content
     * @return return whether msg is sent or not
     */
    public boolean sendMessage(Integer senderID, String receiverID, String content){
        return MC.writeMessage(senderID, receiverID, content, US, UE);
    }

    /**
     *
     * @param userID user's id
     * @return return list of schedule
     */
    @Override
    public ArrayList<String> getSchedule(String userID) {
        return SS.view_schedule(userID);
    }

    /**
     *
     * @param userID user's id
     * @return return received message
     */

    public List<String> getReceivedMessage(Integer userID){
        return MC.viewMessage(userID);
    }

    /**
     *
     * @return return a collectuor
     */

    @Override
    public CollectorController getCollector() {
        return new CollectorController(UE, MC, SS);
    }

    /**
     *
     * @param choice a choice to mark or not
     * @return whether have a choice
     */
    @Override
    public boolean markMessage(String choice) {
        return MC.alterReadStatus(choice);
    }

    /**
     *
     * @param userID user's id
     * @param title user's title
     * @param starttime start time
     * @param roomnumber room number
     * @return return whether or not signed up
     */
    public boolean signup(Integer userID, String title, Integer starttime, Integer roomnumber){
        return SU.signUp(userID, title, starttime, roomnumber);
    }

    /**
     *
     * @param userID user's id
     * @return return a list of signed up event
     */

    public ArrayList<String> viewSignUpEvent(Integer userID){
        return SS.viewSignupEvent(userID);
    }

    /**
     *
     * @param userID user's id
     * @param title title
     * @param starttime start time
     * @param roomnumber room number
     * @return return whether or not canceled
     */

    public Boolean cancel(Integer userID, String title, Integer starttime, Integer roomnumber){
        return SU.cancel(userID, title, starttime, roomnumber);
    }

    /**
     *
     * @param start start time
     * @param end end time
     * @param roomNumber room number
     * @return whether or not setted a conference
     */
    @Override
    public boolean setConference(String start, String end, String roomNumber) {
        return SS.setConference(start,end,roomNumber);
    }

    /**
     *
     * @param title title
     * @param startTime start time of conference
     * @param endTime end time
     * @param roomNumber conference room number
     * @param speakerName speaker name
     * @param size size of conference
     * @param vip whether vip
     * @return whether or not created
     */

    @Override
    public boolean createEvent(String title, String startTime, String endTime, String roomNumber, String speakerName,String size,String vip) {
        return SS.create_event(title,startTime,endTime,roomNumber,speakerName,size,vip);
    }

    /**
     *
     * @param name name
     * @return return name
     */
    @Override
    public boolean existsName(String name) {
        return US.existsName(UE, name);
    }

    /**
     *
     * @param name talk name
     * @return return talk's name
     */

    @Override
    public ArrayList<String> viewTalks(String name) {
        return SS.viewTalks(name);
    }

    /**
     *
     * @param text message sent
     * @return return whether msg is sent
     */

    public boolean speakerSend(String text){
        return MC.speakerSendToAll((Integer) currentUser.get(0), text, UE);
    }

    /**
     *
     * @param starttime start time
     * @param endtime end time
     * @param roomnumber room number
     * @return return whether or not canceled
     */
    @Override
    public boolean cancelEvent(Integer starttime, Integer endtime, Integer roomnumber) {
        return SS.cancel_event(starttime, endtime, roomnumber);
    }

    /**
     *
     * @param names speaker's name
     * @return whether or not all speaker name is valid
     */
    @Override
    public boolean allSpeakerNameValid(String names) {
        for (String each : names.trim().split(" ")) {
            if (!this.existsName(each)) {

                return false;
            }
        }
        return true;
    }
}