import customtkinter as ctk
import appdirs
from datetime import datetime
from src.models.menu import Menu



class FavorieMenuWindow(ctk.CTkToplevel):
    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.list_menus_fav = main_controller.settings.favorites_menus
        self.main_controller = main_controller
        self.nutrition_controller = main_controller.controllers.get("Nutrition")

        # Appliquer le mode d'apparence du main_controller
        ctk.set_appearance_mode(self.main_controller.settings.appearance_mode)
        
        # Appliquer la couleur de fond cohérente avec le thème
        self.configure(fg_color=self.main_controller.theme_colors['bg'])

        # titre et dimensions de la fenêtre
        self.title("Menus favoris")
        self.geometry("700x500")

        # Centrer la fenêtre à l'écran
        self.center_window()

        # Configuration du grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Titre
        title_label = ctk.CTkLabel(
            self,
            text=f"Menus favoris",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 10))

        # Frame scrollable pour afficher les menus
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.main_controller.theme_colors['frame'],
            corner_radius=10,
        )
        self.scrollable_frame.grid(
            row=1, column=0, sticky="nsew", padx=20, pady=(0, 20)
        )
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Afficher les menus favoris
        self.display_favorite_menus()
        self.grab_set()  # Rendre la fenêtre modale

    def center_window(self):
        """Centre la fenêtre au milieu de l'écran"""
        # Dimensions de la fenêtre
        window_width = 700
        window_height = 500
        
        # Obtenir la résolution d'écran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculer la position x et y pour centrer
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Positionner la fenêtre avec les bonnes dimensions
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def display_favorite_menus(self):
        """Affiche la liste des menus favoris avec leur composition"""
        # Récupérer les menus favoris du profil actuel (actualiser depuis les settings)
        self.list_menus_fav = self.main_controller.settings.favorites_menus
        favorite_menus_data = list(
            self.list_menus_fav
        )  # Convertir en liste pour itérer facilement

        # Supprimer les widgets existants dans le scrollable_frame avant de les recréer
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Si pas de menus favoris
        if not favorite_menus_data:
            no_menu_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="Aucun menu favori pour le moment",
                font=ctk.CTkFont(size=13),
                text_color=self.main_controller.theme_colors['text_secondary'],
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
            fg_color=self.main_controller.theme_colors['frame_dark'],
            corner_radius=10,
        )
        menu_frame.pack(fill="x", padx=5, pady=10)
        menu_frame.grid_columnconfigure(0, weight=1)

        # Header avec date/heure et bouton
        header_frame = ctk.CTkFrame(menu_frame, fg_color=self.main_controller.theme_colors['frame_dark'])
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)

        # Bouton Supprimer
        delete_button = ctk.CTkButton(
            header_frame,
            text="🗑 Supprimer",
            width=100,
            height=28,
            corner_radius=6,
            fg_color=self.main_controller.theme_colors['error'],
            hover_color=self.main_controller.theme_colors['error_hover'],
            text_color=self.main_controller.theme_colors['text'],
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda m=menu: self.on_delete_menu(m),
        )
        delete_button.grid(row=0, column=0, sticky="w", padx=(0, 10))

        # Bouton Ajouter
        add_button = ctk.CTkButton(
            header_frame,
            text="+ Ajouter",
            width=100,
            height=28,
            corner_radius=6,
            fg_color=self.main_controller.settings.theme,
            hover_color=self.main_controller.darken_color(self.main_controller.settings.theme),
            text_color=self.main_controller.theme_colors['text'],
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda m=menu: self.on_add_menu(m),
        )
        add_button.grid(row=0, column=2, sticky="e", padx=(10, 0))

        # Liste des aliments
        foods_frame = ctk.CTkFrame(menu_frame, fg_color=self.main_controller.theme_colors['frame_dark'])
        foods_frame.pack(fill="x", padx=15, pady=(0, 5))

        # Afficher chaque aliment du menu
        for food_menu in menu.content:
            self.create_food_item(foods_frame, food_menu)

        # Totaux des macros
        self._create_macros_summary(menu_frame, menu)

    def create_food_item(self, parent_frame, food_menu):
        """Crée un item pour afficher un aliment avec ses macros"""
        item_frame = ctk.CTkFrame(parent_frame, fg_color=self.main_controller.theme_colors['frame'], corner_radius=6)
        item_frame.pack(fill="x", pady=3)
        item_frame.grid_columnconfigure(0, weight=1)

        # Nom et quantité de l'aliment
        food_name_label = ctk.CTkLabel(
            item_frame,
            text=f"• {food_menu.name} ({food_menu.quantity}g)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.main_controller.theme_colors['text'],
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
                text_color=self.main_controller.theme_colors['text_secondary'],
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
        summary_frame = ctk.CTkFrame(parent_frame, fg_color=self.main_controller.theme_colors['frame_darker'], corner_radius=6)
        summary_frame.pack(fill="x", padx=15, pady=(5, 10))

        summary_text = f"📊 Total: {int(total_calories)} kcal | Protéines: {int(total_proteins)}g | Glucides: {int(total_carbs)}g | Lipides: {int(total_fats)}g"
        summary_label = ctk.CTkLabel(
            summary_frame,
            text=summary_text,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.main_controller.settings.theme,
        )
        summary_label.pack(padx=10, pady=8)

    def on_add_menu(self, menu):
        """Callback pour le bouton Ajouter"""

        # Combiner la date sélectionnée (current_date) avec l'heure actuelle
        selected_date = self.nutrition_controller.current_date.strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        current_datetime = f"{selected_date} {current_time}"

        menu_to_add = Menu(current_datetime)
        for food in menu.content:
            menu_to_add.add_food_menu(food, food.quantity)
        self.main_controller.current_profile.eating_habits.append(menu_to_add)
        self.main_controller.settings.serialize(
            appdirs.user_data_dir("Nutritrack") + "/settings.json"
        )  # Sauvegarder après l'ajout
        self.nutrition_controller.display_menus()  # Rafraîchir la page Nutrition si ouverte

    def on_delete_menu(self, menu):
        """Callback pour le bouton Supprimer"""
        self.main_controller.settings.favorites_menus.discard(
            menu
        )  # Supprimer du set des favoris
        self.display_favorite_menus()  # Rafraîchir l'affichage
        self.nutrition_controller.display_menus()  # Rafraîchir la page Nutrition si ouverte
        self.main_controller.settings.serialize(
            appdirs.user_data_dir("Nutritrack") + "/settings.json"
        )
