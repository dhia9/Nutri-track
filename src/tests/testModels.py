import sys
from datetime import date
from src.data.food_data import FoodData
from src.models.food import Food
from src.models.macro import Macro
from src.models.menu import Menu
from src.models.profile import Profile
from src.models.macro_type import MacroType
passed = 0
failed = 0


def ok(label: str):
    global passed
    passed += 1
    print(f"  ✓ {label}")


def fail(label: str, detail: str = ""):
    global failed
    failed += 1
    msg = f"  ✗ {label}"
    if detail:
        msg += f"\n      → {detail}"
    print(msg)


def assert_approx(val, expected, label: str, tol=0.5):
    if abs(val - expected) <= tol:
        ok(label)
    else:
        fail(label, f"obtenu {val:.4f}, attendu {expected:.4f} (tolérance ±{tol})")


def section(title: str):
    print(f"\n{'═'*55}")
    print(f"  {title}")
    print(f"{'═'*55}")

# SECTION 1 — MacroType

section("1. MacroType — unicité et valeurs")

print("\n  Vérifie que l'énumération MacroType contient bien les 4 types")
print("  attendus et que chaque valeur est distincte.\n")
membres = list(MacroType)
if len(membres) == 4:
    ok("MacroType contient exactement 4 membres")
else:
    fail("MacroType devrait contenir 4 membres", f"trouvé : {len(membres)}")

valeurs = [m.value for m in membres]
if len(valeurs) == len(set(valeurs)):
    #verifer en supprimant les doublans
    ok("Toutes les valeurs de MacroType sont distinctes")
else:
    fail("Des valeurs de MacroType sont dupliquées", str(valeurs))

noms_attendus = {"CALORIE", "PROTEIN", "FAT", "CARBOHYDRATE"}
noms_reels = {m.name for m in membres}
if noms_reels == noms_attendus:
    ok("Les noms des membres correspondent exactement aux 4 macronutriments")
else:
    fail("Noms inattendus dans MacroType", f"trouvé : {noms_reels}")


# SECTION 2 — Macro : scaling par masse

section("2. Macro — scaling par masse")

print("\n  Macro reçoit des valeurs nutritionnelles POUR 100g et les")
print("  scale automatiquement selon la masse passée.\n")

print("  Cas : 100g de poulet (25g prot, 165 kcal, 3.6g lip, 0g gluc)")
m100 = Macro(masse=100, proteine=25, calorie=165, fat=3.6, carbohydrate=0)
assert_approx(m100.proteine,      25.0, "Protéines à 100g = 25.0g (facteur 1)")
assert_approx(m100.calorie,      165.0, "Calories à 100g = 165 kcal (facteur 1)")
assert_approx(m100.fat,            3.6, "Lipides  à 100g = 3.6g  (facteur 1)")
assert_approx(m100.carbohydrate,   0.0, "Glucides à 100g = 0.0g  (facteur 1)")

print("\n  Cas : 150g (portion par défaut) — valeurs doivent être × 1.5")
m150 = Macro(masse=150, proteine=25, calorie=165, fat=3.6, carbohydrate=0)
assert_approx(m150.proteine,      37.5,   "Protéines à 150g = 37.5g  (×1.5)")
assert_approx(m150.calorie,      247.5,   "Calories  à 150g = 247.5 kcal (×1.5)")
assert_approx(m150.fat,            5.4,   "Lipides   à 150g = 5.4g   (×1.5)")

print("\n  Cas : 30g (portion minimale) — valeurs doivent être × 0.3")
m30 = Macro(masse=30, proteine=25, calorie=165, fat=3.6, carbohydrate=10)
assert_approx(m30.proteine,        7.5,   "Protéines à 30g = 7.5g   (×0.3)")
assert_approx(m30.calorie,        49.5,   "Calories  à 30g = 49.5 kcal (×0.3)")
assert_approx(m30.carbohydrate,    3.0,   "Glucides  à 30g = 3.0g   (×0.3)")

print("\n  Cas limite : masse = 0g → toutes les valeurs doivent être 0")
m0 = Macro(masse=0, proteine=25, calorie=165, fat=3.6, carbohydrate=10)
assert_approx(m0.calorie,    0.0, "Calories à 0g = 0.0 kcal")
assert_approx(m0.proteine,   0.0, "Protéines à 0g = 0.0g")

