package information_saving;

import java.io.*;

/**
 * @author William Gao
 * A gateway class that is responsible for saving
 * and reading the Collector class
 */
public class Gateway implements IGateway {

    /**
     * A method that saves the collector class
     * it receives or prints stack trace when
     * encountered an IOE exception.
     *
     * @param collectorController An instance of Collector
     */
    public void save(CollectorController collectorController) {
        try {
            FileOutputStream fileOut =
                    new FileOutputStream("phase2/saved_files/information.ser");
            ObjectOutputStream out = new ObjectOutputStream(fileOut);
            out.writeObject(collectorController);
            out.close();
            fileOut.close();
        } catch (IOException i) {
            i.printStackTrace();
        }
    }

    /**
     * A method that reads a in .ser file returning a
     * Collector object.
     *
     * @param path The string representation of file path
     * @return A Collector object in the file
     */
    public CollectorController read(String path) {
        try {
            InputStream file = new FileInputStream(path);
            InputStream buffer = new BufferedInputStream(file);
            ObjectInput input = new ObjectInputStream(buffer);

            CollectorController tempObject = (CollectorController) input.readObject();
            input.close();
            return tempObject;
        } catch (IOException | ClassNotFoundException e) {
            return null;
        }
    }
}
