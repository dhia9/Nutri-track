import os
import tkinter as tk

import customtkinter as ctk
from PIL import Image

import src.views.home_page as home_page
from src.views.nutrition_page import NutritionPage
from src.views.stats_page import StatsPage
from src.views.settings_page import SettingsPage


class MainPage(ctk.CTk):
    """Fenêtre principale avec navigation verticale et zone de contenu."""

    COLOR_BG = "#121212"
    COLOR_SIDEBAR = "#1D1F21"
    COLOR_CONTENT = "#17191B"
    COLOR_ACCENT = "#2DBA7F"
    COLOR_BUTTON = "#2A2D30"
    COLOR_BUTTON_HOVER = "#35393D"
    COLOR_TEXT = "#F1F1F1"
    COLOR_TEXT_SECONDARY = "#A8AFB6"

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        # Configurer la view du contrôleur AVANT d'utiliser ses méthodes
        self.controller.view = self

        self.title("Nutritrack")
        logo_path = os.path.normpath(
            os.path.join(os.getcwd(), "src", "assets", "images", "Logo_sans_txt.png")
        )
        self._sidebar_logo = None
        if os.path.exists(logo_path):
            self._icon_image = tk.PhotoImage(file=logo_path)
            self.iconphoto(True, self._icon_image)
            logo_image = Image.open(logo_path)
            orig_width, orig_height = logo_image.size
            base_size = 48
            scale_factor = 4
            target_width = base_size * scale_factor
            target_height = max(1, int(target_width * orig_height / orig_width))
            self._sidebar_logo = ctk.CTkImage(
                light_image=logo_image,
                dark_image=logo_image,
                size=(target_width, target_height),
            )
        self.geometry("1280x760")
        self.minsize(960, 560)

        # update les dimensions de la fenêtre avant de calculer la position
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (1280 // 2)
        y = (screen_height // 2) - (760 // 2)
        self.geometry(f"+{x}+{y}")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.configure(fg_color=self.COLOR_BG)

        # Grille principale: colonne gauche = navigation, colonne droite = contenu
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.nav_buttons = {}

        self.create_sidebar()
        self.create_page_container()
        self.home_page = home_page.HomePage(
            self.pages_container, main_controller=self.controller
        )
        self.nutrition_page = None
        self.stats_page = None

        pages = {"Accueil": self.home_page}
        if self.controller.current_profile is not None:
            self.nutrition_page = NutritionPage(
                self.pages_container, main_controller=self.controller
            )
            pages["Nutrition"] = self.nutrition_page
            self.stats_page = StatsPage(
                self.pages_container, main_controller=self.controller
            )
            pages["Statistiques"] = self.stats_page
            self.settings_page = SettingsPage(
                self.pages_container, main_controller=self.controller
            )
            pages["Paramètres"] = self.settings_page

        # Déléguer la gestion des pages au contrôleur
        self.controller.set_existing_pages(pages)
        self.controller.show_page("Accueil")
        self.controller.update_nav_buttons()

    def create_sidebar(self):
        """Crée la barre de navigation en colonne à gauche."""
        self.sidebar = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_SIDEBAR,
            width=260,
            corner_radius=0,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(4, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        if self._sidebar_logo is not None:
            ctk.CTkLabel(
                self.sidebar,
                text="",
                image=self._sidebar_logo,
            ).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 2))
        else:
            title_label = ctk.CTkLabel(
                self.sidebar,
                text="NUTRITRACK",
                font=ctk.CTkFont(size=26, weight="bold"),
                text_color=self.COLOR_TEXT,
            )
            title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(24, 2))

        nav_label = ctk.CTkLabel(
            self.sidebar,
            text="NAVIGATION",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.COLOR_TEXT_SECONDARY,
        )
        nav_label.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))

        self.nav_container = ctk.CTkFrame(self.sidebar, fg_color=self.COLOR_SIDEBAR)
        self.nav_container.grid(row=2, column=0, sticky="ew", padx=14)
        self.nav_container.grid_columnconfigure(0, weight=1)

        pages_config = ["Accueil", "Nutrition", "Statistiques", "Paramètres"]
        for index, page_name in enumerate(pages_config):
            btn = self.create_nav_button(self.nav_container, page_name)
            btn.grid(row=index, column=0, sticky="ew", padx=6, pady=6)
            self.nav_buttons[page_name] = btn

        footer_label = ctk.CTkLabel(
            self.sidebar,
            text="Nutritrack v0.1",
            font=ctk.CTkFont(size=11),
            text_color=self.COLOR_TEXT_SECONDARY,
        )
        footer_label.grid(row=5, column=0, sticky="sw", padx=20, pady=(0, 20))

    def create_nav_button(self, parent, page_name):
        """Crée un bouton de navigation stylisé."""
        btn = ctk.CTkButton(
            parent,
            text=page_name,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.COLOR_BUTTON,
            text_color=self.COLOR_TEXT,
            hover_color=self.COLOR_BUTTON_HOVER,
            border_width=2,
            border_color=self.COLOR_BUTTON,
            corner_radius=10,
            height=42,
            command=lambda: self.controller.show_page(page_name),
            anchor="w",
        )
        return btn

    def create_page_container(self):
        """Crée la zone de droite qui affichera les autres pages."""
        self.pages_container = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_CONTENT,
            corner_radius=0,
        )
        self.pages_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.pages_container.grid_columnconfigure(0, weight=1)
        self.pages_container.grid_rowconfigure(0, weight=1)

    def build_profile_pages(self):
        if self.nutrition_page is None:
            self.nutrition_page = NutritionPage(
                self.pages_container, main_controller=self.controller
            )
        if self.stats_page is None:
            self.stats_page = StatsPage(
                self.pages_container, main_controller=self.controller
            )
        return {
            "Accueil": self.home_page,
            "Nutrition": self.nutrition_page,
            "Statistiques": self.stats_page,
        }

    def reload_profile_pages(self):
        if self.nutrition_page is not None and self.nutrition_page.winfo_exists():
            self.nutrition_page.destroy()
        if self.stats_page is not None and self.stats_page.winfo_exists():
            self.stats_page.destroy()

        self.nutrition_page = None
        self.stats_page = None

        pages = {"Accueil": self.home_page}
        if self.controller.current_profile is not None:
            self.nutrition_page = NutritionPage(
                self.pages_container, main_controller=self.controller
            )
            self.stats_page = StatsPage(
                self.pages_container, main_controller=self.controller
            )
            pages["Nutrition"] = self.nutrition_page
            pages["Statistiques"] = self.stats_page

        self.controller.set_existing_pages(pages)
        target_page = self.controller.current_page
        if target_page not in pages:
            target_page = "Accueil"
        self.controller.show_page(target_page)
        self.controller.update_nav_buttons()

    def set_existing_pages(self, pages):
        self.controller.set_existing_pages(pages)

    def show_page(
        self, page_name
    ):  # Permet de changer de page et d'afficher la page d'accueil par défaut
        self.controller.show_page(page_name)
