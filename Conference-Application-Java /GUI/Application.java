package GUI;


public class Application {
    /**
     * My Idea of structure come from this example:
     * https://stackoverflow.com/questions/11367250/concrete-code-example-of-mvp
     * main class for running the program
     */
    public static void main(String[] args) {

        java.awt.EventQueue.invokeLater(() -> {
            IModel IModel = new Model();
            IPresenter IPresenter = new Presenter();
            IPresenter.setModel(IModel);
            IMainMenu viewLogin = new ViewLogin();
            IPresenter.setMenu(viewLogin);
            IPresenter.run();
        });
    }
}
