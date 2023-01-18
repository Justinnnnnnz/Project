package information_saving;

/**
 * @author William Gao
 * An interface that is implemented by the Gateway class
 * The whole point of this interface is to invert a dependency
 * by creating an instance of Gateway with the type of IGateway.
 * So that I can read in files in a use case class without breaking
 * the dependency rule.
 */
public interface IGateway {
    void save(CollectorController collectorController);

    CollectorController read(String filepath);
}