print("\n  Cas limite : masse négative → ValueError attendue")
try:
    m_neg = Macro(masse=-10, proteine=25, calorie=165, fat=3.6, carbohydrate=0)
    fail("Masse négative : ValueError non levée")
except ValueError:
    ok("Masse négative lève bien ValueError")

print("\n  Vérification du __str__ de Macro")
s = str(m100)
if "165" in s and "25" in s:
    ok("__str__ contient les calories et protéines")
else:
    fail("__str__ ne contient pas les valeurs attendues", s)

# ─────────────────────────────────────────────
# SECTION 3 — Profile.get_imc
# ─────────────────────────────────────────────

section("3. Profile — calcul de l'IMC")

print("\n  IMC = poids (kg) / taille² (m)\n")

p = Profile("Test", age=30, height=1.75, weight=70, sex="Homme", target_weight=70)
imc = p.get_imc()
print(f"  Profil : 70 kg / 1.75 m → IMC attendu ≈ 22.86")
assert_approx(imc, 22.86, "IMC calculé ≈ 22.86", tol=0.01)

p2 = Profile("Test2", age=25, height=1.60, weight=55, sex="Femme", target_weight=55)
imc2 = p2.get_imc()
print(f"\n  Profil : 55 kg / 1.60 m → IMC attendu ≈ 21.48")
assert_approx(imc2, 21.48, "IMC calculé ≈ 21.48", tol=0.01)

print("\n  Cas limite : taille = 0 → retourne 0 (pas de division par zéro)")
p_zero = Profile("Zero", age=30, height=0, weight=70, sex="Homme", target_weight=70)
if p_zero.get_imc() == 0:
    ok("Taille = 0 → IMC = 0 (division par zéro évitée)")
else:
    fail("Taille = 0 devrait retourner IMC = 0")

# SECTION 4 — Profile.get_nutritional_needs


section("4. Profile — besoins nutritionnels (Mifflin-St Jeor)")

print("\n  Formule Homme : 10×poids + 6.25×taille − 5×âge + 5, × NAP")
print("  Formule Femme : 10×poids + 6.25×taille − 5×âge − 161, × NAP\n")

# Homme, maintien
ph = Profile("Homme", age=30, height=175, weight=75, sex="Homme", target_weight=75)
mb_h = 10 * 75 + 6.25 * 175 - 5 * 30 + 5       # = 1818.75
det_h = mb_h * 1.55                              # ≈ 2819.06
cal_attendu_h = det_h + 0                        # maintien
needs_h = ph.get_nutritional_needs(nap=1.55)
print(f"  Homme 75kg/175cm/30ans, maintien → calories attendues ≈ {cal_attendu_h:.0f} kcal")
assert_approx(needs_h["calories"], cal_attendu_h, "Calories homme/maintien", tol=1.0)
if needs_h["proteines_g"] > 0 and needs_h["lipides_g"] > 0 and needs_h["glucides_g"] > 0:
    ok("Toutes les macros sont positives pour un profil valide")
else:
    fail("Au moins une macro est nulle ou négative")

# Femme, maintien
pf = Profile("Femme", age=25, height=165, weight=60, sex="Femme", target_weight=60)
mb_f = 10 * 60 + 6.25 * 165 - 5 * 25 - 161     # = 1420.25
det_f = mb_f * 1.55                              # ≈ 2201.39
needs_f = pf.get_nutritional_needs(nap=1.55)
print(f"\n  Femme 60kg/165cm/25ans, maintien → calories attendues ≈ {det_f:.0f} kcal")
assert_approx(needs_f["calories"], det_f, "Calories femme/maintien", tol=1.0)

# Objectifs — ajustement calorique
print("\n  Ajustements selon objectif :")
# Note : pour comparer l'ajustement exact (+300 / -400), il faut un profil
# dont le poids == target_weight (maintien), puis simuler les deux autres
# objectifs en changeant uniquement target_weight sur le MÊME poids de base.
# Si les poids diffèrent entre profils, le MB change et l'écart n'est plus 400/300.

p_base = Profile("Base", age=30, height=175, weight=75, sex="Homme", target_weight=75)
n_maint = p_base.get_nutritional_needs()["calories"]   # target == weight → maintien

