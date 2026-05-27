import os

import appdirs
import src.controllers.home_controller as home_controller
import src.controllers.nutrition_controller as nutrition_controller
import src.controllers.settings_controller as settings_controller
import src.models.settings as settings
import src.data.food_data as food_data
from src.controllers.stats_controller import StatsController


class MainController:
    def __init__(self):
        # La vue principale (MainPage) sera assignée après sa création pour éviter les problèmes de dépendances circulaires
        self.view = None
        self.pages = {}
        self.current_page = None
        
        # Initialiser settings en premier pour récupérer les couleurs
        self.settings = settings.Settings()
        self.settings.deserialize(
            os.path.join(appdirs.user_data_dir("Nutritrack"), "settings.json")
        )  # Charger les données depuis le fichier JSON
        
        # Initialiser les couleurs du thème (light ou dark)
        self.theme_colors = {}
        self.update_theme_colors()  # Appliquer les couleurs selon le mode d'apparence
        
        self.current_profile = (
            self.settings.profiles[0] if len(self.settings.profiles) > 0 else None
        )
        
        # Initialiser food_data une seule fois au démarrage
        self.food_data = food_data.FoodData()
        self.food_data.deserialize("src/data/data.json")
        
        self.controllers = {
            "Home": home_controller.HomeController(self),
            "Nutrition": nutrition_controller.NutritionController(self),
            "Stats": StatsController(self),
            "Settings": settings_controller.SettingsController(self),
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
            # Enregistrer la page dans le dictionnaire
            self.pages[name] = page_widget

    def set_current_profile(self, profile):
        self.current_profile = profile
        nutrition = self.controllers.get("Nutrition")
        if nutrition and hasattr(nutrition, "set_current_profile"):
            nutrition.set_current_profile(profile)
        if self.view is not None and hasattr(self.view, "reload_profile_pages"):
            self.view.reload_profile_pages()
        else:
            self.enable_profile_pages()

    def update_nav_buttons(self):
        if self.view is None:
            return
        profile_selected = self.current_profile is not None
        for name, btn in self.view.nav_buttons.items():
            if name == "Accueil" or name == "Paramètres":
                continue
            enabled = profile_selected and name in self.pages
            btn.configure(
                state="normal" if enabled else "disabled",
                text_color=(
                    self.theme_colors['text'] if enabled else self.theme_colors['text_secondary']
                ),
            )

    def enable_profile_pages(self):
        if self.view is None:
            return
        if "Nutrition" not in self.pages and hasattr(self.view, "build_profile_pages"):
            pages = self.view.build_profile_pages()
            self.set_existing_pages(pages)

        current = self.current_page or "Accueil"
        self._show_page(current)
        self.update_nav_buttons()

    def _show_page(self, page_name):
        """Affiche une page spécifique et met à jour les boutons de navigation."""
        if self.current_profile is None and page_name not in ["Accueil", "Paramètres"]:
            return
        if page_name not in self.pages:
            return

        if page_name == "Statistiques":
            stats_page = self.pages[page_name]
            if hasattr(stats_page, "refresh"):
                stats_page.refresh()

        # Masquer la page actuellement affichée
        if self.current_page and self.current_page in self.pages:
            self.pages[self.current_page].grid_remove()

        # Mettre à jour les styles des boutons de navigation
        for name, btn in self.view.nav_buttons.items():
            if name == page_name:
                btn.configure(
                    fg_color=self.settings.theme,
                    text_color="#0D281C",
                    border_color=self.settings.theme,
                )
            else:
                btn.configure(
                    fg_color=self.theme_colors['button'],
                    text_color=self.theme_colors['text'],
                    border_color=self.theme_colors['button'],
                )

        # Afficher la nouvelle page
        self.pages[page_name].grid()
        self.current_page = page_name

    show_page = _show_page

    def refresh_current_page(self):
        """Recharge la page courante avec les couleurs du thème mis à jour."""
        if self.current_page:
            # Masquer et réafficher la page pour forcer une rafraîchissement
            self.pages[self.current_page].grid_remove()
            self.pages[self.current_page].grid()
            # Mettre à jour les boutons de navigation avec les nouvelles couleurs
            for name, btn in self.view.nav_buttons.items():
                if name == self.current_page:
                    btn.configure(
                        fg_color=self.settings.theme,
                        text_color="#0D281C",
                        border_color=self.settings.theme,
                    )
                else:
                    btn.configure(
                        fg_color=self.theme_colors['button'],
                        text_color=self.theme_colors['text'],
                        border_color=self.theme_colors['button'],
                    )

    def recreate_ui_for_theme_change(self):
        """Recréé toute l'UI (pages et sidebar) quand le thème change."""
        # Mettre à jour les couleurs selon le mode d'apparence
        self.update_theme_colors()
        
        if self.view is not None and hasattr(self.view, 'recreate_all_pages_and_ui'):
            self.view.recreate_all_pages_and_ui()

    def update_theme_colors(self):
        """Met à jour les couleurs des frames selon le mode d'apparence (light/dark)."""
        appearance_mode = self.settings.appearance_mode
        
        if appearance_mode == "light":
            self.theme_colors = {
                'bg': '#F5F5F5',  # Blanc léger
                'sidebar': '#EEEEEE',  # Gris très clair
                'content': '#FFFFFF',  # Blanc
                'button': '#E8E8E8',  # Gris clair
                'button_hover': '#D0D0D0',  # Gris moyen
                'text': '#1F1F1F',  # Noir (texte)
                'text_secondary': '#757575',  # Gris foncé (texte secondaire)
                'frame': '#E8E8E8',  # Gris clair pour les frames
                'frame_dark': '#D0D0D0',  # Gris moyen pour les frames sombres
                'frame_darker': '#B8B8B8',  # Gris foncé pour les frames plus sombres
                'error': '#F44336',  # Rouge (erreur)
                'error_hover': '#E53935',  # Rouge foncé (hover)
            }
        else:  # dark mode
            self.theme_colors = {
                'bg': '#121212',
                'sidebar': '#1D1F21',
                'content': '#17191B',
                'button': '#2A2D30',
                'button_hover': '#35393D',
                'text': '#F1F1F1',
                'text_secondary': '#A8AFB6',
                'frame': '#35393D',  # Gris sombre pour les frames
                'frame_dark': '#2A2A4A',
                'frame_darker': '#1A1A2E',
                'error': '#D9534F',
                'error_hover': '#C9302C',
            }

    def darken_color(self, hex_color: str, factor: float = 0.7) -> str:
        """Assombrit une couleur hex en réduisant la valeur HSV."""
        from colorsys import rgb_to_hsv, hsv_to_rgb
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))
        h, s, v = rgb_to_hsv(r, g, b)
        r2, g2, b2 = hsv_to_rgb(h, s, v * factor)
        return f"#{int(r2*255):02x}{int(g2*255):02x}{int(b2*255):02x}"
