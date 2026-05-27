from copy import deepcopy
from src.models.food import Food
from src.models.food_menu import FoodMenu
from src.models.macro import Macro
from src.models.menu import Menu

def print_test(test_name, status):
    symbol = "✓" if status else "✗"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol} {test_name}{reset}")


def print_section(section_name):
    print(f"\n{'=' * 60}")
    print(f"  {section_name}")
    print(f"{'=' * 60}")

# MACRO TESTS

def test_macro_masse_negative_raises_error():
    try:
        Macro(-10, 20, 100, 5, 15)
        print_test("test_macro_masse_negative_raises_error", False)
        return False
    except ValueError as e:
        result = "La masse doit être positive" in str(e)
        print_test("test_macro_masse_negative_raises_error", result)
        return result


def test_macro_scaling_affects_all_values():
    try:
        macro_100g = Macro(100, 25, 150, 10, 20)
        macro_50g = Macro(50, 25, 150, 10, 20)

        result = (
            macro_100g.proteine == 25 and
            macro_50g.proteine == 12.5 and
            macro_100g.calorie == 150 and
            macro_50g.calorie == 75 and
            macro_100g.fat == 10 and
            macro_50g.fat == 5 and
            macro_100g.carbohydrate == 20 and
            macro_50g.carbohydrate == 10
        )

        print_test("test_macro_scaling_affects_all_values", result)
        return result

    except Exception:
        print_test("test_macro_scaling_affects_all_values", False)
        return False


def test_macro_zero_masse_creates_zero_values():
    try:
        macro = Macro(0, 25, 150, 10, 20)

        result = (
            macro.proteine == 0 and
            macro.calorie == 0 and
            macro.fat == 0 and
            macro.carbohydrate == 0
        )

        print_test("test_macro_zero_masse_creates_zero_values", result)
        return result

    except Exception:
        print_test("test_macro_zero_masse_creates_zero_values", False)
        return False

# FOOD TESTS

def test_food_shares_macro_references():
    try:
        macros = [Macro(100, 25, 150, 10, 20)]
        food = Food("Chicken", macros)

        macros.append(Macro(150, 30, 200, 12, 25))

        result = (
            food.macros is macros and
            len(food.macros) == 2
        )

        print_test("test_food_shares_macro_references", result)
        return result

    except Exception:
        print_test("test_food_shares_macro_references", False)
        return False


def test_food_score_with_zero_calories_returns_zero():
    try:
        macro = Macro(100, 25, 0, 10, 20)
        food = Food("Empty Food", [macro])

        score = food.score(150, 25, 10, 20, 100)

        result = score == 0.0

        print_test("test_food_score_with_zero_calories_returns_zero", result)
        return result

    except Exception:
        print_test("test_food_score_with_zero_calories_returns_zero", False)
        return False

