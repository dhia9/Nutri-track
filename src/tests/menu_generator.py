from datetime import date
from src.data.food_data import FoodData
from src.models.food import Food
from src.models.macro import Macro
from src.models.menu import Menu
from src.models.profile import Profile


def make_menu(items: list[tuple[str, float, float, float, float, float]]) -> Menu:
    menu = Menu(str(date.today()))
    for name, masse, prot, cal, fat, carb in items:
        menu.add_food_menu(
            Food(name, [Macro(masse, prot, cal, fat, carb)]), quantity=masse
        )
    return menu


def check_nutritional_targets(
    menu: Menu,
    target_cal: float,
    target_prot: float,
    target_fat: float,
    target_carb: float,
    threshold: float = 0.60,
) -> bool:
    """Vérifie si les macros du menu atteignent les objectifs à un certain seuil (par défaut 60%)."""
    total_cal = sum(f.macros[0].calorie for f in menu.content)
    total_prot = sum(f.macros[0].proteine for f in menu.content)
    total_fat = sum(f.macros[0].fat for f in menu.content)
    total_carb = sum(f.macros[0].carbohydrate for f in menu.content)

    return (
        total_cal >= target_cal * threshold
        and total_prot >= target_prot * threshold
        and total_fat >= target_fat * threshold
        and total_carb >= target_carb * threshold
    )


def test_alice_perte_premier_repas():
    try:
        food_data = FoodData()
        food_data.deserialize("src/data/data.json")
        profile = Profile("Alice", 20, 165, 58, "Femme", 53)
        nap = 1.375
        meals_per_day = 3

        needs = profile.get_nutritional_needs(nap)
        target_cal = needs["calories"] / meals_per_day
        target_prot = needs["proteines_g"] / meals_per_day
        target_fat = needs["lipides_g"] / meals_per_day
        target_carb = needs["glucides_g"] / meals_per_day

        menu = profile.generate_menu(food_data, nap=nap, meals_per_day=meals_per_day)
        print(
            check_nutritional_targets(
                menu, target_cal, target_prot, target_fat, target_carb
            )
        )
    except Exception:
        print(False)


def test_bob_masse_apres_dejeuner():
    try:
        food_data = FoodData()
        food_data.deserialize("src/data/data.json")
        dejeuner = make_menu(
            [
                ("Riz blanc cuit", 150, 2.7, 130, 0.3, 28),
                ("Poulet cru", 130, 22, 120, 2.5, 0),
                ("Brocoli cuit", 100, 2.8, 35, 0.4, 5),
            ]
        )
        profile = Profile("Bob", 22, 180, 75, "Homme", 82)
        profile.eating_habits.append(dejeuner)
        nap = 1.725
        meals_per_day = 4

        needs = profile.get_nutritional_needs(nap)
        consumed_cal = sum(f.macros[0].calorie for f in dejeuner.content)
        consumed_prot = sum(f.macros[0].proteine for f in dejeuner.content)
        consumed_fat = sum(f.macros[0].fat for f in dejeuner.content)
        consumed_carb = sum(f.macros[0].carbohydrate for f in dejeuner.content)

        target_cal = (needs["calories"] - consumed_cal) / (meals_per_day - 1)
        target_prot = (needs["proteines_g"] - consumed_prot) / (meals_per_day - 1)
        target_fat = (needs["lipides_g"] - consumed_fat) / (meals_per_day - 1)
        target_carb = (needs["glucides_g"] - consumed_carb) / (meals_per_day - 1)

        menu = profile.generate_menu(food_data, nap=nap, meals_per_day=meals_per_day)
        print(
            check_nutritional_targets(
                menu, target_cal, target_prot, target_fat, target_carb
            )
        )
    except Exception:
        print(False)


def test_clara_maintien_collation():
    try:
        food_data = FoodData()
        food_data.deserialize("src/data/data.json")
        petit_dej = make_menu(
            [
                ("Flocons d'avoine", 80, 13, 370, 7, 58),
                ("Yaourt nature", 150, 4, 61, 3.3, 4.7),
                ("Banane", 100, 1.1, 89, 0.3, 23),
            ]
        )
        dejeuner = make_menu(
            [
                ("Pâtes cuites", 200, 5, 158, 0.9, 31),
                ("Thon en boîte", 100, 25, 116, 1, 0),
            ]
        )
        diner = make_menu(
            [
                ("Lentilles cuites", 180, 9, 116, 0.4, 20),
                ("Saumon cru", 120, 20, 208, 13, 0),
            ]
        )
        profile = Profile("Clara", 35, 168, 62, "Femme", 62)
        profile.eating_habits.extend([petit_dej, dejeuner, diner])
        nap = 1.55
        meals_per_day = 5

        needs = profile.get_nutritional_needs(nap)
        consumed_cal = sum(
            sum(f.macros[0].calorie for f in m.content)
            for m in [petit_dej, dejeuner, diner]
        )
        consumed_prot = sum(
            sum(f.macros[0].proteine for f in m.content)
            for m in [petit_dej, dejeuner, diner]
        )
        consumed_fat = sum(
            sum(f.macros[0].fat for f in m.content)
            for m in [petit_dej, dejeuner, diner]
        )
        consumed_carb = sum(
            sum(f.macros[0].carbohydrate for f in m.content)
            for m in [petit_dej, dejeuner, diner]
        )

        target_cal = (needs["calories"] - consumed_cal) / (meals_per_day - 3)
        target_prot = (needs["proteines_g"] - consumed_prot) / (meals_per_day - 3)
        target_fat = (needs["lipides_g"] - consumed_fat) / (meals_per_day - 3)
        target_carb = (needs["glucides_g"] - consumed_carb) / (meals_per_day - 3)

        menu = profile.generate_menu(food_data, nap=nap, meals_per_day=meals_per_day)
        print(
            check_nutritional_targets(
                menu, target_cal, target_prot, target_fat, target_carb
            )
        )
    except Exception:
        print(False)


def test_david_perte_journee_complete():
    try:
        food_data = FoodData()
        food_data.deserialize("src/data/data.json")
        profile = Profile("David", 28, 178, 88, "Homme", 80)
        nap = 1.55
        meals_per_day = 3

        needs = profile.get_nutritional_needs(nap)
        target_cal = needs["calories"] / meals_per_day
        target_prot = needs["proteines_g"] / meals_per_day
        target_fat = needs["lipides_g"] / meals_per_day
        target_carb = needs["glucides_g"] / meals_per_day

        menus = []
        for _ in range(3):
            menu = profile.generate_menu(
                food_data, nap=nap, meals_per_day=meals_per_day
            )
            menus.append(menu)

        all_valid = all(
            check_nutritional_targets(
                m, target_cal, target_prot, target_fat, target_carb
            )
            for m in menus
        )
        print(all_valid)
    except Exception:
        print(False)


def test_emma_sedentaire_repas_unique():
    try:
        food_data = FoodData()
        food_data.deserialize("src/data/data.json")
        profile = Profile("Emma", 45, 162, 70, "Femme", 65)
        nap = 1.2
        meals_per_day = 1

        needs = profile.get_nutritional_needs(nap)
        target_cal = needs["calories"]
        target_prot = needs["proteines_g"]
        target_fat = needs["lipides_g"]
        target_carb = needs["glucides_g"]

        menu = profile.generate_menu(food_data, nap=nap, meals_per_day=meals_per_day)
        print(
            check_nutritional_targets(
                menu, target_cal, target_prot, target_fat, target_carb
            )
        )
    except Exception:
        print(False)
