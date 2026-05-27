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

# Résumé final


print(f"\n{'═'*55}")
print(f"  Résultats : {passed} ✓ réussi(s)  |  {failed} ✗ échoué(s)")
print(f"{'═'*55}\n")

if failed > 0:
    sys.exit(1)