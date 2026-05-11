import src.views.settings_page as settings_page
import src.views.message_box as message_box
from src.models.profile import Profile

class SettingsController: 
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view: settings_page.SettingsPage = None

    def edit_profile(self, name, age, height):
        pass