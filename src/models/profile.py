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
            return self.weight / (self.height ** 2)
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

    def generate_menu(
            self: Profile,
            food_data: FoodData,
            nap: float = 1.55,
            meals_per_day: int = 3,
    ) -> Menu:
        """
        Generates a daily menu for a given profile.

        Args:
            self       : Profile instance
            food_data     : FoodData instance (already deserialized)
            nap           : activity factor (1.2 → 1.9)
            meals_per_day : number of meals (1–6)

        Returns:
            A Menu instance populated with FoodMenu entries.
        """

        meals_per_day = max(1, min(meals_per_day, 6))
        besoins = self.get_nutritional_needs(nap)
        splits = MEAL_SPLITS[meals_per_day]
        menu = Menu(str(date.today()))
        used_today: set[str] = set()

        BASE_PORTION_G = 150
        MAX_ITEMS_PER_MEAL = 4

        for ratio in splits:
            # Macro budget for this meal
            cal_left = besoins["calories"] * ratio
            prot_left = besoins["proteines_g"] * ratio
            fat_left = besoins["lipides_g"] * ratio
            carb_left = besoins["glucides_g"] * ratio
            used_in_meal: set[str] = set()

            for _ in range(MAX_ITEMS_PER_MEAL):
                if cal_left <= 50:
                    break

                # Score every unused food + small random noise to vary menus
                candidates = [
                    (
                        food,
                        food.score(
                            cal_left, prot_left, fat_left, carb_left, BASE_PORTION_G
                        )
                        + random.uniform(0, 0.05),
                    )
                    for food in food_data.content
                    if food.name not in used_in_meal
                       and food.name not in used_today
                       and food.macros  # guard: skip foods with no macro entry
                ]
                if not candidates:
                    break

                best_food = max(candidates, key=lambda x: x[1])[0]
                ref_macro = best_food.macros[0]

                # Clamp portion so we don't overshoot the calorie budget
                cal_per_g = ref_macro.calorie / ref_macro.masse
                max_g = (cal_left / cal_per_g) if cal_per_g > 0 else BASE_PORTION_G
                portion_g = round(max(30.0, min(BASE_PORTION_G, max_g)))

                # Use your Macro class — it handles the masse→quantity scaling
                scaled_macro = Macro(
                    portion_g,
                    ref_macro.proteine / (ref_macro.masse / 100),  # back to per-100g
                    ref_macro.calorie / (ref_macro.masse / 100),
                    ref_macro.fat / (ref_macro.masse / 100),
                    ref_macro.carbohydrate / (ref_macro.masse / 100),
                )

                menu.add_food_menu(Food(best_food.name, [scaled_macro]), quantity=portion_g)

                used_in_meal.add(best_food.name)
                used_today.add(best_food.name)

                cal_left -= scaled_macro.calorie
                prot_left -= scaled_macro.proteine
                fat_left -= scaled_macro.fat
                carb_left -= scaled_macro.carbohydrate

        return menu
