import src.views.main_window as main_window
import src.controllers.main_controller as main_controller
import os
import appdirs
if __name__ == "__main__":
    """
    utile pour retrouver chemin settings.json
    settings_path = os.path.join(
        appdirs.user_data_dir("Nutritrack"), "settings.json")
    print("Chemin :", settings_path)
    print("Existe :", os.path.isfile(settings_path))"""
    controller = main_controller.MainController()
    app = main_window.MainPage(controller=controller)
    app.mainloop()
    
