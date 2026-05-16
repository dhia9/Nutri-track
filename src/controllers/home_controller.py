import src.views.home_page as home_page
import src.views.message_box as message_box
from src.models.profile import Profile


class HomeController:
    def __init__(self, main_controller):
        self.view: home_page.HomePage = None
        self.main_controller = main_controller

    def existing_name_profile(self, name):
        for profile in self.main_controller.settings.profiles:
            if profile.name == name:
                return True
        return False

    def validate_int(self, char):
        """Accepte uniquement les chiffres entiers"""
        if char == "":
            return True
        return char.isdigit()

    def validate_float(self, char):
        """Accepte uniquement les chiffres et virgule/point à la saisie"""
        if char == "":
            return True
        return char.isdigit() or char == "."

    def create_profile(self):
        # Récupérer les données du formulaire
        nom = self.view.nom_entry.get()
        age = self.view.age_entry.get()
        taille = self.view.taille_entry.get()
        poids = self.view.poids_entry.get()
        sex = self.view.sexe_var.get()
        objectif = self.view.objectif_var.get()

        # Valider les données (ex: vérifier que l'âge est un nombre)
        if (
            not nom
            or not age.isdigit()
            or not taille.isdigit()
            or not poids.isdigit()
            or sex not in ["Homme", "Femme"]  # Pas nécessaire mais on sait jamais
            or not objectif.isdigit()
        ):
            message_box.CTkMessageBox(
                self.main_controller.view,  # On attache la message box à la fenêtre principale pour qu'elle soit modale
                title="Erreur",
                message="Veuillez remplir tous les champs correctement.",
            )
            return
        if self.existing_name_profile(nom):
            message_box.CTkMessageBox(
                self.main_controller.view,
                title="Erreur",
                message="Un profil avec ce nom existe déjà. Veuillez choisir un autre nom.",
            )
            return

        # Créer un nouvel objet Profile
        self.main_controller.settings.create_profile(
            name=nom,
            age=int(age),
            weight=float(poids),
            height=float(taille),
            sex=sex,
            target_weight=float(objectif),
        )
        # Vider les champs du formulaire
        self.view.nom_entry.delete(0, "end")
        self.view.age_entry.delete(0, "end")
        self.view.taille_entry.delete(0, "end")
        self.view.poids_entry.delete(0, "end")
        self.view.objectif_Entry.delete(0, "end")
        self.view.sexe_var.set("Homme")
        # Afficher un message de succès
        message_box.CTkMessageBox(
            self.main_controller.view,
            title="Succès",
            message="Profil créé avec succès !",
        )

    def select_profile(self, profile: Profile):
        self.main_controller.set_current_profile(profile)
        if self.view is not None:
            self.view.set_selected_profile(profile)
