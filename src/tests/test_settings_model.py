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

# 4. DOUBLE REFERENCE LIST (SHARED FOOD MACROS)

def test_shared_macro_reference_across_food():
    try:
        s = Settings()

        macros = [Macro(100, 20, 200, 10, 30)]
        food1 = FoodMenu(100, "Rice", macros)
        food2 = FoodMenu(200, "Rice", macros)

        macros.append(Macro(150, 30, 250, 12, 40))

        result = len(food1.macros) == len(food2.macros)

        print_test("shared_macro_reference_across_food", result)
        return result

    except Exception:
        print_test("shared_macro_reference_across_food", False)
        return False


# 5. DEEPCOPY PROTECTION TEST

def test_deepcopy_isolation_settings():
    try:
        s1 = Settings()
        s1.create_profile("X", 20, 180, 70, "M", 65)

        s2 = deepcopy(s1)

        s2.profiles[0].name = "CHANGED"

        result = s1.profiles[0].name != s2.profiles[0].name

        print_test("deepcopy_isolation_settings", result)
        return result

    except Exception:
        print_test("deepcopy_isolation_settings", False)
        return False


# 6. DESERIALIZE DATA CONSISTENCY RISK

def test_deserialize_structure_integrity():
    try:
        s = Settings()

        # simulation JSON minimal valide
        fake_data = {
            "profiles": [
                {
                    "name": "A",
                    "age": 20,
                    "height": 180,
                    "weight": 70,
                    "sex": "M",
                    "target_weight": 65,
                    "eating_habits": []
                }
            ],
            "favorites_menus": []
        }

        

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            json.dump(fake_data, f)
            path = f.name

        s.deserialize(path)

        result = len(s.profiles) == 1 and s.profiles[0].name == "A"

        print_test("deserialize_structure_integrity", result)
        return result

    except Exception:
        print_test("deserialize_structure_integrity", False)
        return False


# 7. SET BEHAVIOR WITH MUTABLE OBJECTS

def test_menu_set_hash_stability_risk():
    try:
        m = Menu("2024-01-01")
        s = Settings()

        s.favorites_menus.add(m)

        # mutation après insertion dans set
        m.content.append(FoodMenu(100, "Chicken"))

        # l'objet reste dans le set mais son état a changé
        result = m in s.favorites_menus

        print_test("menu_set_hash_stability_risk", result)
        return result

    except Exception:
        print_test("menu_set_hash_stability_risk", False)
        return False