p_base.target_weight = 80   # → objectif masse  (target > weight)
n_masse = p_base.get_nutritional_needs()["calories"]

p_base.target_weight = 70   # → objectif perte  (target < weight)
n_perte = p_base.get_nutritional_needs()["calories"]

p_base.target_weight = 75   # reset

if n_perte < n_maint:
    ok("Objectif perte → calories < maintien (−400 kcal appliqué)")
else:
    fail("Objectif perte devrait donner moins de calories que le maintien",
         f"perte={n_perte:.0f}, maintien={n_maint:.0f}")

if n_masse > n_maint:
    ok("Objectif masse → calories > maintien (+300 kcal appliqué)")
else:
    fail("Objectif masse devrait donner plus de calories que le maintien",
         f"masse={n_masse:.0f}, maintien={n_maint:.0f}")

diff_perte = n_maint - n_perte
diff_masse = n_masse - n_maint
assert_approx(diff_perte, 400, "Écart perte/maintien = exactement 400 kcal", tol=1.0)
assert_approx(diff_masse, 300, "Écart masse/maintien = exactement 300 kcal", tol=1.0)

# SECTION 5 — Profile.get_meal_budget


section("5. Profile — budget du repas")

print("\n  Budget = (besoins − déjà consommé) / repas restants")
print("  Le budget ne peut jamais être négatif.\n")

today = str(date.today())

# Aucun repas enregistré → budget = besoins / meals_per_day
p_clean = Profile("Clean", age=30, height=175, weight=75, sex="Homme", target_weight=75)
besoins = p_clean.get_nutritional_needs(1.55)
cal_b, *_ = p_clean.get_meal_budget(nap=1.55, meals_per_day=3, today=today)
attendu_clean = besoins["calories"] / 3
print(f"  0 repas enregistrés, 3 repas/jour → budget cal ≈ {attendu_clean:.0f} kcal")
assert_approx(cal_b, attendu_clean, "Budget 1er repas = besoins/3", tol=1.0)

# Budget négatif impossible : on consomme plus que les besoins
print("\n  Si les besoins sont dépassés → budget = 0 (jamais négatif)")
p_over = Profile("Over", age=30, height=175, weight=75, sex="Homme", target_weight=75)
macro_surcharge = Macro(masse=100, proteine=100, calorie=5000, fat=100, carbohydrate=500)
food_surcharge = Food("Surcharge", [macro_surcharge])
menu_surcharge = Menu(today)
menu_surcharge.add_food_menu(food_surcharge, quantity=100)
p_over.eating_habits.append(menu_surcharge)
cal_budget_over, prot_budget_over, fat_budget_over, carb_budget_over = \
    p_over.get_meal_budget(nap=1.55, meals_per_day=3, today=today)
if cal_budget_over == 0.0:
    ok("Budget calorique = 0.0 quand les besoins sont dépassés")
else:
    fail("Budget calorique devrait être 0 si besoins dépassés", f"obtenu : {cal_budget_over:.2f}")

# Avec 2 repas déjà faits sur 3 → il reste 1 repas
print("\n  2 repas déjà faits sur 3 → le budget porte sur le 1 repas restant")
p_2done = Profile("TwoDone", age=30, height=175, weight=75, sex="Homme", target_weight=75)
macro_small = Macro(masse=100, proteine=10, calorie=200, fat=5, carbohydrate=25)
for _ in range(2):
    m = Menu(today)
    m.add_food_menu(Food("Riz", [macro_small]), quantity=100)
    p_2done.eating_habits.append(m)
besoins2 = p_2done.get_nutritional_needs(1.55)
cal_b2, *_ = p_2done.get_meal_budget(nap=1.55, meals_per_day=3, today=today)
cal_restante = max(0.0, besoins2["calories"] - 2 * macro_small.calorie)
print(f"  Calories restantes attendues (1 repas) ≈ {cal_restante:.0f} kcal")
assert_approx(cal_b2, cal_restante, "Budget = calories restantes / 1 repas", tol=1.0)


# Résumé final


print(f"\n{'═'*55}")
print(f"  Résultats : {passed} ✓ réussi(s)  |  {failed} ✗ échoué(s)")
print(f"{'═'*55}\n")

if failed > 0:
    sys.exit(1)