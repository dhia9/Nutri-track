from datetime import date

from src.data.food_data import FoodData
from src.models.food import Food
from src.models.macro import Macro
from src.models.menu import Menu
from src.models.profile import Profile

# Fonctions utilitaires pour les tests


def make_menu(items: list[tuple[str, float, float, float, float, float]]) -> Menu:
    """Crée un Menu pré-rempli pour simuler un repas déjà enregistré.
    
    Args:
        items: Liste de tuples (nom, masse_g, proteine/100g, calorie/100g, fat/100g, carb/100g).
        
    Returns:
        Un Menu créé avec les aliments spécifiés.
    """
    menu = Menu(str(date.today()))
    for name, masse, prot, cal, fat, carb in items:
        menu.add_food_menu(
            Food(name, [Macro(masse, prot, cal, fat, carb)]), quantity=masse
        )
    return menu


def print_menu(menu: Menu, label: str = ""):
    """Affiche le contenu d'un menu avec ses macros.
    
    Args:
        menu: Le menu à afficher.
        label: Label optionnel pour identifier le menu.
    """
    print(f"\n  {'─' * 20} {label} {'─' * 20}")
    for f in menu.content:
        m = f.macros[0]
        print(
            f"  {f.name:<25} {f.quantity:>4}g "
            f"| {m.calorie:>6.1f} kcal "
            f"| P:{m.proteine:>5.1f}g "
            f"| L:{m.fat:>5.1f}g "
            f"| G:{m.carbohydrate:>5.1f}g"
        )
    total_cal = sum(f.macros[0].calorie for f in menu.content)
    total_prot = sum(f.macros[0].proteine for f in menu.content)
    total_fat = sum(f.macros[0].fat for f in menu.content)
    total_carb = sum(f.macros[0].carbohydrate for f in menu.content)
    print(
        f"  {'TOTAL':<25}      "
        f"| {total_cal:>6.1f} kcal "
        f"| P:{total_prot:>5.1f}g "
        f"| L:{total_fat:>5.1f}g "
        f"| G:{total_carb:>5.1f}g"
    )


def print_daily_summary(profile: Profile, nap: float):
    """Affiche un résumé des macros consommés vs objectifs pour la journée.
    
    Args:
        profile: Le profil pour lequel afficher le bilan.
        nap: Le facteur d'activité physique.
    """
    besoins = profile.get_nutritional_needs(nap)
    today = str(date.today())
    menus = [m for m in profile.eating_habits if m.date == today]
    all_foods = [f for m in menus for f in m.content]

    consumed_cal = sum(f.macros[0].calorie for f in all_foods)
    consumed_prot = sum(f.macros[0].proteine for f in all_foods)
    consumed_fat = sum(f.macros[0].fat for f in all_foods)
    consumed_carb = sum(f.macros[0].carbohydrate for f in all_foods)

    print(f"\n  {'─' * 20} Bilan journalier {'─' * 20}")
    print(f"  {'':25}   {'Consommé':>10}  {'Objectif':>10}  {'Écart':>10}")
    for label, consumed, target in [
        ("Calories (kcal)", consumed_cal, besoins["calories"]),
        ("Protéines (g)", consumed_prot, besoins["proteines_g"]),
        ("Lipides (g)", consumed_fat, besoins["lipides_g"]),
        ("Glucides (g)", consumed_carb, besoins["glucides_g"]),
    ]:
        ecart = consumed - target
        print(f"  {label:<25}   {consumed:>10.1f}  {target:>10.1f}  {ecart:>+10.1f}")


