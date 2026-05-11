import src.views.settings_page as settings_page
import src.views.message_box as message_box
from src.models.profile import Profile

class SettingsController: 
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view: settings_page.SettingsPage = None
        

    def edit_profile(self, name, age, height, weight, target_weight, sex):
        profile = self.main_controller.current_profile
        if not profile:
            message_box.CTkMessageBox(
                self.main_controller.view,
                title="Erreur",
                message="Aucun profil sélectionné.",
            )
            return
        else :
            profile.name = name
            profile.age = age
            profile.height = height
            profile.weight = weight
            profile.target_weight = target_weight
            profile.sex = sex
        
        home_view = self.main_controller.controllers["Home"].view
        if home_view is not None:
            home_view._render_profiles()

    def delete_profile(self):
        home_view = self.main_controller.controllers["Home"].view
        if home_view is not None:  
            home_view._render_profiles()
        pass