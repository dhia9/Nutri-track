from copy import deepcopy
from src.models.settings import Settings
from src.models.menu import Menu
from src.models.food_menu import FoodMenu
from src.models.macro import Macro
import json
import tempfile

# SETTINGS TESTS


def test_profile_mutation_affects_settings():
    s = Settings()
    s.create_profile("Alex", 20, 180, 75, "M", 70)
    profile = s.profiles[0]
    profile.name = "MODIFIED"
    print(s.profiles[0].name == "MODIFIED")


def test_delete_profile_removes_correctly():
    s = Settings()
    s.create_profile("A", 20, 170, 70, "F", 65)
    s.create_profile("B", 25, 180, 80, "M", 75)
    s.delete_profile("A")
    names = [p.name for p in s.profiles]
    print("A" not in names and "B" in names)


def test_favorites_set_mutability_issue():
    s = Settings()
    menu = Menu("2024-01-01")
    s.favorites_menus.add(menu)
    menu.content.append(FoodMenu(150, "Chicken", [Macro(100, 25, 150, 10, 20)]))
    print(len(s.favorites_menus) == 1)


def test_shared_macro_reference_across_food():
    s = Settings()
    macros = [Macro(100, 20, 200, 10, 30)]
    food1 = FoodMenu(100, "Rice", macros)
    food2 = FoodMenu(200, "Rice", macros)
    macros.append(Macro(150, 30, 250, 12, 40))
    print(len(food1.macros) == len(food2.macros))


def test_deepcopy_isolation_settings():
    s1 = Settings()
    s1.create_profile("X", 20, 180, 70, "M", 65)
    s2 = deepcopy(s1)
    s2.profiles[0].name = "CHANGED"
    print(s1.profiles[0].name != s2.profiles[0].name)


def test_deserialize_structure_integrity():
    s = Settings()
    fake_data = {
        "profiles": [
            {
                "name": "A",
                "age": 20,
                "height": 180,
                "weight": 70,
                "sex": "M",
                "target_weight": 65,
                "eating_habits": [],
            }
        ],
        "favorites_menus": [],
    }
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        json.dump(fake_data, f)
        path = f.name
    s.deserialize(path)
    print(len(s.profiles) == 1 and s.profiles[0].name == "A")


def test_menu_set_hash_stability_risk():
    m = Menu("2024-01-01")
    s = Settings()
    s.favorites_menus.add(m)
    m.content.append(FoodMenu(100, "Chicken"))
    print(m in s.favorites_menus)
