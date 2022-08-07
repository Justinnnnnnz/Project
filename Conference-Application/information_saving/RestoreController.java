package information_saving;

import message_system.MessageController;
import schedule_system.ScheduleSystem;
import user.UserEntity;

/**
 * @author William Gao
 * A Controller class that restores information in the file
 * and update entites at the beginning of the program
 */
public class RestoreController {
    private final IGateway i = new Gateway();

    // reads in information as a collector via interface
    public CollectorController getCollector() {
        return i.read("phase2/saved_files/information.ser");
    }

    /**
     * A checker to check if UE is empty
     *
     * @return if UE is empty
     */
    public boolean UENotEmpty() {
        try {
            return getCollector().getUE() != null;

        } catch (NullPointerException e) {
            return false;
        }
    }

    /**
     * A checker to check if MC is empty
     *
     * @return if MC is empty
     */
    public boolean MCNotEmpty() {
        try {
            return getCollector().getMC() != null;

        } catch (NullPointerException e) {
            return false;
        }
    }

    /**
     * A checker to check if SS is empty
     *
     * @return if SS is empty
     */
    public boolean SSNotEmpty() {
        try {
            return getCollector().getSS() != null;

        } catch (NullPointerException e) {
            return false;
        }
    }

    /**
     * @return An UE object
     */
    public UserEntity getUE() {
        if (UENotEmpty())
            return getCollector().getUE();
        return new UserEntity();
    }

    /**
     * @return An MC object
     */
    public MessageController getMC() {
        if (MCNotEmpty())
            return getCollector().getMC();
        return new MessageController();
    }

    /**
     * @return An SS object
     */
    public ScheduleSystem getSS() {
        if (SSNotEmpty())
            return getCollector().getSS();
        return new ScheduleSystem();
    }

}
