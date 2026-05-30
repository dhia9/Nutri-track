from datetime import datetime, timedelta
import unicodedata
import appdirs
import customtkinter as ctk
import src.controllers.main_controller as main_controller
import src.models.menu as Menu
import src.views.food_quantity as food_quantity
import src.views.message_box as message_box
from src.views.fav_win import FavorieMenuWindow
from src.views.suggestedMenus import SuggestedMenuWindow


class NutritionController:
    def __init__(self, main_controller: main_controller):
        self.main_controller = main_controller
        self.view = None  # La view sera assignée par la view elle-même
        self.current_profile = self.main_controller.current_profile
        self.current_date = datetime.now()
        self.favorite_menus = (
            self.main_controller.settings.favorites_menus
        )  # Récupérer les menus favoris depuis les paramètres
        self.suggested_menus = None

    def set_current_profile(self, profile):
        """Définit le profil actuel.

        Args:
            profile: Le profil à définir comme profil actuel.
        """
        self.current_profile = profile

    def fill_food_list(self, food_list):
        """Remplit une liste avec tous les aliments disponibles.

        Args:
        food_list: La liste à remplir avec les noms des aliments.
        """
        for food in self.main_controller.food_data.content:
            food_list.append(food.name)

    def format_text(self, texte):
        texte = unicodedata.normalize("NFD", texte)
        resultat = ""
        for c in texte:
            if unicodedata.combining(c) == 0:
                resultat += c
        return (
            resultat.strip().lower()
        )  # Enlever les accents, les espaces en début et fin, et mettre en minuscules

    def search_foods(self, query: str):
        """Filtre les aliments selon la requête de recherche.

        La recherche est insensible à la case. Affiche/masque les aliments
        qui correspondent dans l'interface.

        Args:
            query: La chaîne de recherche.
        """
        query = self.format_text(query)

        # Si la query est vide, afficher tous les aliments
        if not query:
            self.view.is_filtered = False
            self.view.current_page = 0
            self.view._display_current_page()
            return

        # Filtrer les aliments
        filtered_foods = [
            food for food in self.view.all_foods if query in self.format_text(food)
        ]

        # Mettre à jour la pagination
        self.view._update_pagination(filtered_foods)

    def previous_day(self, event):
        """Affiche le jour précédent et met à jour l'affichage.

        Args:
            event: L'événement lié au clic du bouton.
        """
        # Mettre a jour la date en mettant la date d'avant et ensuite mettre a jour le label
        self.current_date -= timedelta(days=1)
        self.update_date()

    def next_day(self, event):
        """Affiche le jour suivant et met à jour l'affichage.

        Args:
            event: L'événement lié au clic du bouton.
        """
        # Mettre a jour la date en mettant la date d'après et ensuite mettre a jour le label
        self.current_date += timedelta(days=1)
        self.update_date()

    def go_to_today(self, event=None):
        # Mettre à jour la date à aujourd'hui
        self.current_date = datetime.now()
        self.update_date()

    def previous_page(self):
        """Aller à la page précédente"""
        if self.view.current_page > 0:
            self.view.current_page -= 1
            self.view._display_current_page()

    def next_page(self):
        """Aller à la page suivante"""
        foods_to_display = (
            self.view.filtered_foods if self.view.is_filtered else self.view.all_foods
        )
        total_pages = (
            len(foods_to_display) + self.view.items_per_page - 1
        ) // self.view.items_per_page

        if self.view.current_page < total_pages - 1:
            self.view.current_page += 1
            self.view._display_current_page()

    def food_by_name(self, name):
        """Retourne un objet Food de la base de données selon son nom.

        Args:
            name: Le nom de l'aliment.

        Returns:
            L'objet Food correspondant ou None si non trouvé.
        """
        for food in self.main_controller.food_data.content:
            if food.name == name:
                return food
        return None  # Si aucun aliment ne correspond au nom donné

    def add_menu(self):
        """Ouvre une nouvelle fenêtre pour ajouter un aliment avec sa quantité et l'ajoute à la liste de l'utilisateur une fois validé"""
        selected_foods = [
            food_name
            for food_name, is_selected in self.view.selected_foods.items()
            if is_selected
        ]

        if not selected_foods:
            message_box.CTkMessageBox(
                parent=self.view.winfo_toplevel(),
                main_controller=self.main_controller,
                title="Aucun aliment sélectionné",
                message="Veuillez sélectionner au moins un aliment avant d'ajouter un menu.",
                button_text="OK",
            )
            return  # Aucun aliment sélectionné, ne rien faire

        # Ouvrir la fenêtre de quantités
        quantity_window = food_quantity.FoodQuantity(
            selected_foods,
            parent=self.view.winfo_toplevel(),
            main_controller=self.main_controller,
        )
        quantity_window.wait_window()  # Attendre que la fenêtre soit fermée
        quantities = quantity_window.quantities  # Récupérer les quantités saisies

        # Si l'utilisateur a annulé, ne rien faire
        if not quantities:
            return
        now = datetime.now()
        menu_date = self.current_date.replace(
            hour=now.hour, minute=now.minute, second=now.second
        )
        a_menu = Menu.Menu(
            menu_date.strftime("%Y-%m-%d %H:%M:%S")
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
        self.view.selected_foods.clear()  # Vider le dictionnaire de sélections
        self.view._display_current_page()  # Rafraîchir l'affichage

        self.display_menus()  # Mettre à jour l'affichage des menus après l'ajout

    def menus_today(self, date: datetime.date):
        """Retourne les menus consommés par l'utilisateur à un jour donné"""
        profile_menus = []
        date_str = date.strftime("%Y-%m-%d")  # Formater la date pour la comparaison

        for menu in self.current_profile.eating_habits:
            if menu.date.startswith(
                date_str
            ):  # Vérifier si le menu correspond à la date donnée
                profile_menus.append(menu)
        return profile_menus

    def macros_today(self, date: datetime.date):
        """Retourne les macros consommés par l'utilisateur à un jour donné"""
        total_macros = {"calories": 0, "carbohydrate": 0, "proteins": 0, "fats": 0}
        menus = self.menus_today(date)

        for menu in menus:
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

    def toggle_favorite(self, menu: Menu.Menu):
        """Ajoute ou retire un menu des favoris et met à jour l'affichage.

        Args:
            menu: Le menu à ajouter/retirer des favoris.
        """
        # Chercher un favori avec la même composition
        matching_favorite = None
        for fav in self.favorite_menus:
            if menu.has_same_composition(fav):
                matching_favorite = fav
                break

        if matching_favorite:
            # Enlever le favori avec la même composition
            self.favorite_menus.remove(matching_favorite)
        else:
            self.favorite_menus.add(menu)
        # Mettre à jour l'affichage
        self.display_menus()
        # Sauvegarder les favoris dans les paramètres
        self.main_controller.settings.serialize(
            appdirs.user_data_dir("Nutritrack") + "/settings.json"
        )

    def display_menus(self):
        """Affiche les menus consommés pour la date courante"""
        # Nettoyer la scrollable frame
        for widget in self.view.menus_container.winfo_children():
            widget.destroy()

        # Récupérer les menus du jour
        menus = self.menus_today(self.current_date)

        # Afficher "Aucun menu consommé" s'il n'y a pas de menu
        if not menus:
            no_menu_label = ctk.CTkLabel(
                self.view.menus_container,
                text="Aucun menu consommé aujourd'hui",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=self.main_controller.theme_colors["text_secondary"],
            )
            no_menu_label.pack(padx=10, pady=20)
            # Mettre à jour les labels des macros à zéro
            self.view.calories_value_label.configure(text="0 kcal")
            self.view.proteines_value_label.configure(text="0 g")
            self.view.glucides_value_label.configure(text="0 g")
            self.view.lipides_value_label.configure(text="0 g")
            return

        # Afficher chaque menu du jour
        for menu_obj in menus:
            menu_time = menu_obj.date
            # Créer un frame pour chaque menu
            menu_frame = ctk.CTkFrame(
                self.view.menus_container,
                fg_color=self.main_controller.theme_colors["frame_dark"],
                corner_radius=8,
            )
            menu_frame.pack(fill="x", padx=5, pady=5)

            header_frame = ctk.CTkFrame(
                menu_frame, fg_color=self.main_controller.theme_colors["frame_dark"]
            )
            header_frame.pack(fill="x", padx=10, pady=(8, 0))

            # Afficher l'heure du menu
            time_label = ctk.CTkLabel(
                header_frame,
                text=menu_time.split(" ")[1],  # Extraire l'heure (HH:MM:SS)
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=self.main_controller.settings.theme,  # Utiliser la couleur du thème pour l'heure
            )
            time_label.pack(side="left")

            # Frame pour les boutons à droite (étoile au-dessus, supprimer en bas)
            right_buttons_frame = ctk.CTkFrame(
                header_frame, fg_color=self.main_controller.theme_colors["frame_dark"]
            )
            right_buttons_frame.pack(side="right", padx=5)

            # Étoile pour les favoris (cliquable)
            is_favorite = any(
                menu_obj.has_same_composition(fav) for fav in self.favorite_menus
            )

            star_text = "★" if is_favorite else "☆"
            star_button = ctk.CTkButton(
                right_buttons_frame,
                text=star_text,
                width=30,
                height=24,
                corner_radius=6,
                fg_color=self.main_controller.theme_colors["frame_dark"],
                hover_color=self.main_controller.theme_colors["button_hover"],
                text_color="#FFD700",
                font=ctk.CTkFont(size=16),
                command=lambda m=menu_obj: self.toggle_favorite(m),
            )
            star_button.pack(pady=(0, 5))
            # Stocker la référence pour mise à jour ultérieure
            setattr(star_button, "menu_obj", menu_obj)
            setattr(star_button, "is_favorite", is_favorite)

            # Bouton supprimer
            delete_button = ctk.CTkButton(
                right_buttons_frame,
                text="Supprimer",
                width=80,
                height=24,
                corner_radius=10,
                fg_color=self.main_controller.theme_colors["error"],
                hover_color=self.main_controller.theme_colors["error_hover"],
                text_color=self.main_controller.theme_colors["text"],
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda mt=menu_time: self.delete_menu(mt),
            )
            delete_button.pack()

            # Afficher les aliments du menu
            for food_menu in menu_obj.content:
                food_label = ctk.CTkLabel(
                    menu_frame,
                    text=f"• {food_menu.name} ({food_menu.quantity}g)",
                    font=ctk.CTkFont(size=11),
                    text_color=self.main_controller.theme_colors.get("text", "#F1F1F1"),
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

    def show_favorite_menus(self, event):
        """Affiche la fenêtre des menus favoris"""
        fav_win = FavorieMenuWindow(self.view.winfo_toplevel(), self.main_controller)
        fav_win.wait_window()  # Attendre que la fenêtre soit fermée

    def show_Suggested_menus(self, event=None):
        """Affiche la fenêtre des menus proposés par l'algorithme"""
        nap = int(self.current_profile.suggestCaracteristics["nap"])
        meals_per_day = int(self.current_profile.suggestCaracteristics["meals_per_day"])
        self.suggested_menus = self.current_profile.generate_menu(
            self.main_controller.food_data, nap, meals_per_day
        )
        Suggestion_win = SuggestedMenuWindow(
            self.view.winfo_toplevel(), self.main_controller
        )
        Suggestion_win.wait_window()  # Attendre que la fenêtre soit fermée

    def mealPerD_change(self, event=None):
        self.current_profile.suggestCaracteristics["meals_per_day"] = (
            self.view.input_mealPerD.get()
        )

    def nap_change(self, event=None):
        self.current_profile.suggestCaracteristics["nap"] = self.view.input_nap.get()

    def add_suggested_menu(self, menu, window):
        menu.date = self.current_date.strftime("%Y-%m-%d %H:%M:%S")
        self.current_profile.eating_habits.append(menu)
        self.main_controller.settings.serialize(
            appdirs.user_data_dir("Nutritrack") + "/settings.json"
        )

        self.display_menus()
        window.destroy()
