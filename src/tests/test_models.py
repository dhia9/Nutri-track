from copy import deepcopy
from src.models.food import Food
from src.models.food_menu import FoodMenu
from src.models.macro import Macro
from src.models.menu import Menu

# MACRO TESTS


def test_macro_masse_negative_raises_error():
    try:
        Macro(-10, 20, 100, 5, 15)
        print(False)
    except ValueError as e:
        print("La masse doit être positive" in str(e))


def test_macro_scaling_affects_all_values():
    macro_100g = Macro(100, 25, 150, 10, 20)
    macro_50g = Macro(50, 25, 150, 10, 20)
    print(
        macro_100g.proteine == 25
        and macro_50g.proteine == 12.5
        and macro_100g.calorie == 150
        and macro_50g.calorie == 75
        and macro_100g.fat == 10
        and macro_50g.fat == 5
        and macro_100g.carbohydrate == 20
        and macro_50g.carbohydrate == 10
    )


def test_macro_zero_masse_creates_zero_values():
    macro = Macro(0, 25, 150, 10, 20)
    print(
        macro.proteine == 0
        and macro.calorie == 0
        and macro.fat == 0
        and macro.carbohydrate == 0
    )


# FOOD TESTS


def test_food_shares_macro_references():
    macros = [Macro(100, 25, 150, 10, 20)]
    food = Food("Chicken", macros)
    macros.append(Macro(150, 30, 200, 12, 25))
    print(food.macros is macros and len(food.macros) == 2)


def test_food_score_with_zero_calories_returns_zero():
    macro = Macro(100, 25, 0, 10, 20)
    food = Food("Empty Food", [macro])
    score = food.score(150, 25, 10, 20, 100)
    print(score == 0.0)


# FOODMENU TESTS


def test_foodmenu_inherits_from_food():
    macros = [Macro(100, 25, 150, 10, 20)]
    food_menu = FoodMenu(150, "Chicken", macros)
    print(
        food_menu.name == "Chicken"
        and food_menu.quantity == 150
        and isinstance(food_menu, Food)
    )


# MENU TESTS


def test_menu_add_food_mutates_content():
    menu = Menu("2024-01-01")
    macro = Macro(100, 25, 150, 10, 20)
    food = Food("Chicken", [macro])
    menu.add_food_menu(food, 150)
    print(
        len(menu.content) == 1
        and menu.content[0].name == "Chicken"
        and menu.content[0].quantity == 150
    )


def test_menu_hash_allows_use_in_set():
    menu1 = Menu("2024-01-01")
    menu2 = Menu("2024-01-01")
    menu3 = Menu("2024-01-02")
    menu_set = {menu1, menu2, menu3}
    print(len(menu_set) == 2)


# CROSS MODEL TESTS


def test_deepcopy_independence():
    menu1 = Menu("2024-01-01")
    macro = Macro(100, 25, 150, 10, 20)
    food = Food("Chicken", [macro])
    menu1.add_food_menu(food, 150)
    menu2 = deepcopy(menu1)
    menu2.content.clear()
    print(len(menu1.content) == 1 and len(menu2.content) == 0)
