import random
import os
import appdirs
from datetime import datetime, timedelta
import customtkinter as ctk


class StatsController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view = None
        self.current_date = datetime.now()
        self.mesures_corporelles = []
        self.duree = {"calor": None, "macro": None, "corpo": None}

    def macros_by_date(self):
        result = {"calories": {}, "carbohydrate": {}, "proteins": {}, "fats": {}}

        if self.main_controller.current_profile is None:
            return result

        menus_end_to_end = self.menus_all_dates()

        for menu in menus_end_to_end.values():
            if not hasattr(menu, "date") or not hasattr(menu, "content"):
                continue

            date = datetime.fromisoformat(menu.date).date()  # <-- JOUR UNIQUEMENT

            if date not in result["calories"]:
                result["calories"][date] = 0
                result["proteins"][date] = 0
                result["carbohydrate"][date] = 0
                result["fats"][date] = 0

            for food_menu in menu.content:
                if food_menu.macros:
                    macro = food_menu.macros[0]
                    ratio = food_menu.quantity / 100

                    result["calories"][date] += macro.calorie * ratio
                    result["proteins"][date] += macro.proteine * ratio
                    result["carbohydrate"][date] += macro.carbohydrate * ratio
                    result["fats"][date] += macro.fat * ratio

        return result

    def menus_all_dates(self):
        """Retourne tous les menus de tous les jours du profil actuel.

        Returns:
            Dictionnaire avec les menus indexés par date.
        """
        profile_menus = {}
        if self.main_controller.current_profile is None:
            return profile_menus
        for menu in self.main_controller.current_profile.eating_habits:
            profile_menus[menu.date] = menu
        return profile_menus

    def menus_today(self, date: datetime.date):
        """Retourne les menus d'un jour spécifique.

        Args:
            date: La date pour laquelle récupérer les menus.

        Returns:
            Dictionnaire des menus pour cette date.
        """
        profile_menus = {}
        if self.main_controller.current_profile is None:
            return profile_menus
        date_str = date.strftime("%Y-%m-%d")  # Formater la date pour la comparaison
        for menu in self.main_controller.current_profile.eating_habits:
            if menu.date.startswith(
                date_str
            ):  # Vérifier si le menu correspond à la date donnée
                profile_menus[menu.date] = menu
        return profile_menus

    def macros_today(self, date: datetime.date):
        """Retourne les macros consommés par l'utilisateur à un jour donné.

        Args:
            date: La date pour laquelle récupérer les macros.

        Returns:
            Dictionnaire with calories, carbohydrate, proteins, and fats totals.
        """
        total_macros = {"calories": 0, "carbohydrate": 0, "proteins": 0, "fats": 0}
        if self.main_controller.current_profile is None:
            return total_macros
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

    def get_current_profile(self):
        """Retourne le profil actuellement sélectionné.

        Returns:
            Le profil Profile actuel ou None.
        """
        return self.main_controller.current_profile

    def generate_history(self, days=30):
        """Génére un historique de données sur un nombre de jours.

        Returns des données aléatoires pour les tests.

        Args:
            days: Le nombre de jours d'historique à générer.

        Returns:
            Liste de dictionnaires contenant les données par jour.
        """
        history = []
        today = datetime.today()
        for i in range(days):
            date = today - timedelta(days=(days - i))
            history.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "calories": random.randint(1800, 2600),
                    "proteins": random.randint(70, 140),
                    "carbohydrate": random.randint(150, 300),
                    "fats": random.randint(40, 90),
                    "salt": round(random.uniform(3, 9), 1),
                    "sugar": round(random.uniform(20, 70), 1),
                }
            )
        return history

    def mesure_avg(self, data, macro_type):
        """Calcule la moyenne d'un type de macro pour une liste de données.

        Args:
            data: Liste de dictionnaires de données.
            macro_type: La clé du macro à moyenner.

        Returns:
            La moyenne du macro_type ou 0 si aucune donnée.
        """
        total = 0
        for item in data:
            total += item[macro_type]
        return total / len(data) if data else 0

    def update_date(self):
        """
        Mettre a jour sur la vue la date affiché dans le label

        returns:None
        """
        self.view.date_label.configure(
            text=self.current_date.strftime("  %A %d %B %Y  ").capitalize()
        )

    def previous_day(self, event):
        """
        Mettre a jour la date en mettant la date d'avant et ensuite mettre a jour le label

        Parameters
            event : tk.Event
            Événement déclenché par le callback (clic sur le bouton).
        Returns:
            None"""
        self.current_date -= timedelta(days=1)
        self.update_date()

    def next_day(self, event):
        """
        Mettre a jour la date en mettant la date d'après et ensuite mettre a jour le label

        Parameters
            event : tk.Event
            Événement déclenché par le callback (clic sur le bouton).
        Returns:
            None"""
        self.current_date += timedelta(days=1)
        self.update_date()

    def ajouter_mesure(self, mesure):
        """
        Ajouter la mesure au profil courant

        Parameters:
            mesure:Model mesure_coporelles
        Returns:
            None"""
        if self.main_controller.current_profile is not None:
            self.main_controller.current_profile.mesures_corporelles.append(mesure)
            # Sauvegarder les modifications dans le fichier JSON
            settings_path = os.path.join(
                appdirs.user_data_dir("Nutritrack"), "settings.json"
            )
            self.main_controller.settings.serialize(settings_path)
        # Garder aussi en mémoire dans le contrôleur pour la vue actuelle
        self.mesures_corporelles.append(mesure)
        return self.mesures_corporelles

    def get_mesures_corporelles(self):
        """
        Retourne les mesures corporelles du profil courant

        Returns:
            None
        """
        if self.main_controller.current_profile is not None:
            return self.main_controller.current_profile.mesures_corporelles
        return []

    def _update_charts_only(self):
        """
        Rafraîchit uniquement la zone des graphiques et du tableau de statistiques.
        Cette méthode permet une mise à jour partielle de l'interface sans
        reconstruire entièrement la page.
        Args:
            None
        Returns:
            None

        """
        for child in self.view.scroll.winfo_children():
            child.destroy()
        self.view.table_rows = []
        self.view._render_all_charts()

    def _create_ligne_mesure(self, mesure):
        """
        Ajoute une nouvelle ligne dans le tableau d'historique des mesures corporelles.
        Args:
            mesure (MesuresCorporelles):
        Returns:
            None

        """
        values = [
            mesure.date,
            mesure.poids,
            mesure.tour_de_taille,
            mesure.tour_de_bras,
            mesure.masse_grasse,
        ]

        row_widget = []

        for col, value in enumerate(values):
            label = ctk.CTkLabel(self.view.tableau_frame, text=value)
            label.grid(row=len(self.view.table_rows) + 1, column=col, padx=35, pady=5)
            row_widget.append(label)

        self.view.table_rows.append(row_widget)

    def change_period(self, days, type):
        """
        Met à jour la durée , puis rafraîchit la vue.
        Parameters:
        days : int
            Nombre de jours à appliquer pour la période.
        type : str
            Clé représentant le type de période à modifier dans self.duree.

        Returns:
        None
        """
        self.duree[type] = days
        # refresh complet
        # self.view.refresh()
        if type == "macro":
            self.refresh_macro_only()

        elif type == "calor":
            self.refresh_calories_only()

        elif type == "corpo":
            self.refresh_corpo_only()

    def refresh_calories_only(self):
        self.macrosDated = self.macros_by_date()
        data = self.macrosDated["calories"]
        if self.view.calories_canvas:
            self.view.calories_canvas.get_tk_widget().destroy()
        if self.view.calories_widget:
            self.view.calories_widget.destroy()
            self.view.calories_widget = None
        self.view._draw_calories_chart(self.view.calories_card, data)

    def refresh_macro_only(self):
        self.macrosDated = self.macros_by_date()
        if self.view.macro_widget:
            self.view.macro_widget.destroy()
            self.view.macro_widget = None
        self.view._draw_caracteristics_chart(self.view.macros_card)

    def refresh_corpo_only(self):

        if self.view.corpo_widget:
            self.view.corpo_widget.destroy()
            self.view.corpo_widget = None

        self.view._draw_corpo_chart(self.view.corpo_card)

    def last_n_elements(self, l, n):
        """
        Retourne les n derniers éléments d'une liste.
        Parameters:

        l : list
            Liste source.
        n : int
            Nombre d'éléments à récupérer depuis la fin de la liste.

        Returns:
        list
            Sous-liste contenant les n derniers éléments.
        """
        return l[(-1 * n) :]
