import customtkinter as ctk


class SuggestedMenuWindow(ctk.CTkToplevel):
    def __init__(self, parent, main_controller):
        """Initialise la fenêtre des menus suggérés.

        Args:
            parent: Widget parent (fenêtre principale).
            main_controller: Le contrôleur principal de l'application.
        """
        super().__init__(parent)
        self.list_menus_fav = main_controller.settings.favorites_menus
        self.main_controller = main_controller
        self.nutrition_controller = main_controller.controllers.get("Nutrition")
        self.controller = self.main_controller.controllers["Nutrition"]
        # titre et dimensions de la fenêtre
        self.title("Menus suggérés")

        width = 700
        height = 500
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Configuration du grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Titre
        title_label = ctk.CTkLabel(
            self,
            text=f"Menus Proposés",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 10))

        # Frame scrollable pour afficher les menus
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#35393D",
            corner_radius=10,
        )
        self.scrollable_frame.grid(
            row=1, column=0, sticky="nsew", padx=20, pady=(0, 20)
        )
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Afficher les menus favoris
        self.display_suggested_menus()
        self.grab_set()  # Rendre la fenêtre modale

    def display_suggested_menus(self):
        """Affiche la liste des menus suggérés avec leur composition."""
        # Récupérer les menus  proposés (profil actuel)
        suggest_menus_data = self.controller.suggested_menus

        # Supprimer les widgets existants dans le scrollable_frame avant de les recréer
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Si pas de menus
        if not suggest_menus_data:
            no_menu_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="Aucun menu à proposer pour le moment",
                font=ctk.CTkFont(size=13),
                text_color="#A8AFB6",
            )
            no_menu_label.pack(padx=10, pady=20)
            return
        else:
            self.create_menu_frame(suggest_menus_data)

    def create_menu_frame(self, menu):
        """Crée un frame pour afficher un menu avec sa composition.

        Args:
            menu: Le menu à afficher.
        """
        # Frame principal du menu
        menu_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#2A2A4A",
            corner_radius=10,
        )
        menu_frame.pack(fill="x", padx=5, pady=5)
        menu_frame.grid_columnconfigure(0, weight=1)

        # Liste des aliments
        foods_frame = ctk.CTkFrame(menu_frame, fg_color="#2A2A4A")
        foods_frame.pack(fill="x", padx=5, pady=5)

        # Afficher chaque aliment du menu
        for food_menu in menu.content:
            self.create_food_item(foods_frame, food_menu)

        # Totaux des macros
        self._create_macros_summary(menu_frame, menu)
        add_button = ctk.CTkButton(
            menu_frame,
            text="Ajouter Menu",
            fg_color="#4CAF50",
            hover_color="#45A049",
            command=lambda m=menu: self.controller.add_suggested_menu(m, self),
        )

        add_button.pack(pady=10)

    def create_food_item(self, parent_frame, food_menu):
        """Crée un item pour afficher un aliment avec ses macros.

        Args:
            parent_frame: Le frame parent où ajouter l'item.
            food_menu: L'aliment à afficher.
        """
        item_frame = ctk.CTkFrame(parent_frame, fg_color="#35393D", corner_radius=6)
        item_frame.pack(fill="x", pady=3)
        item_frame.grid_columnconfigure(0, weight=1)

        # Nom et quantité de l'aliment
        food_name_label = ctk.CTkLabel(
            item_frame,
            text=f"• {food_menu.name} ({food_menu.quantity}g)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#FFFFFF",
        )
        food_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 2))

        # Macros de l'aliment
        if food_menu.macros:
            # Additionner les macros (liste d'objets Macro) en tenant compte de la quantité
            total_cal = sum(
                m.calorie * (food_menu.quantity / m.masse) for m in food_menu.macros
            )
            total_prot = sum(
                m.proteine * (food_menu.quantity / m.masse) for m in food_menu.macros
            )
            total_carb = sum(
                m.carbohydrate * (food_menu.quantity / m.masse)
                for m in food_menu.macros
            )
            total_fat = sum(
                m.fat * (food_menu.quantity / m.masse) for m in food_menu.macros
            )

            macros_text = f"Cal: {int(total_cal)} | Prot: {int(total_prot)}g | Glucides: {int(total_carb)}g | Lipides: {int(total_fat)}g"
            macros_label = ctk.CTkLabel(
                item_frame,
                text=macros_text,
                font=ctk.CTkFont(size=9),
                text_color="#A8AFB6",
            )
            macros_label.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 5))

    def _create_macros_summary(self, parent_frame, menu):
        """Affiche le résumé des macros totales du menu.

        Args:
            parent_frame: Le frame parent où ajouter le résumé.
            menu: Le menu dont afficher le résumé.
        """
        # Calculer les totaux
        total_calories = 0
        total_proteins = 0
        total_carbs = 0
        total_fats = 0

        for food_menu in menu.content:
            if food_menu.macros:
                # Additionner les macros (liste d'objets Macro) en tenant compte de la quantité
                total_calories += sum(
                    m.calorie * (food_menu.quantity / m.masse) for m in food_menu.macros
                )
                total_proteins += sum(
                    m.proteine * (food_menu.quantity / m.masse)
                    for m in food_menu.macros
                )
                total_carbs += sum(
                    m.carbohydrate * (food_menu.quantity / m.masse)
                    for m in food_menu.macros
                )
                total_fats += sum(
                    m.fat * (food_menu.quantity / m.masse) for m in food_menu.macros
                )

        # Frame de résumé
        summary_frame = ctk.CTkFrame(parent_frame, fg_color="#1A1A2E", corner_radius=6)
        summary_frame.pack(fill="x", padx=15, pady=(5, 10))

        summary_text = f"Total: {int(total_calories)} kcal | Protéines: {int(total_proteins)}g | Glucides: {int(total_carbs)}g | Lipides: {int(total_fats)}g"
        summary_label = ctk.CTkLabel(
            summary_frame,
            text=summary_text,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#4CAF50",
        )
        summary_label.pack(padx=10, pady=8)
