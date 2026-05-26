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
        if not name or not str(age).isdigit() or sex not in ["Homme", "Femme"]:
            message_box.CTkMessageBox(
                self.main_controller.view,
                self.main_controller,
                title="Erreur",
                message="Veuillez remplir tous les champs correctement.",
            )
            return

        try:
            height = float(height)
            weight = float(weight)
            target_weight = float(target_weight)
        except (TypeError, ValueError):
            message_box.CTkMessageBox(
                self.main_controller.view,
                self.main_controller,
                title="Erreur",
                message="Veuillez remplir tous les champs correctement.",
            )
            return

        self.main_controller.settings.update_profile(
            profile=profile,
            name=name,
            age=int(age),
            height=height,
            weight=weight,
            target_weight=target_weight,
            sex=sex,
        )

        home_view = self.main_controller.controllers["Home"].view
        if home_view is not None:
            home_view.render_profiles()

        settings_view = self.main_controller.controllers["Settings"].view
        if settings_view is not None:
            settings_view.update_profile_details(profile)

        message_box.CTkMessageBox(
            self.main_controller.view,
            self.main_controller,
            title="Succès",
            message="Le profil a été modifié avec succès !",
        )

    def delete_profile(self):
        profile = self.main_controller.current_profile
        if not profile:
            message_box.CTkMessageBox(
                self.main_controller.view,
                self.main_controller,
                title="Erreur",
                message="Aucun profil sélectionné.",
            )
            return
        else:
            self.main_controller.settings.delete_profile(profile.name)
            self.main_controller.current_profile = None

        home_view = self.main_controller.controllers["Home"].view
        if home_view is not None:
            home_view.render_profiles()

        settings_view = self.main_controller.controllers["Settings"].view
        if settings_view is not None:
            settings_view.update_profile_details(None)
