package GUI;

public interface IMainMenu {
    void setPresenter(IPresenter IPresenter);

    IPresenter getPresenter();

    void displayErrorMessage();

    Object[] returnUserInput();

    void close();
}
