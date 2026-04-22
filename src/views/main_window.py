import customtkinter as ctk
from home_page import HomeView


class BaseView(ctk.CTk):
    """Fenêtre principale avec navigation verticale et zone de contenu."""

    COLOR_BG = "#121212"
    COLOR_SIDEBAR = "#1D1F21"
    COLOR_CONTENT = "#17191B"
    COLOR_ACCENT = "#2DBA7F"
    COLOR_BUTTON = "#2A2D30"
    COLOR_BUTTON_HOVER = "#35393D"
    COLOR_TEXT = "#F1F1F1"
    COLOR_TEXT_SECONDARY = "#A8AFB6"

    def __init__(self):
        super().__init__()
        self.title("Nutritrack")
        self.geometry("1280x760")
        self.minsize(960, 560)

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
        self.current_page = None
        self.set_existing_pages(
            {
                "Accueil": HomeView(self.pages_container),
            }
        )
        self.show_page("Accueil")

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
            border_width=1.5,
            border_color=self.COLOR_BUTTON,
            corner_radius=10,
            height=42,
            command=lambda: self.show_page(page_name),
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

        # Vue placeholder tant qu'aucune page n'est injectée par le contrôleur
        self.placeholder = ctk.CTkFrame(
            self.pages_container, fg_color=self.COLOR_CONTENT
        )
        self.placeholder.grid(row=0, column=0, sticky="nsew")
        self.placeholder.grid_columnconfigure(0, weight=1)
        self.placeholder.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(
            self.placeholder,
            text="Zone de contenu",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.COLOR_TEXT,
        ).grid(row=0, column=0, pady=(0, 12))

        ctk.CTkLabel(
            self.placeholder,
            text="Les autres pages s'afficheront ici.",
            font=ctk.CTkFont(size=14),
            text_color=self.COLOR_TEXT_SECONDARY,
        ).grid(row=1, column=0)

    def set_existing_pages(self, pages):
        """Enregistre des pages deja creees pour la navigation.

        Args:
            pages: dictionnaire {"NomPage": widget_page}
        """
        self.pages = {}

        if hasattr(self, "placeholder") and self.placeholder.winfo_exists():
            self.placeholder.grid_remove()

        for name, page_widget in pages.items():
            page_widget.grid(row=0, column=0, sticky="nsew")
            page_widget.grid_remove()
            self.pages[name] = page_widget

    def show_page(self, page_name):
        """Affiche une page spécifique."""
        if page_name not in self.pages:
            return

        if self.current_page and self.current_page in self.pages:
            self.pages[self.current_page].grid_remove()

        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.configure(
                    fg_color=self.COLOR_ACCENT,
                    text_color="#0D281C",
                    border_color=self.COLOR_ACCENT,
                )
            else:
                btn.configure(
                    fg_color=self.COLOR_BUTTON,
                    text_color=self.COLOR_TEXT,
                    border_color=self.COLOR_BUTTON,
                )

        self.pages[page_name].grid()
        self.current_page = page_name


if __name__ == "__main__":
    app = BaseView()
    app.mainloop()
