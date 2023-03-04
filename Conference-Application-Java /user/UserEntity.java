package user;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * The entity class for all User.
 * Each user has 3 elements: Integer ID, Integer password and String name.
 */
public class UserEntity implements Serializable {
    private static final long serialVersionUID = -2095916884810199532L;

    protected ArrayList<ArrayList<Object>> userData;

    public UserEntity() {
        this.userData = new ArrayList<>();
    }

    /**
     * A getter for this entity
     *
     * @return return User data entity
     */
    public ArrayList<ArrayList<Object>> getUserData() {
        return userData;
    }


    /**
     * @return Returns the attendee list
     */
    public ArrayList<ArrayList<Object>> getAttendeeList() {
        ArrayList<ArrayList<Object>> attendees = new ArrayList<>();
        for (ArrayList<Object> user : userData) {
            if (Integer.parseInt(user.get(0).toString().substring(0, 1)) == 2) {
                attendees.add(user);
            }
        }
        return attendees;
    }
}
