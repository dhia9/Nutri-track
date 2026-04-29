import src.views.main_window as main_window
import src.controllers.main_controller as main_controller

if __name__ == "__main__":
    controller = main_controller.MainController()
    app = main_window.MainPage(controller=controller)
    app.mainloop()
