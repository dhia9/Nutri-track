import random
import os
import appdirs
from datetime import datetime, timedelta


class StatsController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view = None
        self.current_date = datetime.now()
        self.mesures_corporelles = []

    def macros_by_date(self):
        result = {"calories": {}, "carbohydrate": {}, "proteins": {}, "fats": {}}
        if self.main_controller.current_profile is None:
            return result
        menus_end_to_end = self.menus_all_dates()
        for menu in menus_end_to_end.values():
            if not hasattr(menu, "date") or not hasattr(menu, "content"):
                continue
            date = menu.date[:10]
            for food_menu in menu.content:
                if food_menu.macros:
                    macro = food_menu.macros[0]
                    ratio = food_menu.quantity / 100
                    if date not in result["calories"]:
                        result["calories"][date] = 0
                        result["proteins"][date] = 0
                        result["carbohydrate"][date] = 0
                        result["fats"][date] = 0
                    result["calories"][date] += macro.calorie * ratio
                    result["proteins"][date] += macro.proteine * ratio
                    result["carbohydrate"][date] += macro.carbohydrate * ratio
                    result["fats"][date] += macro.fat * ratio
        return result

    def menus_all_dates(self):
        profile_menus = {}
        if self.main_controller.current_profile is None:
            return profile_menus
        for menu in self.main_controller.current_profile.eating_habits:
            profile_menus[menu.date] = menu
        return profile_menus

    def menus_today(self, date: datetime.date):
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
        """Retourne les macros consommés par l'utilisateur à un jour donné"""
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
        return self.main_controller.current_profile

    def generate_history(self, days=30):
        history = []
        today = datetime.today()
        for i in range(days):
            date = today - timedelta(days=(days - i))
            history.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "calories": random.randint(1800, 2600),
                    "proteins": random.randint(70, 140),
                    "carbs": random.randint(150, 300),
                    "fats": random.randint(40, 90),
                    "salt": round(random.uniform(3, 9), 1),
                    "sugar": round(random.uniform(20, 70), 1),
                }
            )
        return history

    def mesure_avg(self, data, macro_type):
        total = 0
        for item in data:
            total += item[macro_type]
        return total / len(data) if data else 0

    def update_date(self):
        # Mettre a jour sur la vue la date affiché dans le label
        self.view.date_label.configure(
            text=self.current_date.strftime("  %A %d %B %Y  ").capitalize()
        )

    def previous_day(self, event):
        # Mettre a jour la date en mettant la date d'avant et ensuite mettre a jour le label
        self.current_date -= timedelta(days=1)
        self.update_date()

    def next_day(self, event):
        # Mettre a jour la date en mettant la date d'après et ensuite mettre a jour le label
        self.current_date += timedelta(days=1)
        self.update_date()

    def ajouter_mesure(self, mesure):
        # Ajouter la mesure au profil courant
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
        """Retourne les mesures corporelles du profil courant"""
        if self.main_controller.current_profile is not None:
            return self.main_controller.current_profile.mesures_corporelles
        return []
