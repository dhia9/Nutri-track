import customtkinter as ctk
import src.controllers.main_controller as main_controller
import src.views.home_page as home_page


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
        self.geometry("1280x760")
        self.minsize(960, 560)

        self.update_idletasks()  # update les dimensions de la fenêtre avant de calculer la position
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

        self._create_sidebar()
        self._create_page_container()
        # Déléguer la gestion des pages au contrôleur
        self.controller.set_existing_pages(
            {
                "Accueil": home_page.HomePage(
                    self.pages_container, main_controller=self.controller
                ),
            }
        )
        self.controller.show_page("Accueil")

    def _create_sidebar(self):
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

        title_label = ctk.CTkLabel(
            self.sidebar,
            text="NUTRITRACK",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=self.COLOR_TEXT,
        )
        title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(24, 2))

        subtitle_label = ctk.CTkLabel(
            self.sidebar,
            text="Suivi nutritionnel",
            font=ctk.CTkFont(size=12),
            text_color=self.COLOR_TEXT_SECONDARY,
        )
        subtitle_label.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 24))

        nav_label = ctk.CTkLabel(
            self.sidebar,
            text="NAVIGATION",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.COLOR_TEXT_SECONDARY,
        )
        nav_label.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 10))

        self.nav_container = ctk.CTkFrame(self.sidebar, fg_color=self.COLOR_SIDEBAR)
        self.nav_container.grid(row=3, column=0, sticky="ew", padx=14)
        self.nav_container.grid_columnconfigure(0, weight=1)

        pages_config = ["Accueil", "Nutrition", "Statistiques"]
        for index, page_name in enumerate(pages_config):
            btn = self._create_nav_button(self.nav_container, page_name)
            btn.grid(row=index, column=0, sticky="ew", padx=6, pady=6)
            self.nav_buttons[page_name] = btn

        footer_label = ctk.CTkLabel(
            self.sidebar,
            text="Nutritrack v0.1",
            font=ctk.CTkFont(size=11),
            text_color=self.COLOR_TEXT_SECONDARY,
        )
        footer_label.grid(row=5, column=0, sticky="sw", padx=20, pady=(0, 20))

    def _create_nav_button(self, parent, page_name):
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

    def _create_page_container(self):
        """Crée la zone de droite qui affichera les autres pages."""
        self.pages_container = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_CONTENT,
            corner_radius=0,
        )
        self.pages_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.pages_container.grid_columnconfigure(0, weight=1)
        self.pages_container.grid_rowconfigure(0, weight=1)

    def set_existing_pages(self, pages):
        self.controller.set_existing_pages(pages)

    def show_page(
        self, page_name
    ):  # Permet de changer de page et d'afficher la page d'accueil par défaut
        self.controller.show_page(page_name)
