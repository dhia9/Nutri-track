import os

import appdirs
import src.controllers.home_controller as home_controller
import src.controllers.nutrition_controller as nutrition_controller
import src.models.settings as settings


class MainController:
    def __init__(self):
        self.view = None  # La vue principale (MainPage) sera assignée après sa création pour éviter les problèmes de dépendances circulaires
        self.pages = {}
        self.current_page = None
        self.settings = settings.Settings()
        self.settings.deserialize(
            os.path.join(appdirs.user_data_dir("Nutritrack"), "settings.json")
        )  # Charger les données depuis le fichier JSON
        self.current_profile = self.settings.profiles[0] if len(self.settings.profiles) > 0 else None
        
        self.controllers = {
            "Home": home_controller.HomeController(self),
            "Nutrition": nutrition_controller.NutritionController(self),  # Placeholder pour le contrôleur de la page Nutrition
        }  # Dico pour stocker les sous contrôlleur de chaque page

    def set_existing_pages(self, pages):
        """Enregistre des pages deja creees pour la navigation.

        Args:
            pages: dictionnaire {"NomPage": widget_page}
        """
        # Réinitialiser le dictionnaire des pages
        self.pages = {}

        # Vérifier si le placeholder existe et l'enlever
        if hasattr(self.view, "placeholder") and self.view.placeholder.winfo_exists():
            self.view.placeholder.grid_remove()

        for name, page_widget in pages.items():
            page_widget.grid(row=0, column=0, sticky="nsew")  # On affiche
            page_widget.grid_remove()  # On cache dirrectement => pour la fluidité de la navigation
            self.pages[name] = page_widget  # Enregistrer la page dans le dictionnaire

    def show_page(self, page_name):
        """Affiche une page spécifique et met à jour les boutons de navigation."""
        if page_name not in self.pages:
            return

        # Masquer la page actuellement affichée
        if self.current_page and self.current_page in self.pages:
            self.pages[self.current_page].grid_remove()

        # Mettre à jour les styles des boutons de navigation
        for name, btn in self.view.nav_buttons.items():
            if name == page_name:
                btn.configure(
                    fg_color=self.view.COLOR_ACCENT,
                    text_color="#0D281C",
                    border_color=self.view.COLOR_ACCENT,
                )
            else:
                btn.configure(
                    fg_color=self.view.COLOR_BUTTON,
                    text_color=self.view.COLOR_TEXT,
                    border_color=self.view.COLOR_BUTTON,
                )

        # Afficher la nouvelle page
        self.pages[page_name].grid()
        self.current_page = page_name
