import customtkinter as ctk


class FoodQuantity(ctk.CTkToplevel):
    def __init__(self, food_list, parent=None, main_controller=None):
        """Initialise la fenêtre de saisie des quantités d'aliments.

        Args:
            food_list: Liste des noms d'aliments pour lesquels saisir les quantités.
            parent: Widget parent (optionnel).
        """
        super().__init__(parent)
        self.food_list = food_list
        self.quantities = {}  # Dictionnaire pour stocker les valeurs des entries
        self.main_controller = main_controller

        # Obtenir les couleurs du thème
        theme_colors = main_controller.theme_colors if main_controller else {}

        # Configuration de la fenêtre
        self.title("Quantités des aliments")
        self.geometry("600x700")
        self.resizable(True, True)

        # Mettre la fenêtre au premier plan sur Windows
        self.attributes("-topmost", True)
        self.lift()
        self.focus()

        # Rendre la fenêtre modale
        self.grab_set()

        # Centrer la fenêtre sur l'écran
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - 300
        y = (screen_height // 2) - 350
        self.geometry(f"600x700+{x}+{y}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Titre
        self.food_label = ctk.CTkLabel(
            self, text="Quelles Quantités ?", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.food_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))

        # Frame scrollable pour la liste des aliments
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="#35393D", corner_radius=10
        )
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))

        # Pour chaque aliment, créer label + entry + "grammes"
        for food in food_list:
            # Frame pour chaque aliment
            food_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            food_frame.pack(fill="x", padx=5, pady=8)

            # Label de l'aliment
            food_name_label = ctk.CTkLabel(
                food_frame, text=food, font=ctk.CTkFont(size=12), text_color="#FFFFFF"
            )
            food_name_label.pack(side="left", padx=(0, 10), fill="x", expand=True)

            # Entry pour la quantité (nombres seulement)
            quantity_entry = ctk.CTkEntry(
                food_frame,
                placeholder_text="0",
                fg_color="#2A2A4A",
                border_color="#4CAF50",
                border_width=1,
                text_color="#FFFFFF",
                width=60,
            )
            quantity_entry.pack(side="left", padx=5)

            # Label "grammes"
            grammes_label = ctk.CTkLabel(
                food_frame, text="g", font=ctk.CTkFont(size=12), text_color="#A8AFB6"
            )
            grammes_label.pack(side="left", padx=(0, 5))

            # Stocker la référence à l'entry
            self.quantities[food] = quantity_entry

        # Frame pour les boutons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=15)
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # Bouton Valider
        self.submit_btn = ctk.CTkButton(
            button_frame,
            text="✓ Valider",
            command=self.on_submit,
            fg_color="#2DBA7F",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.submit_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # Bouton Annuler
        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="✗ Annuler",
            command=self.on_cancel,
            fg_color="#35393D",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.cancel_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def get_quantities(self):
        """Retourne un dictionnaire avec les quantités saisies"""
        result = {}
        for food, entry in self.quantities.items():
            try:
                quantity = float(entry.get()) if entry.get() else 0
                result[food] = quantity
            except ValueError:
                result[food] = 0
        return result

    def on_submit(self):
        """Valider et fermer la fenêtre"""
        self.quantities = (
            self.get_quantities()
        )  # Mettre à jour les quantités avec les valeurs saisies
        self.destroy()

    def on_cancel(self):
        """Annuler et fermer la fenêtre"""
        self.quantities = {}  # Réinitialiser les quantités
        self.destroy()
