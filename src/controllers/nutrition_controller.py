from datetime import datetime, timedelta

import appdirs
import customtkinter as ctk
import src.controllers.main_controller as main_controller
import src.data.food_data as food_data
import src.models.menu as menu
import src.views.food_quantity as food_quantity
import src.views.message_box as message_box


class NutritionController:
    def __init__(self, main_controller: main_controller):
        self.main_controller = main_controller
        self.view = None  # La view sera assignée par la view elle-même
        self.current_profile = self.main_controller.current_profile
        self.current_date = datetime.now()
        self.food_data = (
            food_data.FoodData()
        )  # Initialiser la base de données en mémoire
        self.food_data.deserialize(
            "src/data/data.json"
        )  # Charger les données depuis le fichier JSON

    def set_current_profile(self, profile):
        self.current_profile = profile

    def fill_food_list(
        self, food_list
    ):  # Remplir la liste des aliments selon le fichier JSON
        for food in self.food_data.content:
            food_list.append(food.name)

    def search_foods(self, query: str):
        """Filtre les aliments selon la query de recherche (insensible à la casse)"""
        query = query.strip().lower()

        # Si la query est vide, afficher tous les aliments
        if not query:
            for food_name, food_data in self.view.food_items.items():
                food_data["checkbox"].pack(
                    side="left", padx=10, pady=10, fill="x", expand=True
                )
                food_data["frame"].pack(fill="x", padx=5, pady=5)
            return

        # Filtrer et afficher seulement les aliments qui correspondent
        for food_name, food_data in self.view.food_items.items():
            if query in food_name.lower():
                # Afficher l'aliment
                food_data["checkbox"].pack(
                    side="left", padx=10, pady=10, fill="x", expand=True
                )
                food_data["frame"].pack(fill="x", padx=5, pady=5)
            else:
                # Cacher l'aliment
                food_data["frame"].pack_forget()

    def previous_day(self, event):
        # Mettre a jour la date en mettant la date d'avant et ensuite mettre a jour le label
        self.current_date -= timedelta(days=1)
        self.update_date()

    def next_day(self, event):
        # Mettre a jour la date en mettant la date d'après et ensuite mettre a jour le label
        self.current_date += timedelta(days=1)
        self.update_date()

    def food_by_name(self, name):
        """Retourne un objet Food de la base de données selon son nom"""
        for food in self.food_data.content:
            if food.name == name:
                return food
        return None  # Si aucun aliment ne correspond au nom donné

    def add_menu(self):
        """Ouvre une nouvelle fenêtre pour ajouter un aliment avec sa quantité et l'ajoute à la liste de l'utilisateur une fois validé"""
        selected_foods = [
            food_name
            for food_name, data in self.view.food_items.items()
            if data["var"].get() == "on"
        ]

        if not selected_foods:
            message_box.CTkMessageBox(
                parent=self.view.winfo_toplevel(),
                title="Aucun aliment sélectionné",
                message="Veuillez sélectionner au moins un aliment avant d'ajouter un menu.",
                button_text="OK",
            )
            return  # Aucun aliment sélectionné, ne rien faire

        # Ouvrir la fenêtre de quantités
        quantity_window = food_quantity.FoodQuantity(
            selected_foods, parent=self.view.winfo_toplevel()
        )
        quantity_window.wait_window()  # Attendre que la fenêtre soit fermée
        quantities = quantity_window.quantities  # Récupérer les quantités saisies

        # Si l'utilisateur a annulé, ne rien faire
        if not quantities:
            return

        a_menu = menu.Menu(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )  # reformater la date pour le traitement des données avec .strptime lors de la désérialisation du JSON (pour la partie stat notamment)

        for food_name, quantity in quantities.items():
            food = self.food_by_name(food_name)
            if food and quantity > 0:  # Vérifier que la quantité est > 0
                a_menu.add_food_menu(
                    food=food,
                    quantity=quantity,
                )

        # Ne sauvegarder que si le menu contient au moins un aliment
        if not a_menu.content:
            return

        self.current_profile.eating_habits.append(a_menu)
        self.main_controller.settings.serialize(
            appdirs.user_data_dir("Nutritrack") + "/settings.json"
        )  # Sauvegarder les données après l'ajout du menu

        # Décocher toutes les cases
        for food_name, data in self.view.food_items.items():
            data["var"].set("off")

        self.display_menus()  # Mettre à jour l'affichage des menus après l'ajout

    def menus_today(self, date: datetime.date):
        """Retourne les menus consommés par l'utilisateur à un jour donné"""
        profile_menus = {}
        date_str = date.strftime("%Y-%m-%d")  # Formater la date pour la comparaison

        for menu in self.current_profile.eating_habits:
            if menu.date.startswith(
                date_str
            ):  # Vérifier si le menu correspond à la date donnée
                profile_menus[menu.date] = menu
        return profile_menus

    def macros_today(self, date: datetime.date):
        """Retourne les macros consommés par l'utilisateur à un jour donné"""
        total_macros = {"calories": 0, "carbohydrate": 0, "proteins": 0, "fats": 0}
        menus = self.menus_today(date)

        for menu in menus.values():
            for food_menu in menu.content:
                if food_menu.macros:
                    macro = food_menu.macros[0]
                    ratio = food_menu.quantity / 100
                    total_macros["calories"] += macro.calorie * ratio
                    total_macros["proteins"] += macro.proteine * ratio
                    total_macros["carbohydrate"] += macro.carbohydrate * ratio
                    total_macros["fats"] += macro.fat * ratio
        return total_macros

    def delete_menu(self, menu_time: str):
        """Supprime un menu par sa date (timestamp) et met à jour l'affichage."""
        if self.current_profile is None:
            return
        self.current_profile.eating_habits = [
            menu
            for menu in self.current_profile.eating_habits
            if menu.date != menu_time
        ]
        self.main_controller.settings.serialize(
            appdirs.user_data_dir("Nutritrack") + "/settings.json"
        )
        self.display_menus()

    def display_menus(self):
        """Affiche les menus consommés pour la date courante"""
        # Nettoyer la scrollable frame
        for widget in self.view.menus_scrollable_frame.winfo_children():
            widget.destroy()

        # Récupérer les menus du jour
        menus = self.menus_today(self.current_date)

        # Afficher "Aucun menu consommé" s'il n'y a pas de menu
        if not menus:
            no_menu_label = ctk.CTkLabel(
                self.view.menus_scrollable_frame,
                text="Aucun menu consommé aujourd'hui",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#A8AFB6",
            )
            no_menu_label.pack(padx=10, pady=20)
            # Mettre à jour les labels des macros à zéro
            self.view.calories_value_label.configure(text="0 kcal")
            self.view.proteines_value_label.configure(text="0 g")
            self.view.glucides_value_label.configure(text="0 g")
            self.view.lipides_value_label.configure(text="0 g")
            return

        # Afficher chaque menu du jour
        for menu_time, menu_obj in menus.items():
            # Créer un frame pour chaque menu
            menu_frame = ctk.CTkFrame(
                self.view.menus_scrollable_frame, fg_color="#2A2A4A", corner_radius=8
            )
            menu_frame.pack(fill="x", padx=5, pady=5)

            header_frame = ctk.CTkFrame(menu_frame, fg_color="#2A2A4A")
            header_frame.pack(fill="x", padx=10, pady=(8, 0))

            # Afficher l'heure du menu
            time_label = ctk.CTkLabel(
                header_frame,
                text=menu_time.split(" ")[1],  # Extraire l'heure (HH:MM:SS)
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#4CAF50",
            )
            time_label.pack(side="left")

            delete_button = ctk.CTkButton(
                header_frame,
                text="Supprimer",
                width=90,
                height=24,
                corner_radius=6,
                fg_color="#D9534F",
                hover_color="#C9302C",
                text_color="#FFFFFF",
                command=lambda mt=menu_time: self.delete_menu(mt),
            )
            delete_button.pack(side="right")

            # Afficher les aliments du menu
            for food_menu in menu_obj.content:
                food_label = ctk.CTkLabel(
                    menu_frame,
                    text=f"• {food_menu.name} ({food_menu.quantity}g)",
                    font=ctk.CTkFont(size=11),
                    text_color="#FFFFFF",
                )
                food_label.pack(anchor="w", padx=20, pady=2)

        # Mettre à jour les labels des macros totales
        macros = self.macros_today(self.current_date)
        self.view.calories_value_label.configure(text=f"{int(macros['calories'])} kcal")
        self.view.proteines_value_label.configure(text=f"{int(macros['proteins'])} g")
        self.view.glucides_value_label.configure(
            text=f"{int(macros['carbohydrate'])} g"
        )
        self.view.lipides_value_label.configure(text=f"{int(macros['fats'])} g")

    def update_date(self):
        # Mettre a jour sur la vue la date affiché dans le label
        self.view.date_label.configure(
            text=self.current_date.strftime("  %A %d %B %Y  ").capitalize()
        )
        self.display_menus()
