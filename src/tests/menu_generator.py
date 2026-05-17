from src.data.food_data import FoodData
from src.models.profile import Profile


def test_generate_menu():
    food_data = FoodData()
    food_data.deserialize("../data/data.json")

    profiles = [
        ("Alice", 20, 165, 58, "Femme", 55, 1.375, 3),
        ("Bob", 22, 180, 80, "Homme", 85, 1.55, 4),
        ("Clara", 35, 170, 65, "Femme", 65, 1.2, 2),
        ("David", 28, 175, 70, "Homme", 68, 1.725, 5),
    ]

    for name, age, height, weight, sex, target, nap, meals in profiles:
        profile = Profile(name, age, height, weight, sex, target)
        menu = profile.generate_menu(food_data, nap, meals)

        total_cal = sum(f.macros[0].calorie for f in menu.content)
        total_prot = sum(f.macros[0].proteine for f in menu.content)

        print(f"\n{'=' * 50}")
        print(f"Profil : {name} | {weight} -> {target} | {meals} repas/jour")
        print(f"{'=' * 50}")
        for food_menu in menu.content:
            m = food_menu.macros[0]
            print(f"  {food_menu.name:<25} {food_menu.quantity:>4}g "
                  f"| {m.calorie:>6.1f} kcal "
                  f"| P:{m.proteine:>5.1f}g "
                  f"| L:{m.fat:>5.1f}g "
                  f"| G:{m.carbohydrate:>5.1f}g")
        print(f"  {'TOTAL':<25}       | {total_cal:>6.1f} kcal | P:{total_prot:>5.1f}g")


if __name__ == "__main__":
    test_generate_menu()
