package GUI;

public interface IViewUser {
    void setPresenter(IPresenter IPresenter);

    IPresenter getPresenter();

    void close();

    void displayErrorMessage();

    void successMessage();
}
