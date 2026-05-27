from copy import deepcopy
from src.models.settings import Settings
from src.models.menu import Menu
from src.models.food_menu import FoodMenu
from src.models.macro import Macro
import json
import tempfile

# OUTILS

def print_test(name, ok):
    symbol = "✓" if ok else "X"
    color = "\033[92m" if ok else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol} {name}{reset}")


def print_section(name):
    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}")


# 1. MUTATION DES PROFILS (SIDE EFFECT GLOBAL STATE)

def test_profile_mutation_affects_settings():
    try:
        s = Settings()

        s.create_profile("Alex", 20, 180, 75, "M", 70)

        profile = s.profiles[0]
        profile.name = "MODIFIED"

        result = s.profiles[0].name == "MODIFIED"

        print_test("profile_mutation_affects_settings", result)
        return result

    except Exception:
        print_test("profile_mutation_affects_settings", False)
        return False


# 2. DELETE PROFILE BUG (DOUBLE LOOP REMOVE RISK)

def test_delete_profile_removes_correctly():
    try:
        s = Settings()

        s.create_profile("A", 20, 170, 70, "F", 65)
        s.create_profile("B", 25, 180, 80, "M", 75)

        s.delete_profile("A")

        names = [p.name for p in s.profiles]
        result = "A" not in names and "B" in names

        print_test("delete_profile_removes_correctly", result)
        return result

    except Exception:
        print_test("delete_profile_removes_correctly", False)
        return False

# 3. SET FAVORITES: MUTABLE OBJECTS PROBLEM

def test_favorites_set_mutability_issue():
    try:
        s = Settings()

        menu = Menu("2024-01-01")
        s.favorites_menus.add(menu)

        # modifier le menu après insertion dans un set
        menu.content.append(
            FoodMenu(150, "Chicken", [Macro(100, 25, 150, 10, 20)])
        )

        # danger: mutation après hash
        result = len(s.favorites_menus) == 1

        print_test("favorites_set_mutability_issue", result)
        return result

    except Exception:
        print_test("favorites_set_mutability_issue", False)
        return False
