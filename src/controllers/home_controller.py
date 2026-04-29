import src.controllers.main_controller as main_controller
import src.views.home_page as home_page


class HomeController:
    def __init__(self, main_controller: main_controller.MainController = None):
        self.view: home_page.HomePage = None
        self.main_controller = main_controller

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
            or not sex in ["Homme", "Femme"] # Pas nécessaire mais on sait jamais
            or not objectif.isdigit()
        ):
            print("Données invalides")
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
