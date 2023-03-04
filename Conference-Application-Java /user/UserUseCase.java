package user;


import java.util.ArrayList;

/**
 * A Use Case Class for User.
 */
public class UserUseCase {
    /**
     * A adder to add user to the system
     *
     * @param data     User data
     * @param userID   User ID
     * @param password User password
     * @param name     User name
     */
    public void addNewUser(UserEntity data, Integer userID, Integer password, String name) {
        ArrayList<Object> newUser = new ArrayList<>();
        newUser.add(userID);
        newUser.add(password);
        newUser.add(name);
        data.userData.add(newUser);
    }

    /**
     * @param data     User Entity
     * @param UserID   User ID
     * @param password User Password
     * @return a boolean determining if the user is in the system.
     */
    public boolean verifyUser(UserEntity data, Integer UserID, Integer password) {
        for (ArrayList<Object> user : data.getUserData()) {
            if (user.get(0).equals(UserID) && user.get(1).equals(password))
                return true;
        }
        return false;
    }

    /**
     * @param data   User Entity
     * @param UserID user ID
     * @return a boolean determining if the user's ID is in the system.
     */
    public boolean existsID(UserEntity data, Integer UserID) {
        for (ArrayList<Object> user : data.getUserData()) {
            if (user.get(0).equals(UserID))
                return true;
        }
        return false;
    }

    /**
     * @param data User Entity
     * @param name User ID
     * @return a boolean determining if the user's name is in the system.
     */
    public boolean existsName(UserEntity data, String name) {
        for (ArrayList<Object> user : data.getUserData()) {
            if (user.get(2).equals(name))
                return true;
        }
        return false;
    }


}