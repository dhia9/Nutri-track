import random
from datetime import date

from src.data.food_data import FoodData
from src.models.food import Food
from src.models.macro import Macro
from src.models.menu import Menu
from src.models.model import Model

MEAL_SPLITS = {
    1: [1.00],
    2: [0.40, 0.60],
    3: [0.25, 0.40, 0.35],
    4: [0.20, 0.35, 0.30, 0.15],
    5: [0.15, 0.30, 0.30, 0.15, 0.10],
    6: [0.15, 0.10, 0.30, 0.10, 0.25, 0.10],
}


class Profile(Model):
    def __init__(self, name, age, height, weight, sex, target_weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.sex = sex
        self.target_weight = target_weight
        self.eating_habits = []

    def get_imc(self):
        if self.height > 0:
            return self.weight / (self.height**2)
        else:
            return 0

    def get_nutritional_needs(self, nap=1.55) -> dict:
        """
        Cette fonction retourne dans un dictionnaire les différents besoins journaliers nutrionels pour ce profil.
        :param nap: Facteur d'actvitié physique
        :return: Un dictionnaire avec toutes les informations sur les nutriments à consommer chaque jour.
        :rtype: dict
        Exemple :
        MB          : 1 801 kcal\n
        DET         : 2 791 kcal\n
        Cible       : 3 091 kcal\n
        Protéines   : 216 g\n
        Glucides    : 387 g\n
        Lipides     :  76 g\n
        """
        # 1. Métabolisme de base (Mifflin-St Jeor)
        if self.sex == "Homme":
            mb = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            mb = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

        # 2. Dépense énergétique totale
        det = mb * nap

        if self.target_weight > self.weight:
            objectif = "masse"
        elif self.target_weight < self.weight:
            objectif = "perte"
        else:
            objectif = "maintien"

        # 3. Ajustement objectif
        ajustements = {"perte": -400, "maintien": 0, "masse": 300}
        calories = det + ajustements[objectif]

        # 4. Macros (ratios selon objectif)
        ratios = {
            "perte": {"proteines": 0.32, "lipides": 0.27, "glucides": 0.41},
            "maintien": {"proteines": 0.22, "lipides": 0.28, "glucides": 0.50},
            "masse": {"proteines": 0.28, "lipides": 0.22, "glucides": 0.50},
        }[objectif]

        return {
            "calories": calories,
            "proteines_g": (calories * ratios["proteines"]) / 4,
            "lipides_g": (calories * ratios["lipides"]) / 9,
            "glucides_g": (calories * ratios["glucides"]) / 4,
        }

    def get_consumed_today(self, today: str) -> tuple[float, float, float, float]:
        """Calcule les macros déjà consommées aujourd'hui."""
        menus_today = [m for m in self.eating_habits if m.date == today]
        cal = sum(f.macros[0].calorie for m in menus_today for f in m.content)
        prot = sum(f.macros[0].proteine for m in menus_today for f in m.content)
        fat = sum(f.macros[0].fat for m in menus_today for f in m.content)
        carb = sum(f.macros[0].carbohydrate for m in menus_today for f in m.content)
        return cal, prot, fat, carb

    def get_meal_budget(
        self, nap: float, meals_per_day: int, today: str
    ) -> tuple[float, float, float, float]:
        """
        Calcule le budget macro pour le prochain repas.
        = (besoins journaliers - déjà consommé) / repas restants
        """
        besoins = self.get_nutritional_needs(nap)

        cal_consumed, prot_consumed, fat_consumed, carb_consumed = (
            self.get_consumed_today(today)
        )

        # Repas déjà effectués aujourd'hui
        meals_done = sum(1 for m in self.eating_habits if m.date == today)
        meals_remaining = max(1, meals_per_day - meals_done)

        return (
            max(0.0, besoins["calories"] - cal_consumed) / meals_remaining,
            max(0.0, besoins["proteines_g"] - prot_consumed) / meals_remaining,
            max(0.0, besoins["lipides_g"] - fat_consumed) / meals_remaining,
            max(0.0, besoins["glucides_g"] - carb_consumed) / meals_remaining,
        )

    def get_used_today(self, today: str) -> set[str]:
        """Retourne les noms des aliments déjà consommés aujourd'hui (à éviter)."""
        return {
            f.name for m in self.eating_habits if m.date == today for f in m.content
        }

    def pick_best_food(
        self,
        food_data: FoodData,
        cal_budget: float,
        prot_budget: float,
        fat_budget: float,
        carb_budget: float,
        used_in_meal: set[str],
        used_today: set[str],
        base_portion_g: float,
    ) -> Food | None:
        """
        Sélectionne l'aliment le plus compatible avec le budget macro restant.
        Ajoute un bruit aléatoire pour varier les menus générés.
        """
        candidates = [
            (
                food,
                food.score(
                    cal_budget, prot_budget, fat_budget, carb_budget, base_portion_g
                )
                + random.uniform(0, 0.05),
            )
            for food in food_data.content
            if food.name not in used_in_meal
            and food.name not in used_today
            and food.macros  # guard: skip foods with no macro entry
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda x: x[1])[0]

    def compute_portion(
        self, food: Food, cal_budget: float, base_portion_g: float
    ) -> tuple[float, Macro]:
        """
        Calcule la portion en grammes (clamped pour ne pas dépasser le budget calorique)
        et retourne le Macro correspondant.
        """
        ref_macro = food.macros[0]

        # Portion maximale avant de dépasser le budget calorique
        cal_per_g = ref_macro.calorie / ref_macro.masse
        max_g = (cal_budget / cal_per_g) if cal_per_g > 0 else base_portion_g
        portion_g = round(max(30.0, min(base_portion_g, max_g)))

        # Macro class gère le scaling masse → quantité en interne
        scaled_macro = Macro(
            portion_g,
            ref_macro.proteine / (ref_macro.masse / 100),  # back to per-100g
            ref_macro.calorie / (ref_macro.masse / 100),
            ref_macro.fat / (ref_macro.masse / 100),
            ref_macro.carbohydrate / (ref_macro.masse / 100),
        )
        return portion_g, scaled_macro

    def generate_menu(
        self,
        food_data: FoodData,
        nap: float = 1.55,
        meals_per_day: int = 3,
    ) -> Menu:
        """
        Génère UN seul repas pour compléter la journée en cours.

        - Tient compte des repas déjà enregistrés aujourd'hui (eating_habits)
        - Répartit équitablement les macros restantes sur les repas futurs
        """
        today = str(date.today())

        BASE_PORTION_G = 150
        MAX_ITEMS_PER_MEAL = 4

        # Budget macro pour ce repas = restant / repas encore à faire
        cal_budget, prot_budget, fat_budget, carb_budget = self.get_meal_budget(
            nap, meals_per_day, today
        )

        # Aliments déjà consommés aujourd'hui (à éviter pour varier)
        used_today = self.get_used_today(today)
        used_in_meal: set[str] = set()
        menu = Menu(today)

        for _ in range(MAX_ITEMS_PER_MEAL):
            if cal_budget <= 50:
                break

            # Sélection de l'aliment le plus adapté au budget restant
            best_food = self.pick_best_food(
                food_data,
                cal_budget,
                prot_budget,
                fat_budget,
                carb_budget,
                used_in_meal,
                used_today,
                BASE_PORTION_G,
            )
            if best_food is None:
                break

            # Calcul de la portion et du Macro associé
            portion_g, scaled_macro = self.compute_portion(
                best_food, cal_budget, BASE_PORTION_G
            )

            menu.add_food_menu(Food(best_food.name, [scaled_macro]), quantity=portion_g)
            used_in_meal.add(best_food.name)
            used_today.add(best_food.name)

            # Mise à jour du budget restant pour les prochains aliments du repas
            cal_budget -= scaled_macro.calorie
            prot_budget -= scaled_macro.proteine
            fat_budget -= scaled_macro.fat
            carb_budget -= scaled_macro.carbohydrate

        return menu