def run_scenario(
    food_data: FoodData,
    profile: Profile,
    nap: float,
    meals_per_day: int,
    existing_menus: list[Menu],
    description: str,
):
    """Exécute un scénario de génération de menu.
    
    Génére un menu pour un profil donné avec les conditions spécifiées
    et affiche les résultats.
    
    Args:
        food_data: Base de données des aliments.
        profile: Le profil pour lequel générer un menu.
        nap: Facteur d'activité physique.
        meals_per_day: Nombre de repas par jour.
        existing_menus: Menus déjà enregistrés pour cette journée.
        description: Description du scénario.
    """
    print(f"\n{'═' * 60}")
    print(f" {profile.name} | {description}")
    print(
        f" Objectif poids : {profile.weight}kg → {profile.target_weight}kg"
        f" | NAP {nap} | {meals_per_day} repas/jour"
    )
    print(f"{'═' * 60}")

    # Enregistre les repas déjà effectués
    for i, m in enumerate(existing_menus):
        profile.eating_habits.append(m)
        print_menu(m, label=f"Repas existant {i + 1}")

    # Génère le repas suivant
    generated = profile.generate_menu(food_data, nap=nap, meals_per_day=meals_per_day)
    profile.eating_habits.append(generated)
    print_menu(
        generated, label=f"Repas généré ({len(existing_menus) + 1}/{meals_per_day})"
    )

    print_daily_summary(profile, nap)


# Scénarios


def test_alice_perte_premier_repas(food_data):
    """Fonction de test : Femme en perte de poids avec aucun repas enregistré, génére le petit-déjeuner.
    
    Args:
        food_data: Base de données des aliments.
    """
    run_scenario(
        food_data,
        profile=Profile("Alice", 20, 165, 58, "Femme", 53),
        nap=1.375,
        meals_per_day=3,
        existing_menus=[],
        description="Perte de poids — 1er repas de la journée",
    )


def test_bob_masse_apres_dejeuner(food_data):
    """Fonction de test : Homme en prise de masse avec déjeuner déjà fait, génére le dîner.
    
    Args:
        food_data: Base de données des aliments.
    """
    dejeuner = make_menu(
        [
            ("Riz blanc cuit", 150, 2.7, 130, 0.3, 28),
            ("Poulet cru", 130, 22, 120, 2.5, 0),
            ("Brocoli cuit", 100, 2.8, 35, 0.4, 5),
        ]
    )
    run_scenario(
        food_data,
        profile=Profile("Bob", 22, 180, 75, "Homme", 82),
        nap=1.725,
        meals_per_day=4,
        existing_menus=[dejeuner],
        description="Prise de masse — après le déjeuner",
    )


def test_clara_maintien_collation(food_data):
    """Fonction de test : Femme en maintien avec 3 repas sur 5 déjà faits, génére une collation.
    
    Args:
        food_data: Base de données des aliments.
    """
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
    run_scenario(
        food_data,
        profile=Profile("Clara", 35, 168, 62, "Femme", 62),
        nap=1.55,
        meals_per_day=5,
        existing_menus=[petit_dej, dejeuner, diner],
        description="Maintien — collation après 3 repas",
    )


def test_david_perte_journee_complete(food_data):
    """Fonction de test : Homme en perte de poids et génére les 3 repas un par un.
    
    Args:
        food_data: Base de données des aliments.
    """
    profile = Profile("David", 28, 178, 88, "Homme", 80)
    nap = 1.55

    print(f"\n{'═' * 60}")
    print(f" {profile.name} | Perte de poids — génération repas par repas")
    print(f" {profile.weight}kg → {profile.target_weight}kg | NAP {nap} | 3 repas/jour")
    print(f"{'═' * 60}")

    for i in range(3):
        menu = profile.generate_menu(food_data, nap=nap, meals_per_day=3)
        profile.eating_habits.append(menu)
        print_menu(menu, label=f"Repas {i + 1}/3")

    print_daily_summary(profile, nap)


def test_emma_sedentaire_repas_unique(food_data):
    """Fonction de test : Femme sédentaire avec 1 seul repas par jour.
    
    Args:
        food_data: Base de données des aliments.
    """
    run_scenario(
        food_data,
        profile=Profile("Emma", 45, 162, 70, "Femme", 65),
        nap=1.2,
        meals_per_day=1,
        existing_menus=[],
        description="Sédentaire — repas unique",
    )


if __name__ == "__main__":
    food_data = FoodData()
    food_data.deserialize("../data/data.json")

    test_alice_perte_premier_repas(food_data)
    test_bob_masse_apres_dejeuner(food_data)
    test_clara_maintien_collation(food_data)
    test_david_perte_journee_complete(food_data)
    test_emma_sedentaire_repas_unique(food_data)
