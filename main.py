import src.controllers.main_controller as main_controller
import src.views.main_window as main_window

if __name__ == "__main__":
    controller = main_controller.MainController()
    app = main_window.MainPage(controller=controller)
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print(f"Fermeture de l'application")
