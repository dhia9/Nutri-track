import customtkinter as ctk

class FavorieMenuWindow(ctk.CTkToplevel):
    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.list_menus_fav = main_controller.settings.favorites_menus
        self.main_controller = main_controller

        # titre et dimensions de la fenêtre
        self.title("Menus favoris")
        self.geometry("700x500")

        # Configuration du grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Titre
        title_label = ctk.CTkLabel(
            self,
            text=f"📋Menus favoris",
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
        self.display_favorite_menus()
        self.grab_set()  # Rendre la fenêtre modale

    def display_favorite_menus(self):
        """Affiche la liste des menus favoris avec leur composition"""
        # Récupérer les menus favoris du profil actuel
        favorite_menus_data = list(self.list_menus_fav)  # Convertir en liste pour itérer facilement

        # Si pas de menus favoris
        if not favorite_menus_data:
            no_menu_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="Aucun menu favori pour le moment",
                font=ctk.CTkFont(size=13),
                text_color="#A8AFB6",
            )
            no_menu_label.pack(padx=10, pady=20)
            return 

        # Afficher chaque menu favori
        for menu in favorite_menus_data:
            self.create_menu_frame(menu)

    def create_menu_frame(self, menu):
        """Crée un frame pour afficher un menu avec sa composition"""
        # Frame principal du menu
        menu_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#2A2A4A",
            corner_radius=10,
        )
        menu_frame.pack(fill="x", padx=5, pady=10)
        menu_frame.grid_columnconfigure(0, weight=1)

        # Header avec date/heure et bouton
        header_frame = ctk.CTkFrame(menu_frame, fg_color="#2A2A4A")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)

        # Bouton Supprimer
        delete_button = ctk.CTkButton(
            header_frame,
            text="🗑 Supprimer",
            width=100,
            height=28,
            corner_radius=6,
            fg_color="#D9534F",
            hover_color="#C9302C",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda m=menu: self._on_delete_menu(m),
        )
        delete_button.grid(row=0, column=0, sticky="w", padx=(0, 10))

        # Bouton Ajouter
        add_button = ctk.CTkButton(
            header_frame,
            text="+ Ajouter",
            width=100,
            height=28,
            corner_radius=6,
            fg_color="#4CAF50",
            hover_color="#45a049",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda m=menu: self._on_add_menu(m),
        )
        add_button.grid(row=0, column=2, sticky="e", padx=(10, 0))

        # Liste des aliments
        foods_frame = ctk.CTkFrame(menu_frame, fg_color="#2A2A4A")
        foods_frame.pack(fill="x", padx=15, pady=(0, 5))

        # Afficher chaque aliment du menu
        for food_menu in menu.content:
            self.create_food_item(foods_frame, food_menu)

        # Totaux des macros
        self._create_macros_summary(menu_frame, menu)

    def create_food_item(self, parent_frame, food_menu):
        """Crée un item pour afficher un aliment avec ses macros"""
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
            total_cal = sum(m.calorie * (food_menu.quantity / m.masse) for m in food_menu.macros)
            total_prot = sum(m.proteine * (food_menu.quantity / m.masse) for m in food_menu.macros)
            total_carb = sum(m.carbohydrate * (food_menu.quantity / m.masse) for m in food_menu.macros)
            total_fat = sum(m.fat * (food_menu.quantity / m.masse) for m in food_menu.macros)
            
            macros_text = f"Cal: {int(total_cal)} | Prot: {int(total_prot)}g | Glucides: {int(total_carb)}g | Lipides: {int(total_fat)}g"
            macros_label = ctk.CTkLabel(
                item_frame,
                text=macros_text,
                font=ctk.CTkFont(size=9),
                text_color="#A8AFB6",
            )
            macros_label.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 5))

    def _create_macros_summary(self, parent_frame, menu):
        """Affiche le résumé des macros totales du menu"""
        # Calculer les totaux
        total_calories = 0
        total_proteins = 0
        total_carbs = 0
        total_fats = 0

        for food_menu in menu.content:
            if food_menu.macros:
                # Additionner les macros (liste d'objets Macro) en tenant compte de la quantité
                total_calories += sum(m.calorie * (food_menu.quantity / m.masse) for m in food_menu.macros)
                total_proteins += sum(m.proteine * (food_menu.quantity / m.masse) for m in food_menu.macros)
                total_carbs += sum(m.carbohydrate * (food_menu.quantity / m.masse) for m in food_menu.macros)
                total_fats += sum(m.fat * (food_menu.quantity / m.masse) for m in food_menu.macros)

        # Frame de résumé
        summary_frame = ctk.CTkFrame(parent_frame, fg_color="#1A1A2E", corner_radius=6)
        summary_frame.pack(fill="x", padx=15, pady=(5, 10))

        summary_text = f"📊 Total: {int(total_calories)} kcal | Protéines: {int(total_proteins)}g | Glucides: {int(total_carbs)}g | Lipides: {int(total_fats)}g"
        summary_label = ctk.CTkLabel(
            summary_frame,
            text=summary_text,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#4CAF50",
        )
        summary_label.pack(padx=10, pady=8)

    def _on_add_menu(self, menu):
        """Callback pour le bouton Ajouter"""
        # Le backend sera implémenté par l'utilisateur
        print(f"Ajout du menu du {menu.date}")

    def _on_delete_menu(self, menu):
        """Callback pour le bouton Supprimer"""
        # Le backend sera implémenté par l'utilisateur
        print(f"Suppression du menu du {menu.date}")