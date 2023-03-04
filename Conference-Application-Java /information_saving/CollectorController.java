package information_saving;

import message_system.MessageController;
import schedule_system.ScheduleSystem;
import user.UserEntity;

import java.io.Serializable;

/**
 * @author William Gao
 * A controller class that collects all the entites that are
 * needed to restore the conference. And this is the class that
 * will be serialized by Gateway.
 */
public class CollectorController implements Serializable {
    private static final long serialVersionUID = -2095916884810199532L;
    UserEntity UE;
    MessageController MC;
    ScheduleSystem SS;

    /**
     * @param UE Input UE
     * @param MC Input MC
     * @param SS Input SS
     */
    public CollectorController(UserEntity UE, MessageController MC, ScheduleSystem SS) {
        this.UE = UE;
        this.MC = MC;
        this.SS = SS;
    }

    /**
     * @return An UE object
     */
    public UserEntity getUE() {
        return UE;
    }

    /**
     * @return A MC object
     */
    public MessageController getMC() {
        return MC;
    }

    /**
     * @return A SS object
     */
    public ScheduleSystem getSS() {
        return SS;
    }
}
